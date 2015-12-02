from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.template.context_processors import csrf
from registration.forms import RegistrationForm

# Create your views here.
def login_register(request):
    return render(request, 'crow/login_register.html')

# Create your views here.
#@login_required
def home_page(request):
    return render(request, 'crow/index.html')