from django.contrib import admin

# Register your models here.
from .models import Pesanan, DetailPesanan
@admin.register(Pesanan)
class PesananAdmin(admin.ModelAdmin):
    pass

@admin.register(DetailPesanan)
class DetailPesananAdmin(admin.ModelAdmin):
    pass