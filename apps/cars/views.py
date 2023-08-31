from django.http import Http404
from django.forms import model_to_dict
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from .serializers import CarSerializer
from .models import CarModel
from .filters import car_filtered_queryset


# class CarListCreateView(APIView):
#     def get(self, *args, **kwargs):
#         # cars = CarModel.objects.all()
#         # serializer = CarSerializer(cars, many=True)
#         # return Response(serializer.data, status.HTTP_200_OK)
#         # qs = CarModel.objects.all().filter(price__in=[12000, 15000], brand__icontains='m')
#         # qs = CarModel.objects.filter(Q(price=12000) & Q(brand='lada'))
#         # qs = CarModel.objects.filter(Q(price=12000) | Q(brand='ford'))
#         # qs = CarModel.objects.filter(Q(price=12000) | Q(brand='ford')).order_by('price', 'brand')
#         # qs = CarModel.objects.filter(Q(price=12000) | Q(brand='ford')).order_by('price', 'brand').reverse()
#         # qs = CarModel.objects.filter(Q(price=12000) | Q(brand='ford')).order_by('price', 'brand').reverse().exclude(brand='lada')
#         # qs = CarModel.objects.filter(Q(price=12000) | Q(brand='ford')).order_by('price', 'brand').reverse().exclude(brand='lada')[:1]
#         # print(qs.query)
#         qs = car_filtered_queryset(self.request.query_params)
#         serializer = CarSerializer(qs, many=True)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def post(self, *args, **kwargs):
#         data = self.request.data
#         serializer = CarSerializer(data=data)
#
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#         return Response(serializer.data, status.HTTP_201_CREATED)


# class CarRetrieveUpdateDestroyView(APIView):
#     def get(self, *args, **kwargs):
#         pk = kwargs['pk']
#
#         # try:
#         #     car = CarModel.objects.get(pk=pk)
#         # except CarModel.DoesNotExist:
#         #     raise Http404()
#
#         car = get_object_or_404(CarModel, pk=pk)
#         serializer = CarSerializer(car)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def put(self, *args, **kwargs):
#         pk = kwargs['pk']
#         data: dict = self.request.data
#
#         # try:
#         #     car = CarModel.objects.get(pk=pk)
#         # except CarModel.DoesNotExist:
#         #     raise Http404()
#
#         car = get_object_or_404(CarModel, pk=pk)
#         serializer = CarSerializer(car, data)
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def patch(self, *args, **kwargs):
#         pk = kwargs['pk']
#         data: dict = self.request.data
#
#         # try:
#         #     car = CarModel.objects.get(pk=pk)
#         # except CarModel.DoesNotExist:
#         #     raise Http404()
#         car = get_object_or_404(CarModel, pk=pk)
#         serializer = CarSerializer(car, data, partial=True)
#
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def delete(self, *args, **kwargs):
#         pk = kwargs['pk']
#
#         # try:
#         #     car = CarModel.objects.get(pk=pk)
#         #     car.delete()
#         # except CarModel.DoesNotExist:
#         #     raise Http404()
#         car = get_object_or_404(CarModel, pk=pk)
#         car.delete()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CarListCreateView(GenericAPIView):
#     def get(self, *args, **kwargs):
#         qs = car_filtered_queryset(self.request.query_params)
#         serializer = CarSerializer(qs, many=True)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     # def post(self, *args, **kwargs):
#     #     data = self.request.data
#     #     serializer = CarSerializer(data=data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status.HTTP_201_CREATED)
#
#
# class CarRetrieveUpdateDestroyView(GenericAPIView):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()
#
#     # lookup_field = 'my_id' #це якщо не хочеш використовувати 'pk' а хочеш 'my_id'
#
#     def get(self, *args, **kwargs):
#         # pk = kwargs['pk']
#         # car = get_object_or_404(CarModel, pk=pk)
#         car = self.get_object()
#         serializer = CarSerializer(car)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def put(self, *args, **kwargs):
#         pk = kwargs['pk']
#         data: dict = self.request.data
#         car = get_object_or_404(CarModel, pk=pk)
#         serializer = CarSerializer(car, data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def patch(self, *args, **kwargs):
#         # pk = kwargs['pk']
#         # car = get_object_or_404(CarModel, pk=pk)
#         car = self.get_object()
#         data: dict = self.request.data
#         serializer = CarSerializer(car, data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def delete(self, *args, **kwargs):
#         # pk = kwargs['pk']
#         # car = get_object_or_404(CarModel, pk=pk)
#         car = self.get_object()
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CarListView(GenericAPIView, ListModelMixin):
#
#     def get_queryset(self):
#         return car_filtered_queryset(self.request.query_params)
#
#     def get(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#
# # def get(self, *args, **kwargs):
# #     qs = car_filtered_queryset(self.request.query_params)
# #     serializer = CarSerializer(qs, many=True)
# #     return Response(serializer.data, status.HTTP_200_OK)
#
#
# class CarRetrieveUpdateDestroyView(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()
#
#     # def get(self, *args, **kwargs):
#     #     # pk = kwargs['pk']
#     #     # car = get_object_or_404(CarModel, pk=pk)
#     #     car = self.get_object()
#     #     serializer = CarSerializer(car)
#     #     return Response(serializer.data, status.HTTP_200_OK)
#     def get(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
#
#     # def put(self, *args, **kwargs):
#     #     pk = kwargs['pk']
#     #     data: dict = self.request.data
#     #     car = get_object_or_404(CarModel, pk=pk)
#     #     serializer = CarSerializer(car, data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status.HTTP_200_OK)
#     def put(self, request, *args, **kwargs):
#         return super().update(request, *args, **kwargs)
#
#     # def patch(self, *args, **kwargs):
#     #     # pk = kwargs['pk']
#     #     # car = get_object_or_404(CarModel, pk=pk)
#     #     car = self.get_object()
#     #     data: dict = self.request.data
#     #     serializer = CarSerializer(car, data, partial=True)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status.HTTP_200_OK)
#     def patch(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)
#
#     # def delete(self, *args, **kwargs):
#     #     # pk = kwargs['pk']
#     #     # car = get_object_or_404(CarModel, pk=pk)
#     #     car = self.get_object()
#     #     car.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
#     def delete(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)

class CarListView(ListAPIView):

    def get_queryset(self):
        return car_filtered_queryset(self.request.query_params)

    # def get(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()

    # def get(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    #
    # def patch(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)
