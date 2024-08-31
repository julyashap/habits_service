from django.urls import path
from rest_framework import routers
from habits.apps import HabitsConfig
from habits.views import HabitViewSet, HabitPublicListAPIView, GetTGBotLink

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register('', HabitViewSet, basename='habits')

urlpatterns = [
    path('public-list/', HabitPublicListAPIView.as_view(), name='habit_public_list'),

    path('tg-bot-link/', GetTGBotLink.as_view(), name='tg_bot_link'),
] + router.urls
