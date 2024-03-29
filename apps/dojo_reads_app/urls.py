from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^books/create$', views.create),
    url(r'^books/(?P<id>\d+)$', views.display),
    url(r'^delete$', views.delete),
    url(r'^users/(?P<id>\d+)$', views.user),
]