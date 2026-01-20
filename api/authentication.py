import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Users
from rest_framework.status import HTTP_401_UNAUTHORIZED

class MyCustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 1. Отримуємо заголовок Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # 2. Перевіряємо формат (очікуємо: Bearer <token>)
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Invalid Authorization header format. Expected: Bearer <token>')

        token = parts[1]

        # 3. Декодуємо токен
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception:
            raise exceptions.AuthenticationFailed('Authentication error')

        # 4. ПЕРЕВІРКА ТИПУ (тепер payload вже існує)
        if payload.get('type') != 'access':
            raise exceptions.AuthenticationFailed('Use Access token, not Refresh')
        try:
            # Використовуємо .get(), бо id унікальний
            user = Users.objects.get(id=payload['user_id'])
        except Users.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found.')
        except KeyError:
            raise exceptions.AuthenticationFailed('Token does not contain user_id')

        # 6. Повертаємо (user, auth). auth зазвичай None або сам токен
        return (user, token)