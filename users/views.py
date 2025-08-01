from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Profile
from .forms import ( 
    UserRegisterForm, 
    UserLoginForm, 
    CustomPasswordResetForm, 
    CustomSetPasswordForm,
    UserPasswordChangeForm,
    UserProfileUpdateForm,
)
from django.views.generic import (
    CreateView,  
    DetailView, 
    UpdateView,
)
from django.contrib.auth.views import (
    PasswordChangeView,  
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView,
)



class UserLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('landing')


class UserLogoutView(LogoutView):

    template_name = 'users/logout.html'
    next_page = reverse_lazy('logout')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы вышли, надеюсь вас не собьёт автобус")
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):

    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):

        response = super().form_valid(form)
        user = self.object
        login(self.request, user)

        return response
    
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(self.success_url)
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):

        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрировались! Добро пожаловать в клуб приятель!")
        
        return response
    

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('profile_detail')


class CustomPasswordResetView(PasswordResetView):

    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.profile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    success_url = reverse_lazy('profile_detail')
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)
    

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)