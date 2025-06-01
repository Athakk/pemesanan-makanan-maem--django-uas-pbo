from django.urls import path    
from . import views


urlpatterns = [
    path('', views.pesanan_view, name='pesanan'),
    path('create/', views.create_pesanan, name='create_pesanan'),
    path('update/<int:pk>/', views.update_pesanan, name='update_pesanan'),
    path('delete/<int:pesanan_id>/', views.delete_pesanan, name='delete_pesanan'),
]