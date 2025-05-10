# accounts/urls.py
from django.urls import path
from .views import ( RegisterAPI, ProfileAPI, LoginAPI, LogoutAPI, UserListAPI, UserRetrieveAPI
            , ProfileUpdateAPI, ChangePasswordAPI, DeleteUserAPI)

app_name = 'accounts'

urlpatterns = [
    path('users/', UserListAPI.as_view(), name='user_list'),
    path('users/<int:id>/', UserRetrieveAPI.as_view(), name='user_retrieve'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateAPI.as_view(), name='profile_update'),
    path('password/change/', ChangePasswordAPI.as_view(), name='change_password'),
    path('delete-user/<int:user_id>/', DeleteUserAPI.as_view(), name='delete_user'),
]
