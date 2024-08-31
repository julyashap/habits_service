from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitOrRewardValidator, TimeToCompleteValidator, IsEnjoyableHabitValidator, \
    EnjoyableHabitValidator
from users.serializers import UserDetailSerializer


class HabitSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitOrRewardValidator(), TimeToCompleteValidator(),
                      IsEnjoyableHabitValidator(), EnjoyableHabitValidator()]
