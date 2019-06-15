from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, authenticate

from user.forms import MyUserCreationForm, AccountForm
from user.models import User


class Register(View):
    def get(self, request):
        form = MyUserCreationForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('project:create')
        return render(request, 'user/register.html', {'form': form})


class Account(LoginRequiredMixin, View):
    def get(self, request):
        form = AccountForm(instance=request.user)
        return render(request, 'user/account.html', {'form': form, 'user_pk': request.user.pk})

    def post(self, request):
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'user/account.html', {'form': form, 'user_pk': request.user.pk})


class ViewProfile(View):
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        return render(request, 'user/profile.html', {'user': user})
