import os
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken

import requests

from .models import PktTrailUser

_logger = logging.getLogger(__name__)


@api_view(('POST',))
def auth_github(req):
    code = req.POST.get('code', None)

    if code is None:
        return Response(dict(message="Code not provided"),status=status.HTTP_401_UNAUTHORIZED)

    access_token = get_access_token(code)

    if access_token:
        user_info = get_user_info(access_token)
        if user_info:
            username = user_info['login']
            provider = 'Github'
            user = PktTrailUser.objects.filter(username=username, auth_provider=provider).first()

            if user is None:
                toks = user_info['name'].split()
                user_args = {
                        'username': user_info['login'],
                        'provider_id': user_info['id'],
                        'profile_url': user_info['html_url'],
                        'avatar_url': user_info['avatar_url'],
                        'email': user_info['email']
                }

                firstname, lastname = None, None
                if len(toks) < 2:
                    if len(tokens) == 1:
                        firstname = toks[0].strip()
                else:
                    firstname, lastname = toks[0].strip(), toks[1].strip()

                if firstname is not None:
                    user_args['first_name'] =  firstname
                if lastname is not None:
                    user_args['last_name'] =  lastname

                user = PktTrailUser.objects.create(**user_args)

            token_payload = {
                'id': user.id,
                'name': user.first_name or "Stranger",
                'login': '@'.join([user.username, user.auth_provider]),
                'profile_url': user.profile_url,
                'avatar_url': user.avatar_url
            }

            token = get_jwt_token(token_payload)

            return Response(dict(token=token), status=status.HTTP_200_OK)

        return Response(dict(message="User not found"), status=status.HTTP_404_NOT_FOUND)

    return Response(dict(message="Invalid code"),status=status.HTTP_400_BAD_REQUEST)


def get_access_token(code):
    GITHUB_OAUTH_ACCESS_TOKEN_URL="https://github.com/login/oauth/access_token"
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', None)
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', None)

    if GITHUB_CLIENT_ID is None or GITHUB_CLIENT_SECRET is None:
        return None

    params = {'client_id': GITHUB_CLIENT_ID,'client_secret': GITHUB_CLIENT_SECRET, 'code': code}
    headers = {'accept':"application/json"}
    try:
        access_token_res = requests.post(GITHUB_OAUTH_ACCESS_TOKEN_URL,params=params,headers=headers)
    except Exception as e:
        _logger.exception("GitHub Access Token Request")
        return None

    _logger.debug("/access_token Response: %d", access_token_res.status_code)

    access_token = access_token_res.json().get('access_token')

    return access_token


def get_user_info(access_token):
    GITHUB_USER_INFO_URL = "https://api.github.com/user"

    headers = {'authorization': "token "+ access_token}
    try:
        user_info_res = requests.get(GITHUB_USER_INFO_URL,headers=headers)
    except Exception as e:
        _logger.exception("GitHub User Info Request")
        return None
    _logger.debug("/user_info Response: %d", user_info_res.status_code)

    if user_info_res.ok:
        user_info = user_info_res.json()
        return user_info

    return None


def get_jwt_token(payload):
    access = AccessToken()
    access['id'] = payload['id']
    access['name'] = payload['name']
    access['login'] = payload['login']
    access['profile_url'] = payload['profile_url']
    access['avatar_url'] = payload['avatar_url']

    return str(access)
