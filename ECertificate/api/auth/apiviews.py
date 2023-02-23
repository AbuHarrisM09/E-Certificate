import subprocess

from ECertificate.api.auth.serializers import UserSerializer

from rest_framework import generics

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import status, APIView

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class LoginView(generics.CreateAPIView):

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            username = list(User.objects.get(id=user.id).username)
            username_string = "".join(username)
            subprocess.run('py manage.py flushexpiredtokens')
            return Response(
                {
                    "username": username_string,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                }

                , status=status.HTTP_200_OK)
        return Response({"error": "Username atau Password Salah!"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            subprocess.run('py manage.py flushexpiredtokens')
            return Response({"detail": "Logout Berhasil!"})
        except Exception as e:
            return Response({"detail": "Token Tidak Valid!"})