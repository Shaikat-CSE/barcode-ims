from django.utils.functional import SimpleLazyObject
from .models import User
from mongoengine.errors import DoesNotExist

class AnonymousUser:
    """
    A class that mimics Django's AnonymousUser.
    """
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False
    
    def __str__(self):
        return 'AnonymousUser'
    
    @property
    def is_anonymous(self):
        return True
    
    @property
    def is_authenticated(self):
        return False

def get_user(request):
    """
    Get the user from the session.
    """
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return AnonymousUser()
    
    try:
        return User.objects.get(id=user_id)
    except DoesNotExist:
        return AnonymousUser()

class MongoEngineAuthMiddleware:
    """
    Middleware for authenticating users with MongoEngine.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set the user attribute on the request
        request.user = SimpleLazyObject(lambda: get_user(request))
        
        # Get response
        response = self.get_response(request)
        
        return response 