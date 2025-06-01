from django.db import models


# Create your models here.
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField()
    jenis = models.IntegerField(choices=[
        (1, 'Makanan'),
        (2, 'Minuman'),
    ], default=1)
    image = models.ImageField(upload_to='menus/')

    def __str__(self):
        return self.nama


