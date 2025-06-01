from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile_view, name='user_profile'),
    path('update/', views.update_user_profile, name='update_user_profile'),
    path('delete/', views.delete_user_profile, name='delete_user_profile'),
]