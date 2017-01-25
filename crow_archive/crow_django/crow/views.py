from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.shortcuts import render

from crow.models import Layer
from crow.forms import CommentForm

# Create your views here.
def login_register(request):
    return render(request, 'crow/login_register.html')

# Create your views here.
@login_required
def home_page(request):
    return render(request, 'crow/index.html', {'layers': Layer.objects.all()})


# Define the view which will be used to comment a layer
class LayerDetail(CreateView):
    model = Layer
    template_name = 'crow/layer_detail.html'
    form_class = CommentForm

    # Define additional meta data, which is needed to create a new Comment-Object
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        kwargs['layer'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    # Define the context which will be used when rendering the template
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['layer'] = self.get_object()
        return data
