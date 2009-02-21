from django.conf.urls.defaults import *

from microblog import views

urlpatterns = patterns('',
    (r'^users/(?P<username>.*)/friends/$', views.friends),
    (r'^users/(?P<username>.*)/(?P<id>\d+)/$', views.showentry),
    (r'^users/(?P<username>.*)/$', views.profile),
    (r'^post/$', views.postentry),
    (r'^$', views.index),
)

