from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .forms import PesananForm, DetailPesananForm, DetailPesananFormSet
from .models import Pesanan, DetailPesanan
from django.contrib.auth.decorators import user_passes_test


def is_staff_required(user):
    return user.is_authenticated and user.is_staff


# Create your views here.
@user_passes_test(is_staff_required, login_url='/')
def pesanan_view(request):
    pesanans = Pesanan.objects.all().order_by('-tanggal_pesan').order_by('status')
    detail_pesanans = DetailPesanan.objects.all()
    return render(request, 'pesanan.html', {'pesanans': pesanans, 'detail_pesanans': detail_pesanans})

#Create
@user_passes_test(is_staff_required, login_url='/')
def create_pesanan(request):
    if request.method == 'POST':
        pesanan_form = PesananForm(request.POST)
        formset = DetailPesananFormSet(request.POST, request.FILES, prefix='detailpesanan')

        if pesanan_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    pesanan = pesanan_form.save(commit=False)
                    pesanan.user = request.user
                    pesanan.save()

                    formset.instance = pesanan
                    detail_pesanan_instances = formset.save(commit=False)

                    total_harga_pesanan = 0
                    for detail_pesanan in detail_pesanan_instances:
                        # Make sure the menu object is loaded to calculate subtotal correctly
                        detail_pesanan.menu = detail_pesanan.menu 
                        detail_pesanan.pesanan = pesanan # Ensure FK is set
                        detail_pesanan.save()
                        total_harga_pesanan += detail_pesanan.subtotal # Use the @property subtotal

                    # Handle deleted forms in the formset
                    for form in formset.deleted_forms:
                        if form.instance.id:
                            form.instance.delete()

                    pesanan.total_harga = total_harga_pesanan
                    pesanan.save()

                    return redirect('pesanan')
            except Exception as e:
                print(f"Error saat membuat pesanan: {e}")
    else:
        pesanan_form = PesananForm()
        formset = DetailPesananFormSet(prefix='detailpesanan')

    context = {
        'pesanan_form': pesanan_form,
        'formset': formset,
    }
    return render(request, 'pesanan_form.html', context)

def update_pesanan(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    if request.method == 'POST':
        pesanan_form = PesananForm(request.POST, instance=pesanan)
        formset = DetailPesananFormSet(request.POST, instance=pesanan, prefix='detailpesanan')

        if pesanan_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    pesanan = pesanan_form.save() # Simpan perubahan pada Pesanan

                    formset.instance = pesanan # Pastikan formset terkait dengan instance Pesanan ini
                    detail_pesanan_instances = formset.save(commit=False)
                    
                    total_harga_pesanan = 0
                    for detail_pesanan in detail_pesanan_instances:
                        detail_pesanan.pesanan = pesanan # Pastikan FK tetap benar
                        detail_pesanan.save()
                        total_harga_pesanan += detail_pesanan.subtotal
                    
                    for form in formset.deleted_forms:
                        if form.instance.pk:
                            form.instance.delete()

                    pesanan.total_harga = total_harga_pesanan
                    pesanan.save()

                    return redirect('pesanan')
            except Exception as e:
                print(f"Error saat mengedit pesanan: {e}")
    else:
        pesanan_form = PesananForm(instance=pesanan)
        formset = DetailPesananFormSet(instance=pesanan, prefix='detailpesanan')

    context = {
        'pesanan_form': pesanan_form,
        'formset': formset,
    }
    return render(request, 'pesanan/edit_pesanan.html', context) # Ganti dengan path template Anda


@user_passes_test(is_staff_required, login_url='/')
def delete_pesanan(request, id):
    pesanan = Pesanan.objects.get(id=id)
    if request.method == 'POST':
        pesanan.delete()
        return redirect('pesanan_list')
    return render(request, 'pesanan_confirm_delete.html', {'pesanan': pesanan})