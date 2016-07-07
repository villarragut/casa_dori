from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^imagenes/$', views.pics, name='pics'),
    url(r'^confirmacion/(?P<pk>\d+)/$', views.confirmation, name='confirmation'),
    url(r'^error/', views.rejection, name='rejection'),
    url(r'^mantenimiento/$', views.housekeeping, name='housekeeping'),
]