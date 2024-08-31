from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitOrRewardValidator, TimeToCompleteValidator, IsEnjoyableHabitValidator, \
    EnjoyableHabitValidator
from users.serializers import UserDetailSerializer


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['pk', 'place', 'time', 'action', 'is_enjoyable', 'related_habit', 'periodicity', 'reward',
                  'time_to_complete', 'is_public', 'created_at', 'user']
        read_only_fields = ['pk', 'user', 'created_at']
        validators = [HabitOrRewardValidator(), TimeToCompleteValidator(),
                      IsEnjoyableHabitValidator(), EnjoyableHabitValidator()]


class HabitPublicSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Habit
        fields = ['pk', 'place', 'time', 'action', 'is_enjoyable', 'related_habit', 'periodicity', 'reward',
                  'time_to_complete', 'created_at', 'user']
