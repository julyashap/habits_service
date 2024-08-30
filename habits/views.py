from rest_framework import viewsets, generics
from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsOwner]

    def list(self, request, *args, **kwargs):
        self.queryset = Habit.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def get_queryset(self):
        self.queryset = Habit.objects.exclude(user=self.request.user).filter(is_public=True)
        return super().get_queryset()
