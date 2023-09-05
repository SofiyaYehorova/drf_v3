from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView

from apps.users.models import UserModel as User

from .filters import UserFilter
from rest_framework.permissions import AllowAny

UserModel: User = get_user_model()
from .serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    filterset_class = UserFilter
    permission_classes = (AllowAny,)
