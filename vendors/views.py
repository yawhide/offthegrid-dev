import sys
from datetime import timedelta, datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event, Vendor

from vendors.cron import get_facebook_events

highscore_cache = []

def index(request):
  return render(request, 'vendors/index.html', {})

def event_list(request):
  today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
  events = Event.objects.exclude(start_time__lt=today).order_by('-start_time') #happened_past_30_days()

  context = {
    'latest_events': events,
  }
  return render(request, 'vendors/event_list.html', context)

def event(request, event_id):
  event = get_object_or_404(Event, pk=event_id)
  vendors = event.vendors.all()
  context = {
    'event': event,
    'vendors': vendors,
  }
  return render(request, 'vendors/event_vendors.html', context)

def vendor(request, vendor_id):
  past_30_days = (datetime.utcnow() - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
  vendor = get_object_or_404(Vendor, pk=vendor_id)
  occurrences = vendor.event_set.filter(start_time__gte=past_30_days).count()
  context = {
    'vendor': vendor,
    'occurrences': occurrences,
  }
  return render(request, 'vendors/vendor.html', context)

def vendor_highscore(request):
  global highscore_cache
  if len(highscore_cache) == 0:
    print('highscore_cache is empty!')
    highscore_cache = getHighscore()
  context = {
    'vendors': highscore_cache,
  }
  return render(request, 'vendors/highscore.html', context)

def update_events(request):
  get_facebook_events()
  global highscore_cache
  highscore_cache = getHighscore()
  return render(request, 'vendors/update.html', {})

def getHighscore():
  past_30_days = (datetime.utcnow() - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
  vendors = [{
    'vendor': v,
    'occurrences': v.event_set.filter(start_time__gte=past_30_days).count(),
  } for v in Vendor.objects.all()]
  return sorted(vendors, key=lambda k: k['occurrences'], reverse=True)
