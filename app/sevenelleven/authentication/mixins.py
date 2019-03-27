import json

import jwt

from .models import User as UserModel
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_exempt

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

User = UserModel()


class JSONWebTokenAuthMixin():
    """Authenticated the user with JSONWebTokenAuthMixinBase only if
    the authentication was provided."""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user, request.token = self.authenticate(request)
        except exceptions.AuthenticationFailed as e:
            response = HttpResponse(
                json.dumps({
                    'errors': [str(e)]
                }),
                status=401,
                content_type='application/json'
            )

            return response

        return super().dispatch(request, *args, **kwargs)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        try:
            user_id = payload['user_id']

            if user_id:
                user = User.objects.get(pk=user_id, is_active=True)

                return user
            else:
                msg = 'Invalid payload'
                raise exceptions.AuthenticationFailed(msg)
        except User.DoesNotExist:
            msg = 'Invalid signature'
            raise exceptions.AuthenticationFailed(msg)

    def authenticate(self, request):  # noqa [C901]
        # if user is already authenticated (for example via session)
        # skip the header auth

        if request.user.is_authenticated:
            return (request.user, None)

        auth = get_authorization_header(request).split()

        if not auth:
            return (AnonymousUser(), None)

        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            raise exceptions.AuthenticationFailed()

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = (
                'Invalid Authorization header. Credentials string '
                'should not contain spaces.'
            )
            raise exceptions.AuthenticationFailed(msg)

        try:
            payload = jwt_decode_handler(auth[1])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)

        return (user, auth[1])
