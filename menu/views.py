import os
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MenuForm
from .models import Menu
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def is_staff_required(user):
    return user.is_authenticated and user.is_staff

# Create your views here.
@user_passes_test(is_staff_required, login_url='/')
def menu_view(request):
    menus = Menu.objects.all()
    return render(request, 'menu.html', {'menus': menus})

#Create
@user_passes_test(is_staff_required, login_url='/')
def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuForm()
    return render(request, 'menu_form.html', {'form': form})

#Update
@user_passes_test(is_staff_required, login_url='/')
def update_menu(request, menu_id):
    menu = Menu.objects.get(id  = menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            if 'image' in request.FILES:
                # If a new image is uploaded, delete the old one
                if menu.image and os.path.isfile(menu.image.path):
                    os.remove(menu.image.path)
            else:
                # If no new image is uploaded, keep the old one
                form.instance.image = menu.image
            form.save()
            return redirect('menu')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu_form.html', {'form': form})

#Delete
@user_passes_test(is_staff_required, login_url='/')
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id = menu_id)

    if request.method == 'POST':
        if menu.image:
            if os.path.isfile(menu.image.path):
                os.remove(menu.image.path)

        menu.delete()
        messages.success(request, f'Item "{menu.nama}" berhasil dihapus.')

        return redirect('menu')
    return render(request, 'menu_confirm_delete.html', {'menu': menu})
