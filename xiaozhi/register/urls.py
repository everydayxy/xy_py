from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'^$', views.register_page, name = 'register_page'),
}