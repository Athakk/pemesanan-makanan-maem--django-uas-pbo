from importlib.metadata import requires
from django import forms
from .models import Pesanan
from .models import DetailPesanan
from menu.models import Menu 
from django.forms import inlineformset_factory

from django.contrib.auth.models import User

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama_pemesan', 'total_harga', 'status']
        widgets = {
            'nama_pemesan': forms.TextInput(attrs={'placeholder' : 'Nama Pemesan', 'class': 'form-control my-2'}),
            'total_harga': forms.NumberInput(attrs={'placeholder' : 'Harga', 'class': 'form-control my-2'}),
            'status': forms.Select(attrs={'placeholder' : 'Stok', 'class': 'form-control my-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama_pemesan'].required = True

class DetailPesananForm(forms.ModelForm):
    class Meta:
        model = DetailPesanan
        fields = ['menu', 'jumlah']
        widgets = {
            'menu': forms.Select(attrs={'class': 'form-control my-2'}),
            'jumlah': forms.NumberInput(attrs={'placeholder' : 'Jumlah', 'class': 'form-control my-2', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu'].queryset = Menu.objects.filter(stok__gt=0)  

DetailPesananFormSet = inlineformset_factory(
    Pesanan,            
    DetailPesanan,     
    form=DetailPesananForm, 
    fields=['menu', 'jumlah'],
    extra=1,            
    can_delete=True     
)
