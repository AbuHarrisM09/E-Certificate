import random
import subprocess

from ECertificate.api.auth.serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer, ChangePasswordSerializer

from course.models import OTP
from rest_framework import generics
from django.utils import timezone


from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework.generics import GenericAPIView

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

class SendOTPView(GenericAPIView):

    serializer_class = SendOTPSerializer

    @csrf_exempt
    def post(self, request):
        data = self.request.data
        email = data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with email does not exist.'}, status=404)

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP ke database
        otp_obj, created = OTP.objects.update_or_create(
            email=email, 
            defaults={
                'otp': otp,
                'created_at': timezone.now()
            })

        # Kirim otp ke user
        from_email = 'Median Talenta Raya', settings.EMAIL_HOST_USER
        subject = 'OTP Untuk Mereset Password Anda.'
        message = f'OTP Milikmu : {otp}. akan kadaluarsa dalam 10 menit.'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'detail': 'OTP dikirim.'})


class VerifyOTPAPIView(GenericAPIView):

    serializer_class = VerifyOTPSerializer

    @csrf_exempt
    def post(self, request):
        data = self.request.data
        email = data['email']
        otp = data['otp']

        User = get_user_model()
        user = User.objects.get(email=email)
        try:
            otp_obj = OTP.objects.get(email=email, otp=otp)
        except OTP.DoesNotExist:
            return JsonResponse({'error': 'Invalid OTP!.'}, status=400)

        # Cek jika otp kadaluarsa
        if otp_obj.is_expired():
            return JsonResponse({'error': 'OTP telah kadaluarsa!.'}, status=400)

        refresh = RefreshToken.for_user(user)
        response = JsonResponse({'detail': 'OTP terverifikasi.'}, status=200)
        response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)
        response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)

        # Verifikasi OTP
        otp_obj.is_verified = True
        otp_obj.save()
        
        return response


class ChangePasswordView(GenericAPIView):

    serializer_class = ChangePasswordSerializer

    def post(self, request):
        # Get password baru
        data = self.request.data
        password = request.data.get('password')

        # Generate access token menggunakan refresh token
        refresh = request.COOKIES.get('refresh_token')
        if not refresh:
            return Response({'detail': 'Refresh token not found.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = RefreshToken(refresh)
            token.verify()
        except Exception:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Set password baru untuk user
        User = get_user_model()
        user = User.objects.get(id=token['user_id'])
        user.set_password(password)
        user.save()

        # Generate access token baru
        new_refresh = RefreshToken.for_user(user)
        response = Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=str(new_refresh.access_token), httponly=True)

        return response