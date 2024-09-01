import json
from datetime import datetime, timedelta
import pytz
import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import status
from rest_framework.reverse import reverse
from config import settings
from habits.models import Habit
from rest_framework.exceptions import APIException

ZONE = pytz.timezone(settings.TIME_ZONE)
NOW = datetime.now(ZONE)


def send_tg_message(habit_pk):
    habit = Habit.objects.get(pk=habit_pk)

    if habit.related_habit:
        text_reward = f'приятной привычкой:\n{habit.related_habit}'
    elif habit.reward:
        text_reward = habit.reward

    params = {
        'text': f'Выполните привычку:\n\n{habit}\nза {habit.time_to_complete}\n\nИ вознаградите себя {text_reward}!',
        'chat_id': habit.user.tg_chat_id,
    }
    response = requests.get(f'{settings.TG_URL}{settings.TG_TOKEN}/sendMessage', params=params)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        raise APIException(f'Cначала начните диалог с telegram-ботом! Получить ссылку на бота вы можете '
                           f'по URL-адресу: {reverse("habits:tg_bot_link")}')


def create_periodic_task(every, time, habit_pk):
    period = IntervalSchedule.DAYS
    schedule = IntervalSchedule.objects.create(every=every, period=period)

    start_time = time.astimezone(ZONE) + timedelta(minutes=2)

    PeriodicTask.objects.create(
        interval=schedule,
        name=f'Send telegram message {habit_pk}',
        task='habits.tasks.send_tg_message',
        args=json.dumps(habit_pk),
        start_time=start_time
    )
