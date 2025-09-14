from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from auth.serializers import UserRequestSerializer
from commons.jwt_utils import JWTUtils


# Create your views here.

class AuthView(ViewSet):


    @swagger_auto_schema(request_body=UserRequestSerializer, responses={200: "{'message': 'Login successful',"
                                         "'token': 'IDTOKEN'}",
                                    401: "{'message': 'Username or password incorrect'}"})
    @action(detail=False, methods=['POST'], url_path='login')
    def login(self,request):
        user_request_credentials = UserRequestSerializer(data=request.data)
        if user_request_credentials.is_valid():
            user: User = authenticate(**user_request_credentials.validated_data)
            if user:
                print(f"auth: {user.get_username()} {user.get_group_permissions()}")
                token_body_info = {
                    "user": user.get_username(),
                    "permissions": [permission for permission in user.get_group_permissions()]
                }
                token = JWTUtils.encode(token_body_info)
                return Response({
                    "message": "Login successful",
                    "token": token
                },status=status.HTTP_200_OK)

        return Response({
            "message": "Username or password incorrect",
        }, status=status.HTTP_401_UNAUTHORIZED)