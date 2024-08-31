from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test_user@test.ru", password="test_password", tg_chat_id=692738945)
        self.another_user = User.objects.create(email="test_another_user@test.ru", password="test_password")

    def test_authenticated_user(self):
        response = self.client.get(reverse('habits:habits-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):
        data = {
            'email': 'test_user_create@test.ru',
            'password': 'test_password',
            "tg_chat_id": 692738945
        }

        response = self.client.post(reverse('users:user_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="test_user@test.ru")
        self.assertIsNotNone(user)
        self.assertEqual(user.password, 'test_password')

    def test_user_update(self):
        data = {
            'email': 'test_user1@test.ru',
            'password': 'test_password1',
            "tg_chat_id": 692738945,
            'first_name': 'Test'
        }

        # тестирование текущим пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('users:user_update', kwargs={'pk': self.user.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('email'), 'test_user1@test.ru')
        self.assertEqual(response.json().get('password'), 'test_password1')
        self.assertEqual(response.json().get('first_name'), 'Test')

        # тестирование внешним пользователем
        self.client.force_authenticate(user=self.another_user)
        response = self.client.put(reverse('users:user_update', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_retrieve(self):
        # тестирование текущим пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:user_retrieve', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('password'), 'test_password')
        self.assertEqual(response.json().get('email'), 'test_user@test.ru')
        self.assertEqual(response.json().get('first_name'), '')
        self.assertEqual(response.json().get('last_name'), '')
        self.assertEqual(response.json().get('tg_chat_id'), '692738945')

        # тестирование внешним пользователем
        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(reverse('users:user_retrieve', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_destroy(self):
        # тестирование текущим пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('users:user_destroy', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # тестирование внешним пользователем
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(reverse('users:user_destroy', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
