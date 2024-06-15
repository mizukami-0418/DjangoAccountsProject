# accounts/views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

# ユーザー新規登録
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, '新規登録が完了しました')
            return redirect('detail')
        else:
            messages.error(request, '新規登録が出来ませんでした。再登録をお願いします')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            # userが存在する場合
            if user is not None:
                login(request, user)
                messages.success(request, 'ログインしました')
                return redirect('detail')
            else:
                messages.error(request, '入力に誤りがあります')
        else:
            messages.error(request, 'ログイン出来ませんでした。再度ログインしてください')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'ログアウトが完了しました')
    return redirect('home')

@login_required
def user_detail(request):
    return render(request, 'user_detail.html')

@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'ユーザー情報を更新しました')
            return redirect('detail')
        else:
            messages.error(request, '更新に失敗しました。再度更新してください')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'user_edit.html', {'form': form})