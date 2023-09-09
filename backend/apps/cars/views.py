from django.db.models import Q
from django.forms import model_to_dict
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from core.permissions.is_super_user import IsSuperUser

from .filters import CarFilter
from .models import CarModel
from .serializers import CarSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(ListAPIView):
    '''
        Get all cars
    '''
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    filterset_class = CarFilter
    permission_classes = (AllowAny,)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    '''
        get:
            Get car by id
        put:
            Full update car by id
        patch:
            Partial update car by id
        delete:
            Delete car by id

    '''
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
