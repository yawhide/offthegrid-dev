import sys
from datetime import timedelta, datetime
from pytz import timezone

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event, Vendor

from vendors.cron import get_facebook_events

highscore_cache = []
san_fran_tz = timezone('America/Los_Angeles')
san_fran_time = datetime.now(san_fran_tz)

def index(request):
  return render(request, 'vendors/index.html', {})

def event_list(request):
  context = {
    'latest_events': get_event_list(),
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
  vendor = get_object_or_404(Vendor, pk=vendor_id)
  occurrences = past_30_days_filter(vendor).count()
  context = {
    'vendor': vendor,
    'occurrences': occurrences,
  }
  return render(request, 'vendors/vendor.html', context)

def vendor_highscore(request):
  global highscore_cache
  if len(highscore_cache) == 0:
    update_highscore_cache()
  context = {
    'vendors': highscore_cache,
  }
  return render(request, 'vendors/highscore.html', context)

def update_events(request):
  get_facebook_events()
  update_highscore_cache()
  return render(request, 'vendors/update.html', {})



def update_highscore_cache():
  global highscore_cache
  vendors = [{
    'vendor': v,
    'occurrences': past_30_days_filter(v).count(),
  } for v in Vendor.objects.all()]
  highscore_cache = sorted(vendors, key=lambda k: k['occurrences'], reverse=True)

def get_event_list():
  global san_fran_time
  beginning_san_fran_day = convert_time_to_midnight(san_fran_time)
  return Event.objects.exclude(start_time__lt=beginning_san_fran_day).order_by('start_time')

def convert_time_to_midnight(time):
  return time.replace(hour=0, minute=0, second=0, microsecond=0)

def past_30_days_filter(model):
  global san_fran_time
  beginning_san_fran_day = convert_time_to_midnight(san_fran_time)
  one_month_ago = convert_time_to_midnight(san_fran_time - timedelta(days=30))
  return model.event_set.filter(start_time__gte=one_month_ago, start_time__lt=beginning_san_fran_day)
