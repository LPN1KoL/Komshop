from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Product
        fields = [
            "name", "price", "product_code", "age_start", "age_end", "height",
            "width", "length", "weight", "concrete", "installation_time", "params",
            "photo"
        ]


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Tag
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Category
        fields = ["name"]


class LoginForm(forms.Form):
    login = forms.CharField(max_length=255, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegForm(forms.Form):
    login = forms.CharField(max_length=255, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')
    email = forms.EmailField(label='email')
