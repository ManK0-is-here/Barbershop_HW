from .forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import *
from django.views.generic import CreateView


class CustomLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('landing')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('landing')


class RegisterView(CreateView):

    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        return super().form_valid(form)