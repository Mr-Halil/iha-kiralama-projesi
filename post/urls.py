from django.conf.urls import url
from .views import *

app_name = 'post'

urlpatterns = [
    url(r'^index/$', post_index, name='index'),
    url(r'^create/$', post_create, name='create'),
    
    
    url(r'^(?P<slug>[\w-]+)/kirala/$', post_kirala, name='kirala'),
    url(r'^(?P<slug>[\w-]+)/kirala/sil$', post_kirala_delete, name='kirala_delete'),

    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
]