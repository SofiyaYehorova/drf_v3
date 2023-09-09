from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permissions import IsAdminOrWriteOnlyPermission, IsSuperUser

from apps.users.models import UserModel as User

from .filters import UserFilter

UserModel: User = get_user_model()
from core.services.email_service import EmailService

from .serializers import AvatarSerializer, UserSerializer


class UserListCreateView(ListCreateAPIView):
    '''
        get:
            Get all users
        post:
            Create user

    '''
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    filterset_class = UserFilter
    permission_classes = (IsAdminOrWriteOnlyPermission,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserAddAvatarView(UpdateAPIView):  # підкапотно використовує два методи put and patch
    '''
        put:
            Update a model instance(user) add photo
    '''
    serializer_class = AvatarSerializer
    http_method_names = ('put',)  # вказуємо який з методів будемо використовути, інший метод заблоковано

    def get_object(self):
        return UserModel.objects.all_with_profiles().get(pk=self.request.user.pk).profile

    def perform_update(self, serializer):
        self.get_object().avatar.delete()
        super().perform_update(serializer)


class UserToAdminView(GenericAPIView):
    '''
           patch:
               Changing permission from user to admin
       '''
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    '''
        patch:
            Changing permission from admin to user
    '''
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    '''
       patch:
           Block user
   '''
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    '''
       patch:
           Unblock user
   '''
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockAdminUserView(BlockUserView):
    '''
       patch:
           Block admin(can do this just superuser)
    '''
    permission_classes = (IsSuperUser,)


class UnBlockAdminUserView(UnBlockUserView):
    '''
       patch:
           Unblock admin(can do this just superuser)
    '''
    permission_classes = (IsSuperUser,)


class TestEmailView(GenericAPIView):
    '''
        get user email for check it
    '''
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        EmailService.test_email()
        return Response('ok')
