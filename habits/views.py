from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from config import settings
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublicSerializer
from habits.services import create_periodic_task


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        habit.save()

        if not habit.is_enjoyable and habit.user.tg_chat_id:
            create_periodic_task(habit.periodicity_every, habit.time, habit.pk)

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


class GetTGBotLink(views.APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response("TG Bot link")
        }
    )
    def get(self, *args, **kwargs):
        return Response({'tg_bot_link': settings.TG_BOT_LINK}, status=status.HTTP_200_OK)
