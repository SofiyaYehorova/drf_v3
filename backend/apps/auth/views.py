from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.dataclasses.user_dataclass import UserDataClass
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken, SocketToken

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

from .serializers import EmailSerializer, PasswordSerializer

UserModel: User = get_user_model()


class MeView(RetrieveAPIView):
    '''
        get:
            User can get information about himself
    '''
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ActivateUserView(GenericAPIView):
    '''
        post:
            Create token for activate user
    '''
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        token = kwargs['token']
        user: User = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class RecoveryPasswordRequestView(GenericAPIView):
    '''
        post:
            Create token for request to recovery password
    '''

    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_password(user)
        return Response('Check your email', status.HTTP_200_OK)


class RecoveryPasswordView(GenericAPIView):
    '''
       post:
           Create token for to recovery password
   '''
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        data = self.request.data  # дістали password
        serializer = self.get_serializer(data=data)  # отримали екземпляр serializer
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user: User = JWTService.validate_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response('password changed', status.HTTP_200_OK)


class AuthTokenView(GenericAPIView):
    def get(self, *args, **kwargs):
        token = JWTService.create_token(self.request.user, SocketToken)
        return Response({'token': str(token)}, status.HTTP_200_OK)
