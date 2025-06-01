import os
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def is_staff_required(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_required, login_url='/')
def user_profile_view(request):
    user = User.objects.all()
    return render(request, 'user_profile.html', {'user': user})

@user_passes_test(is_staff_required, login_url='/')
def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    return render(request, 'user_profile_form.html', {'form': form})

@user_passes_test(is_staff_required, login_url='/')
def update_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'user_profile_form.html', {'form': form})

@user_passes_test(is_staff_required, login_url='/')
def delete_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User "{user.username}" has been deleted.')
        return redirect('user_profile')

    return render(request, 'user_profile_confirm_delete.html', {'user': user})




