from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import os


@api_view(('POST',))
def authenticate(req):
    code = req.POST.get('code', None)

    if code is None:
        return Response(dict(message="Code not provided"),status=status.HTTP_401_UNAUTHORIZED)

    access_token = get_access_token(code)

    if access_token:
        user_info = get_user_info(access_token)
        if user_info:
            return Response(dict(user=user_info), status=status.HTTP_200_OK)

        return Response(dict(message="User not found"), status=status.HTTP_404_NOT_FOUND)

    return Response(dict(message="Invalid code"),status=status.HTTP_400_BAD_REQUEST)


def get_access_token(code):
    GITHUB_OAUTH_ACCESS_TOKEN_URL="https://github.com/login/oauth/access_token"
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', None)
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', None)

    params = {'client_id': GITHUB_CLIENT_ID,'client_secret': GITHUB_CLIENT_SECRET, 'code': code}
    headers = {'accept':"application/json"}
    access_token_res = requests.post(GITHUB_OAUTH_ACCESS_TOKEN_URL,params=params,headers=headers)
    print("/access_token Response:", access_token_res.status_code)

    access_token = access_token_res.json().get('access_token')

    return access_token

def get_user_info(access_token):
    GITHUB_USER_INFO_URL = "https://api.github.com/user"

    headers = {'authorization': "token "+ access_token}
    user_info_res = requests.get(GITHUB_USER_INFO_URL,headers=headers)
    print("/user_info Response:", user_info_res.status_code)

    if user_info_res.status_code == 200:
        user_info = user_info_res.json()
        return user_info

    return None
