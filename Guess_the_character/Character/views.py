from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from Character.forms import CustomAuthenticationForm


# Create your views here.

def show_index_page(request):
    return render(request, 'Character/index.html')


class LoginViewPage(LoginView):
    template_name = 'Character/login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('index')
