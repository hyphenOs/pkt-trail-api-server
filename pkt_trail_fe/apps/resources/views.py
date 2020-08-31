import os
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import AccessToken

from pkt_trail_fe.settings import BASE_DIR


class CustomPermission(BasePermission):
    message = "Invalid or Expired Token"

    def has_permission(self, req, view):

        header = self.get_header(req)
        if header is None:
            return False

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return False

        validated_token = self.get_validated_token(raw_token)
        if validated_token is None:
            return False

        return True


    def get_header(self, req):
        header = req.META.get("HTTP_AUTHORIZATION")

        return header

    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) != 2:
            return None

        if parts[0] != "Bearer":
            return None

        return parts[1]

    def get_validated_token(self, raw_token):
        try:
            return AccessToken(raw_token)
        except Exception as e:
            print(e)

        # raise InvalidJWT()


class InvalidJWT(APIException):
    status_code = 403
    default_detail = "Invalid token"
    default_code = "service_unavailable"


class ResourceView(APIView):
    permission_classes = [CustomPermission, ]

    def get(self, req):
        resources_json_path = BASE_DIR + "/sample_jsons/resources.json"
        with open(resources_json_path) as f:
            resources = json.load(f)

        content = {'resources': resources}
        return Response(content, status=status.HTTP_200_OK)



