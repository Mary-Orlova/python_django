"""
Форма для продуктов с подключением картинок с многовариантным выбором.
"""


from django import forms
from django.utils.translation import gettext_lazy as _
from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
    )

