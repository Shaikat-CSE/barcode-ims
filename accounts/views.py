from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.utils import timezone
from django.contrib.auth import login as auth_login

def register_view(request):
    """View for user registration"""
    if request.user.is_authenticated:
        return redirect('inventory:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """View for user login"""
    # Check if user is already logged in
    if request.session.get('_auth_user_id'):
        return redirect('inventory:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            # Try to find the user by username or email
            try:
                # Try username first
                user = User.objects.get(username=username)
            except:
                try:
                    # Try email next
                    user = User.objects.get(email=username)
                except:
                    # No user found
                    messages.error(request, 'Invalid username or password.')
                    return render(request, 'accounts/login.html', {'form': form})
            
            # Check password
            if user.check_password(password):
                # Set session data
                request.session['_auth_user_id'] = str(user.id)
                request.session['_auth_user_backend'] = 'accounts.auth_backend.MongoEngineBackend'
                
                # Update last login time
                user.last_login = timezone.now()
                user.save()
                
                # Set session expiry based on remember_me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to the page the user was trying to access, or to home
                next_url = request.GET.get('next', 'inventory:index')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """View for user logout"""
    # Clear session
    if '_auth_user_id' in request.session:
        del request.session['_auth_user_id']
    if '_auth_user_backend' in request.session:
        del request.session['_auth_user_backend']
    
    # Use Django's logout to clean up any other session data
    logout(request)
    
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """View for user profile"""
    return render(request, 'accounts/profile.html') 