from rest_framework import serializers

from .models import CarModel


# class CarSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     brand = serializers.CharField(max_length=25)
#     price = serializers.IntegerField()
#     year = serializers.IntegerField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         car = CarModel.objects.create(**validated_data)
#         return car
#
#     def update(self, instance, validated_data):
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()
#         return instance

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        # fields='__all__'
        fields = ('id', 'brand', 'price', 'year', 'created_at', 'updated_at',)