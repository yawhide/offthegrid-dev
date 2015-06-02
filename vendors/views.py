import sys
from datetime import timedelta, datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event, Vendor

from vendors.cron import get_facebook_events

# Create your views here.
def index(request):
  today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
  events = Event.objects.exclude(start_time__lt=today).order_by('-start_time') #happened_past_30_days()

  context = {
    'latest_events': events,
  }
  return render(request, 'vendors/index.html', context)

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
  get_facebook_events()
  past_30_days = (datetime.utcnow() - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
  vendors = [{
    'vendor': v,
    'occurrences': v.event_set.filter(start_time__gte=past_30_days).count(),
  } for v in Vendor.objects.all()]
  context = {
    'vendors': sorted(vendors, key=lambda k: k['occurrences'], reverse=True),
  }

  return render(request, 'vendors/highscore.html', context)
