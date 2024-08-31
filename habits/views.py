from rest_framework import viewsets, generics
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublicSerializer
from habits.services import NOW, create_periodic_task


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user, created_at=NOW)
        habit.save()

        if not habit.is_enjoyable and habit.user.tg_chat_id:
            create_periodic_task(habit.periodicity, habit.pk)

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        self.queryset = Habit.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitPublicSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        self.queryset = Habit.objects.exclude(user=self.request.user).filter(is_public=True)
        return super().get_queryset()
