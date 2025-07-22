from django.contrib.auth.backends import BaseBackend
from mongoengine.errors import DoesNotExist
from .models import User

class MongoEngineBackend(BaseBackend):
    """
    Custom authentication backend for MongoEngine User model.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on username/email and password.
        """
        if username is None or password is None:
            return None
        
        try:
            # Try to find the user by username
            user = User.objects.get(username=username)
        except DoesNotExist:
            try:
                # Try to find the user by email
                user = User.objects.get(email=username)
            except DoesNotExist:
                # No user found with this username or email
                return None
        
        # Check if the password is correct
        if user.check_password(password):
            return user
        
        # Password is incorrect
        return None
    
    def get_user(self, user_id):
        """
        Retrieve a user by their ID.
        """
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None 