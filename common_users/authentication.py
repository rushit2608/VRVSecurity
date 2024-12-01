from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils import timezone
import datetime


class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self):
        super().__init__()

    def authenticate(self, request):
        return super().authenticate(request)
    
    def get_validated_token(self, raw_token):
        """
            To validate JWT token if user changes/resets password.
        """
        validated_token = super().get_validated_token(raw_token)
        user = self.get_user(validated_token)

        if user.last_password_change:
            iat = datetime.datetime.fromtimestamp(validated_token['iat'], tz=timezone.utc)
            if iat < user.last_password_change:
                print("CustomJWTAuthentication: Token is invalid due to password change")  
                raise InvalidToken("Token is invalid due to a recent password change.")

        return validated_token