from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitOrRewardValidator, TimeToCompleteValidator, IsEnjoyableHabitValidator, \
    EnjoyableHabitValidator, PeriodicityValidator
from users.serializers import UserDetailSerializer


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['pk', 'place', 'time', 'action', 'is_enjoyable', 'related_habit', 'periodicity_every', 'reward',
                  'time_to_complete', 'is_public', 'user']
        read_only_fields = ['pk', 'user']
        validators = [HabitOrRewardValidator(), TimeToCompleteValidator(),
                      IsEnjoyableHabitValidator(), EnjoyableHabitValidator(),
                      PeriodicityValidator()]


class HabitPublicSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Habit
        fields = ['pk', 'place', 'time', 'action', 'is_enjoyable', 'related_habit', 'periodicity_every', 'reward',
                  'time_to_complete', 'user']
