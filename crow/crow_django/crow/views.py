from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import OeQLayer

# Create your views here.
def login_register(request):
    return render(request, 'crow/login_register.html')

# Create your views here.
@login_required
def home_page(request):
    layer_list = {}
    feature_list = OeQLayer.objects.all()
    layer_list['Heinrichstr'] = feature_list
    return render(request, 'crow/index.html', {'layer_list': layer_list})


