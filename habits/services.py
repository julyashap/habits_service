import json
from datetime import datetime, timedelta
import pytz
import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from config import settings
from habits.models import Habit

ZONE = pytz.timezone(settings.TIME_ZONE)
NOW = datetime.now(ZONE)


def send_tg_message(habit_pk):
    habit = Habit.objects.get(pk=habit_pk)

    params = {
        'text': f'Выполните привычку:\n\n{habit}',
        'chat_id': habit.user.tg_chat_id,
    }
    requests.get(f'{settings.TG_URL}{settings.TG_TOKEN}/sendMessage', params=params)


def create_periodic_task(periodicity, habit_pk):
    every = 1
    period = IntervalSchedule.DAYS
    for_start_time = {'days': 1}

    if periodicity == 'hourly':
        period = IntervalSchedule.HOURS
        for_start_time = {'hours': 1}
    elif periodicity == 'weekly':
        every = 7
        for_start_time = {'days': 7}

    schedule = IntervalSchedule.objects.create(every=every, period=period)
    start_time = Habit.objects.filter(pk=habit_pk).first().created_at + timedelta(**for_start_time)

    PeriodicTask.objects.create(
        interval=schedule,
        name='Send telegram message',
        task='habits.tasks.send_tg_message',
        args=json.dumps([habit_pk]),
        start_time=start_time
    )
