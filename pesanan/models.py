from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pesanan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesanan') 
    nama_pemesan = models.CharField(max_length=100)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.IntegerField(choices=[
        (1, 'Menunggu Pembayaran'),
        (2, 'Diproses'),
        (3, 'Selesai'),
        (4, 'Dibatalkan'),
    ], default=1)
    tanggal_pesan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pesanan #{self.id} - {self.tanggal_pesan.strftime('%Y-%m-%d %H:%M')}"

class DetailPesanan(models.Model):
    id = models.AutoField(primary_key=True)
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE)
    menu = models.ForeignKey('menu.Menu', on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    harga_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.harga_item:
            self.harga_item = self.menu.harga
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.jumlah * self.harga_item

    def __str__(self):
        return f"{self.jumlah} x {self.menu.nama} untuk Pesanan #{self.pesanan.id}"
