"""smic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/hof/uploaddata/$', 'hof.views.admin_update_data'), 
    url(r'^$', 'hof.views.index'),
    url(r'^top5/', 'hof.views.top5'),
    url(r'^top5b/', 'hof.views.top5b'),
    url(r'^top5c/', 'hof.views.top5c'),
    url(r'^top5i/', 'hof.views.top5i'),
    url(r'^top5q/', 'hof.views.top5q'),
    url(r'^top5co/', 'hof.views.top5co'),
    url(r'^top10/', 'hof.views.top10'),
    url(r'^top10m/', 'hof.views.top10m'),
    url(r'^top10e/', 'hof.views.top10e'),
    url(r'^rules/', 'hof.views.rules'),
    url(r'^news/', 'hof.views.news'),
    url(r'^news/(.+)/$', 'hof.views.news'),
    url(r'^polls/', 'hof.views.polls'),
    url(r'^me/', 'hof.views.me'),
    url(r'^vote/', 'hof.views.vote'),
    url(r'^login/', 'hof.views.login'),
    url(r'^article/(.+)/$', 'hof.views.article'),
    url(r'^admin/', include(admin.site.urls)),
]
