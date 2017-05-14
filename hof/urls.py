from django.conf.urls import url

from . import views

urlpatterns = [
    '''
    url(r'^top5/', views.top5, name='top5'),
    url(r'^$', views.index, name='index'),
    url(r'^top5b/', views.top5b, name='top5b'),
    url(r'^top5c/', views.top5c, name='top5c'),
    url(r'^top5i/', views.top5i, name='top5i'),
    url(r'^top5q/', views.top5q, name='top5q'),
    url(r'^top5co/', views.top5co, name='top5co'),
    url(r'^top10/', views.top10, name='top10'),
    url(r'^top10m/', views.top10m, name='top10m'),
    url(r'^top10e/', views.top10e, name='top10e'),
    '''
]