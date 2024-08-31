from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('retrieve/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('destroy/<int:pk>/', UserDestroyAPIView.as_view(), name='user_destroy'),
]
