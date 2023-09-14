from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.cars.models import CarModel
from apps.users.models import UserModel as User

from ..models import AutoParkModel

UserModel: User = get_user_model()


class AutoParkTestCase(APITestCase):
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

    def test_create_auto_parks_without_auth(self):
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            'name': 'User'
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(AutoParkModel.objects.count(), count)

    def test_create_auto_park(self):
        self._authenticate()
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['name'], "Uber")  # перевіряємо чи назви одинакові
        # self.assertIsInstance(response.data['cars'], list)  # перевіряємо мавив даних і чи є він списком
        self.assertEquals(AutoParkModel.objects.count(), count + 1)

    def test_add_car_to_auto_park(self):
        self._authenticate()
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        pk = response.data['id']

        prev_count = CarModel.objects.count()
        sample_car = {
            "brand": "Audi",
            "body": "Coupe",
            "price": 15000,
            "year": 2016
        }
        cars_count = len(self.client.get(reverse('auto_parks_list_create_car', args=(pk,))).data)
        response_cars = self.client.post(reverse('auto_parks_list_create_car', args=(pk,)), sample_car)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(CarModel.objects.count(), prev_count + 1)
        self.assertEquals(len(str(response_cars.data['id'])), cars_count + 1)

    def test_update_retrieve_destroy_auto_park_by_id(self):
        self._authenticate()
        count_auto_parks = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        pk = response.data['id']

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(AutoParkModel.objects.count(), count_auto_parks + 1)

        sample_auto_park_update = {
            "name": "Uklon"
        }
        response_put = self.client.put(reverse('auto_parks_retrieve_update_destroy', args=(pk,)),
                                       sample_auto_park_update)
        response_destroy = self.client.delete(reverse('auto_parks_retrieve_update_destroy', args=(pk,)))

        self.assertEquals(response_put.status_code, status.HTTP_200_OK)
        self.assertEquals(response_put.data['name'], "Uklon")
        self.assertEquals(response_destroy.status_code, status.HTTP_204_NO_CONTENT)
