from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^events/$', views.event_list, name='event_list'),
  url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
  url(r'^vendor/(?P<vendor_id>[0-9]+)/$', views.vendor, name='vendor'),
  url(r'^highscore/$', views.vendor_highscore, name='vendor_highscore'),
  url(r'^update/$', views.update_events, name='update_events'),
]
