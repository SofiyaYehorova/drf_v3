from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer

from .models import AutoParkModel
from .serializers import AutoParkSerializer


class AutoParkListCreateView(ListCreateAPIView):
    '''
        get:
            Get all auto parks
        post:
            Create auto park
    '''
    serializer_class = AutoParkSerializer  # for create
    queryset = AutoParkModel.objects.prefetch_related('cars')  # for get
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsAdminUser(),)


class AutoParkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    '''
        get:
            Get aut park by id
        put:
            Full update auto park by id
        patch:
            Partial update auto park by id
        delete:
            Destroy auto park by id
    '''
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()


class AutoParkCarListCreateView(GenericAPIView):
    '''
        get:
            Get car by auto_park id
        post:
            Create car for auto_park id
    '''
    queryset = AutoParkModel.objects.all()

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        exist = AutoParkModel.objects.filter(pk=pk).exists()
        if not exist:
            raise Http404()
        cars = CarModel.objects.filter(auto_park_id=pk)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        exists = AutoParkModel.objects.filter(pk=pk).exists()
        if not exists:
            raise Http404()
        serializer.save(auto_park_id=pk)
        return Response(serializer.data, status.HTTP_201_CREATED)
