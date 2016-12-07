from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework.authtoken.models import Token

def custom_jwt_payload_handler(user):
    payload = jwt_payload_handler(user)
    # payload['token'] = user.
    tokens = Token.objects.filter(user=user)
    if len(tokens) > 0:
        payload['token'] = tokens[0].key

    return payload
