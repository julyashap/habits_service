from rest_framework import viewsets, generics
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.services import NOW


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user, created_at=NOW)
        habit.save()

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsOwner]

    def list(self, request, *args, **kwargs):
        self.queryset = Habit.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        self.queryset = Habit.objects.exclude(user=self.request.user).filter(is_public=True)
        return super().get_queryset()
