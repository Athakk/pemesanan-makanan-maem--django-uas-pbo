from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def is_staff_required(user):
    return user.is_authenticated and user.is_staff

def custom_login_redirect(request):
    if request.user.is_staff:
        return redirect(reverse('admin_view'))
    else:
        return redirect(reverse('user_view'))
    
@user_passes_test(is_staff_required, login_url='/')
def admin_view(request):
    return render(request, 'admin/dashboard.html')

@login_required(login_url='/login/')
def user_view(request):
    return render(request, 'user/dashboard.html')
