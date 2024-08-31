from celery import shared_task
from habits import services


@shared_task
def send_tg_message(habit_pk):
    services.send_tg_message(habit_pk)
