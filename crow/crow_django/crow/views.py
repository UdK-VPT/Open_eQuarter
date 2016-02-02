from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.shortcuts import render

from crow.models import Layer

# Create your views here.
def login_register(request):
    return render(request, 'crow/login_register.html')

# Create your views here.
@login_required
def home_page(request):
    return render(request, 'crow/index.html', {'layers': Layer.objects.all()})


class LayerDetail(DetailView):
    model = Layer
