import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_tokens(user = None, refresh_token=None):
    if user:
        access_payload = {
            'user_id': str(user.id),
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(minutes=30),
        }
        refresh_payload = {
            'user_id': str(user.id),
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=30),
        }
        return (
            jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256'),
            jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
        )

    elif refresh_token:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                raise ValueError('Invalid token type')

            user_id = payload['user_id']
            new_access_payload = {
                'user_id': user_id,
                'type': 'access',
                'exp': datetime.utcnow() + timedelta(minutes=30),
            }
            new_refresh_payload = {
                'user_id': user_id,
                'type': 'refresh',
                'exp': datetime.utcnow() + timedelta(days=30),
            }
            return (
                jwt.encode(new_access_payload, settings.SECRET_KEY, algorithm='HS256'),
                jwt.encode(new_refresh_payload, settings.SECRET_KEY, algorithm='HS256')
            )
        except jwt.ExpiredSignatureError:
            raise ValueError('Refresh token has expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid refresh token')
