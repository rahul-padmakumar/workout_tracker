from rest_framework_simplejwt.authentication import (
  JWTAuthentication, InvalidToken
)


class CustomAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        token_iat = validated_token.get('iat')

        if user.password_reset_on and (
              token_iat < user.password_reset_on.timestamp()
        ):
            raise InvalidToken('Please log in again.')

        return user
