from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls import include
from config import views
from .views import custom_login_redirect # Import view kustom Anda


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', next_page='/redirect_after_login/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    path('redirect_after_login/', custom_login_redirect, name='custom_login_redirect'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin-django/', admin.site.urls),  # URL untuk admin site

    path('admin/', include([
        path('', views.admin_view, name='admin_view'),  # admin/ untuk admin_view
        path('menu/', include('menu.urls')),  # admin/menu/ untuk menu.urls
        path('pesanan/', include('pesanan.urls')),  # admin/pesanan/ untuk pesanan.urls
        path('userprofile/', include('userprofile.urls')),  # admin/userprofile/ untuk userprofile.urls
        path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    ])),
    
    # URL untuk user view
    path('', views.user_view, name='user_view'),

]
