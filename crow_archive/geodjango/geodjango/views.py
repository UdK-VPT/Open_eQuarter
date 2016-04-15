from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.template.context_processors import csrf
from registration.forms import RegistrationForm

# Create your views here.
def home_page(request):
    context = {}
    context.update(csrf(request))
    context.update({'reg_form': RegistrationForm()})
    context.update({'login_form': AuthenticationForm()})


    return render(request, 'geodjango/index.html', context)