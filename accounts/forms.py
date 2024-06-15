# accounts/forms.py
from typing import Any
from django import forms
from .models import CustomUser


# ユーザー新規登録のフォーム
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード確認用', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('パスワードが一致しません')
        return cd['confirm_password']

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    new_password = forms.CharField(label='新パスワード', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='新パスワード再入力', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')
        
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
    
        if new_password and new_password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
        
        return cleaned_data
