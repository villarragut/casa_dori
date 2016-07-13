from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^imagenes/$', views.pics, name='pics'),
    url(r'^imagenes/([0-2]{1})/$', views.floors, name='floors'),
    url(r'^confirmacion/(?P<pk>\d+)/$', views.confirmation, name='confirmation'),
    url(r'^error/', views.rejection, name='rejection'),
    url(r'^mapa/', views.maps, name='maps'),
    url(r'^tarifas/', views.price, name='price'),
    url(r'^disponibilidad/', views.calendar, name='calendar'),
    url(r'^mantenimiento/$', views.housekeeping, name='housekeeping'),
]