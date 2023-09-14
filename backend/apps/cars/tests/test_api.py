from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

from ...auto_parks.models import AutoParkModel
from ..models import CarModel

UserModel: User = get_user_model()


class CarsTestCase(APITestCase):
    def _authenticate(self):
        email = "admin@gmail.com"
        password = "P@$$word1"
        user = {
            "email": email,
            "password": password,
            "profile": {
                "name": "Іван",
                "surname": "Попов",
                "age": 20

            }
        }
        self.client.post(reverse('users_list_create'), user, format='json')
        user = UserModel.objects.get(email=user['email'])
        user.is_active = True
        user.is_staff = True
        user.save()
        response = self.client.post(reverse('auth_login'), {"email": email, "password": password})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_update_retrieve_destroy_cars(self):
        self._authenticate()
        count_auto_park = AutoParkModel.objects.count()

        sample_auto_park = {
            "name": "Uber"
        }
        response_auto_park = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        pk = response_auto_park.data['id']

        prev_count_cars = CarModel.objects.count()
        sample_car = {
            "brand": "Audi",
            "body": "Jeep",
            "price": 15000,
            "year": 2016
        }

        response_cars = self.client.post(reverse('auto_parks_list_create_car', args=(pk,)), sample_car)
        response_get_all_cars = self.client.get(reverse('cars_get_all_cars'))

        self.assertEquals(response_auto_park.status_code, status.HTTP_201_CREATED)
        self.assertEquals(AutoParkModel.objects.count(), count_auto_park + 1)
        self.assertEquals(response_cars.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response_get_all_cars.status_code, status.HTTP_200_OK)

        def test_update_retrieve_destroy_car_by_id(self):
            self._authenticate()
            count_auto_park = AutoParkModel.objects.count()

            sample_auto_park = {
                "name": "Uber"
            }
            response_auto_park = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
            pk = response_auto_park.data['id']

            prev_count_cars = CarModel.objects.count()
            sample_car = {
                "brand": "Audi",
                "body": "Jeep",
                "price": 15000,
                "year": 2016
            }

            sample_car_put = {
                "brand": "BMW",
                "body": "Coupe",
                "price": 16000,
                "year": 2018
            }
            sample_car_patch = {
                "brand": "Kia",
                "body": "Jeep",
            }
            response_car = self.client.post(reverse('auto_parks_list_create_car', args=(pk,)), sample_car)
            response_put = self.client.put(reverse('cars_retrieve_update_destroy', args=(pk,)), sample_car_put)
            response_patch = self.client.patch(reverse('cars_retrieve_update_destroy', args=(pk,)), sample_car_patch)
            response_destroy = self.client.delete(reverse('cars_retrieve_update_destroy', args=(pk,)))

            self.assertEquals(response_auto_park.status_code, status.HTTP_201_CREATED)
            self.assertEquals(response_car.status_code, status.HTTP_201_CREATED)
            self.assertEquals(AutoParkModel.objects.count(), count_auto_park+1)
            self.assertEquals(CarModel.objects.count(), prev_count_cars+1)
            self.assertEquals(response_put.data, sample_car_put)
            self.assertEquals(response_patch.data, sample_car_patch)
            self.assertEquals(response_destroy.status, status.HTTP_204_NO_CONTENT)
