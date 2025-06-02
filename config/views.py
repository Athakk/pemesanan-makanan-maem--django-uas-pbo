import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.db.models import Sum # Mengimpor Sum langsung dari django.db.models
from pesanan.models import Pesanan, DetailPesanan

def is_staff_required(user):
    return user.is_authenticated and user.is_staff

def custom_login_redirect(request):
    if request.user.is_staff:
        return redirect(reverse('admin_view'))
    else:
        return redirect(reverse('user_view'))
    
@user_passes_test(is_staff_required, login_url='/')
def admin_view(request):
    today = datetime.date.today()
    
    # Filter untuk hari ini: Pastikan membandingkan rentang waktu
    # Dari awal hari ini sampai akhir hari ini
    penjualan_hari_ini = Pesanan.objects.filter(
        tanggal_pesan__date=today # Membandingkan hanya bagian tanggal dari DateTimeField
    ).count()
    
    total_pendapatan_hari_ini = Pesanan.objects.filter(
        tanggal_pesan__date=today
    ).aggregate(total=Sum('total_harga'))['total'] or 0

    # Filter untuk bulan ini di tahun ini
    penjualan_bulan_ini = Pesanan.objects.filter(
        tanggal_pesan__month=today.month,
        tanggal_pesan__year=today.year # Tambahkan filter tahun
    ).count()
    
    total_pendapatan_bulan_ini = Pesanan.objects.filter(
        tanggal_pesan__month=today.month,
        tanggal_pesan__year=today.year # Tambahkan filter tahun
    ).aggregate(total=Sum('total_harga'))['total'] or 0

    context = {
        'penjualan_hari_ini': penjualan_hari_ini,
        'penjualan_bulan_ini': penjualan_bulan_ini,
        'total_pendapatan_hari_ini': total_pendapatan_hari_ini,
        'total_pendapatan_bulan_ini': total_pendapatan_bulan_ini,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='/login/')
def user_view(request):
    return render(request, 'user/dashboard.html')