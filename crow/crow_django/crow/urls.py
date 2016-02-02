from django.conf.urls import url
from crow import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^layer_(?P<pk>\d+)/$', views.LayerDetail.as_view(), name='layer_detail'),
]
