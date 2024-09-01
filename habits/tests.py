from datetime import timedelta, datetime
import pytz
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from config import settings
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_owner = User.objects.create(email="test_owner@test.ru", password="test_password")
        self.standart_user = User.objects.create(email="test_standart@test.ru", password="test_password")

        self.enjoyable_habit = Habit.objects.create(user=self.user_owner, place='test', time='2024-08-31 12:00:00',
                                                    action='test', is_enjoyable=True,
                                                    time_to_complete=timedelta(minutes=1))

        zone = pytz.timezone(settings.TIME_ZONE)
        self.now = datetime.now(zone)

    def test_create_habit(self):
        data = {
            'place': 'test',
            'time': '2024-08-31 12:00:00',
            'action': 'test',
            'is_enjoyable': False,
            'related_habit': self.enjoyable_habit.pk,
            'periodicity_every': 3,
            'time_to_complete': timedelta(minutes=1),
            'is_public': True
        }

        self.client.force_authenticate(user=self.user_owner)
        response = self.client.post(reverse('habits:habits-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'pk': self.enjoyable_habit.pk + 1,
            'user': self.user_owner.pk,
            'place': 'test',
            'time': '2024-08-31T12:00:00+04:00',
            'action': 'test',
            'is_enjoyable': False,
            'related_habit': self.enjoyable_habit.pk,
            'periodicity_every': 3,
            'time_to_complete': '00:01:00',
            'is_public': True,
            'reward': None
        })

    def test_create_habit_with_error(self):
        not_enjoyable_habit = Habit.objects.create(user=self.user_owner, place='test',
                                                   time='2024-08-31 12:00:00', action='test',
                                                   is_enjoyable=False, time_to_complete=timedelta(minutes=1))

        data_with_reward_and_related_habit = {
            'place': 'test',
            'time': '2024-08-31 12:00:00',
            'action': 'test',
            'is_enjoyable': False,
            'related_habit': not_enjoyable_habit.pk,
            'time_to_complete': timedelta(minutes=3),
            'is_public': True,
            'reward': 'test',
        }

        data_without_reward_and_related_habit = {
            'place': 'test',
            'time': '2024-08-31 12:00:00',
            'action': 'test',
            'is_enjoyable': False,
            'time_to_complete': timedelta(minutes=1),
            'is_public': True,
        }

        data_enjoyable_habit = {
            'place': 'test',
            'time': '2024-08-31 12:00:00',
            'action': 'test',
            'is_enjoyable': True,
            'related_habit': not_enjoyable_habit.pk,
            'time_to_complete': timedelta(minutes=1),
            'is_public': True,
        }

        data_periodicity_every = {
            'place': 'test',
            'time': '2024-08-31 12:00:00',
            'action': 'test',
            'is_enjoyable': True,
            'periodicity_every': 8,
            'time_to_complete': timedelta(minutes=1),
            'is_public': True,
        }

        self.client.force_authenticate(user=self.user_owner)

        response = self.client.post(reverse('habits:habits-list'), data=data_with_reward_and_related_habit)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('non_field_errors'), [
            "У полезной привычки нельзя указывать связанную привычку и вознаграждение одновременно!",
            "Время выполнения не должно быть больше 2-х минут!",
            "У полезной привычки в связанных привычках может быть только приятная привычка!"
        ])

        response = self.client.post(reverse('habits:habits-list'), data=data_without_reward_and_related_habit)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('non_field_errors'), [
            "У полезной привычки обязательно должна быть либо связанная привычка, либо вознаграждение!"
        ])

        response = self.client.post(reverse('habits:habits-list'), data=data_enjoyable_habit)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('non_field_errors'), [
            "У приятной привычки не может быть связанной привычки или вознаграждения!"
        ])

        response = self.client.post(reverse('habits:habits-list'), data=data_periodicity_every)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('non_field_errors'), [
            "Привычку нельзя выполнять реже, чем раз в неделю!"
        ])

    def test_retrieve_lesson(self):
        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'pk': self.enjoyable_habit.pk,
            'user': self.user_owner.pk,
            'place': 'test',
            'time': '2024-08-31T12:00:00+04:00',
            'action': 'test',
            'is_enjoyable': True,
            'related_habit': None,
            'periodicity_every': 1,
            'time_to_complete': '00:01:00',
            'is_public': False,
            'reward': None
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.get(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lesson(self):
        Habit.objects.create(user=self.user_owner, place='test', time='2024-08-31 12:00:00',
                             action='test', is_enjoyable=True,
                             time_to_complete=timedelta(minutes=1))

        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('habits:habits-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    'pk': self.enjoyable_habit.pk,
                    'user': self.user_owner.pk,
                    'place': 'test',
                    'time': '2024-08-31T12:00:00+04:00',
                    'action': 'test',
                    'is_enjoyable': True,
                    'related_habit': None,
                    'periodicity_every': 1,
                    'time_to_complete': '00:01:00',
                    'is_public': False,
                    'reward': None
                },
                {
                    'pk': self.enjoyable_habit.pk + 1,
                    'user': self.user_owner.pk,
                    'place': 'test',
                    'time': '2024-08-31T12:00:00+04:00',
                    'action': 'test',
                    'is_enjoyable': True,
                    'related_habit': None,
                    'periodicity_every': 1,
                    'time_to_complete': '00:01:00',
                    'is_public': False,
                    'reward': None
                }
            ]
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.get(reverse('habits:habits-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_update_lesson(self):
        # тестирование метода владельцем
        data = {
            'place': 'test-update',
            'time': '2024-08-31 12:00:00',
            'action': 'test-update',
            'is_enjoyable': True,
            'periodicity_every': 7,
            'time_to_complete': timedelta(minutes=1),
            'is_public': True
        }

        self.client.force_authenticate(user=self.user_owner)
        response = self.client.put(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'pk': self.enjoyable_habit.pk,
            'user': self.user_owner.pk,
            'place': 'test-update',
            'time': '2024-08-31T12:00:00+04:00',
            'action': 'test-update',
            'is_enjoyable': True,
            'related_habit': None,
            'periodicity_every': 7,
            'time_to_complete': '00:01:00',
            'is_public': True,
            'reward': None
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.put(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_lesson(self):
        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # тестирование метода обычным пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.delete(reverse('habits:habits-detail', kwargs={'pk': self.enjoyable_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitPublicListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(email="test_1@test.ru", password="test_password")
        self.user_2 = User.objects.create(email="test_2@test.ru", password="test_password")

        self.habit_not_public = Habit.objects.create(user=self.user_1, place='test', time='2024-08-31 12:00:00',
                                                     action='test', is_enjoyable=True,
                                                     time_to_complete=timedelta(minutes=1))
        self.habit_public_1 = Habit.objects.create(user=self.user_2, place='test', time='2024-08-31 12:00:00',
                                                   action='test', is_enjoyable=True,
                                                   time_to_complete=timedelta(minutes=1),
                                                   is_public=True)
        self.habit_public_2 = Habit.objects.create(user=self.user_1, place='test', time='2024-08-31 12:00:00',
                                                   action='test', is_enjoyable=True,
                                                   time_to_complete=timedelta(minutes=1),
                                                   is_public=True)

        zone = pytz.timezone(settings.TIME_ZONE)
        self.now = datetime.now(zone)

    def test_habit_public_list(self):
        # тестирование пользователем user_1
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('habits:habit_public_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    'pk': self.habit_public_1.pk,
                    'place': 'test',
                    'time': '2024-08-31T12:00:00+04:00',
                    'action': 'test',
                    'is_enjoyable': True,
                    'related_habit': None,
                    'periodicity_every': 1,
                    'time_to_complete': '00:01:00',
                    'reward': None,
                    'user': {'avatar': None,
                             'country': None,
                             'email': 'test_2@test.ru',
                             'first_name': '',
                             'last_name': '',
                             'phone': None}
                }
            ]
        })

        # тестирование пользователем user_2
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(reverse('habits:habit_public_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    'pk': self.habit_public_2.pk,
                    'place': 'test',
                    'time': '2024-08-31T12:00:00+04:00',
                    'action': 'test',
                    'is_enjoyable': True,
                    'related_habit': None,
                    'periodicity_every': 1,
                    'time_to_complete': '00:01:00',
                    'reward': None,
                    'user': {'avatar': None,
                             'country': None,
                             'email': 'test_1@test.ru',
                             'first_name': '',
                             'last_name': '',
                             'phone': None}
                }
            ]
        })


class GetTGBotTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru", password="test_password")

    def test_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habits:tg_bot_link'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'tg_bot_link': 'https://t.me/habittt_reminder_bot'})
