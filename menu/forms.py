from django import forms
from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'nama': forms.TextInput(attrs={'placeholder' : 'Nama Makanan/Minuman','class': 'form-control my-2'}),
            'harga': forms.NumberInput(attrs={'placeholder' : 'Harga', 'class': 'form-control my-2'}),
            'stok': forms.NumberInput(attrs={'placeholder' : 'Stok', 'class': 'form-control my-2'}),
            'jenis': forms.Select(attrs={'class': 'form-control my-2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control my-2'}),
        }



