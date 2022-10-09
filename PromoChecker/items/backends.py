from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    """Pluggable Backend authentication system class
    """
    
    def authenticate(
        self,
        request=None,
        username=None,
        password=None,
        **kwargs
    ):
        UserModel = get_user_model()
        
        # print(username) 1st field in the login page id is username
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            
        try:
            case_insensitive_username_field = f"{UserModel.USERNAME_FIELD}__iexact"
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
            
        