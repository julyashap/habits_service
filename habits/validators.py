from datetime import timedelta
from rest_framework.exceptions import ValidationError


class HabitOrRewardValidator:
    def __call__(self, value):
        is_current_habit_enjoyable = dict(value).get('is_enjoyable')
        related_habit = dict(value).get('related_habit')
        reward = dict(value).get('reward')

        if not is_current_habit_enjoyable and related_habit and reward:
            raise ValidationError('У полезной привычки нельзя указывать связанную '
                                  'привычку и вознаграждение одновременно!')
        elif not is_current_habit_enjoyable and not related_habit and not reward:
            raise ValidationError('У полезной привычки обязательно должна быть либо связанная '
                                  'привычка, либо вознаграждение!')


class TimeToCompleteValidator:
    def __call__(self, value):
        time_to_complete = dict(value).get('time_to_complete')

        if time_to_complete > timedelta(minutes=2):
            raise ValidationError('Время выполнения не должно быть больше 2-х минут!')


class IsEnjoyableHabitValidator:
    def __call__(self, value):
        is_current_habit_enjoyable = dict(value).get('is_enjoyable')
        related_habit = dict(value).get('related_habit')

        if not is_current_habit_enjoyable and related_habit and not related_habit.get('is_enjoyable'):
            raise ValidationError('У полезной привычки в связанных привычках может быть только приятная привычка!')


class EnjoyableHabitValidator:
    def __call__(self, value):
        is_current_habit_enjoyable = dict(value).get('is_enjoyable')
        related_habit = dict(value).get('related_habit')
        reward = dict(value).get('reward')

        if is_current_habit_enjoyable and related_habit or reward:
            raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения!')
