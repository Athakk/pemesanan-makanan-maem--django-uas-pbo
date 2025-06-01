from django.urls import path    
from . import views
from django.conf import settings
from django.conf.urls.static import static
# menu/urls.py


urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('create/', views.create_menu, name='create_menu'),
    path('update/<int:menu_id>/', views.update_menu, name='update_menu'),
    path('delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)