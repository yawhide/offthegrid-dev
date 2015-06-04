import pytz, mock, numpy
from datetime import datetime, timedelta

from django.test import TestCase, RequestFactory

from .models import Vendor, Event
from views import update_highscore_cache, get_event_list, convert_time_to_midnight, past_30_days_filter, san_fran_time, highscore_cache
from cron import saveEventIntoDB

def create_vendor(vehicle, name, url, food, img):
  return Vendor.objects.create(vehicle=vehicle, name=name, url=url, food=food, img=img)

def create_event(start_time, end_time, location, name, facebook_id):
  return Event.objects.create(start_time=start_time, end_time=end_time, location=location, name=name, facebook_id=facebook_id)

def create_vendor_from_array(arr):
  for i in arr:
    create_vendor('', i, '', '', '')

class ViewTests(TestCase):
  def setUp(self):
    self.factory = RequestFactory()

  """
    event_list should only show events that start after the current day at 12:00am san fran's time
  """
  def test_event_list(self):
    expired_event_time = convert_time_to_midnight(san_fran_time)-timedelta(seconds=1)
    assert len(get_event_list()) == 0
    e1 = create_event(san_fran_time, san_fran_time+timedelta(hours=3), '', 'Event1', '')
    e2 = create_event(expired_event_time, expired_event_time+timedelta(hours=3), '', 'Event2', '')
    e3 = create_event(datetime.utcnow(), datetime.utcnow()+timedelta(hours=3), '', 'Event2', '')
    e4 = create_event(datetime.utcnow()+timedelta(days=15), datetime.utcnow()+timedelta(days=15, hours=3), '', 'Event2', '')
    e5 = create_event(datetime.utcnow()-timedelta(days=15), datetime.utcnow()-timedelta(days=14, hours=21), '', 'Event2', '')

    assert len(get_event_list()) == 3

  """
    past_30_days_filter should only return the instances of a model's foreign keys whose start_time is within the past 30 days from 12:00am san fran's time
  """
  def test_past_30_day_filter(self):
    expired_event_time = convert_time_to_midnight(san_fran_time)-timedelta(seconds=1)
    e1 = create_event(san_fran_time, san_fran_time+timedelta(hours=3), '', 'Event1', '')
    e2 = create_event(expired_event_time, expired_event_time+timedelta(hours=3), '', 'Event2', '')
    e3 = create_event(datetime.utcnow(), datetime.utcnow()+timedelta(hours=3), '', 'Event3', '')
    e4 = create_event(datetime.utcnow()+timedelta(days=15), datetime.utcnow()+timedelta(days=15, hours=3), '', 'Event4', '')
    e5 = create_event(datetime.utcnow()-timedelta(days=15), datetime.utcnow()-timedelta(days=14, hours=21), '', 'Event5', '')
    e6 = create_event(datetime.utcnow()-timedelta(days=2), datetime.utcnow()-timedelta(days=1, hours=21), '', 'Event5', '')
    e7 = create_event(datetime.utcnow()+timedelta(days=1), datetime.utcnow()+timedelta(days=1, hours=10), '', 'Event5', '')

    v1 = create_vendor('truck', 'vendor1', '', '', '')
    v2 = create_vendor('cart', 'vendor2', '', '', '')
    v3 = create_vendor('tent', 'vendor3', '', '', '')
    v4 = create_vendor('truck', 'vendor4', '', '', '')
    v5 = create_vendor('truck', 'vendor5', '', '', '')

    e1.vendors.add(v1, v2, v5)
    e2.vendors.add(v2, v4)
    e3.vendors.add(v1)
    e4.vendors.add(v3, v4, v5)
    e5.vendors.add(v1, v3)
    e6.vendors.add(v1, v2, v3, v4)
    e7.vendors.add(v1, v2, v3, v4, v5)

    v1_filtered = past_30_days_filter(v1)
    v2_filtered = past_30_days_filter(v2)
    v3_filtered = past_30_days_filter(v3)
    v4_filtered = past_30_days_filter(v4)
    v5_filtered = past_30_days_filter(v5)

    assert(len(v1_filtered) == 2)
    assert(len(v2_filtered) == 2)
    assert(len(v3_filtered) == 2)
    assert(len(v4_filtered) == 2)
    assert(len(v5_filtered) == 0)

  """
    the highscore_cache should keep a list of all the vendors and the number of of events they have attended in the past 30 days
  """
  def test_highscore_cache(self):
    assert len(highscore_cache) == 0
    test_vendors = ['Little Green Cyclo', 'We Sushi', 'Cheese Gone Wild', 'Bacon Bacon', 'Naked Chorizo', 'Garden Creamery', 'Hill County BBQ', 'Lobsta Truck', 'Crepe \'Em Coming', 'Curry Up Now', 'The Taco Guys']
    create_vendor_from_array(test_vendors)
    request = {
      "description": "Live music every Monday night! This market is located in the Caltrain parking lot at El Camino Real and O'Neill St.\n\nLocation: Caltrain Parking Lot (El Camino Real Ave and Oneill Ave)\nTime: 5:00pm - 9:00pm\nPublic Transportation: Caltrain Belmont Station\n\nVendors:\nLittle Green Cyclo\nWe Sushi\nCheese Gone Wild\nBacon Bacon\nNaked Chorizo\nGarden Creamery\nHill County BBQ\nLobsta Truck\nCrepe 'Em Coming\n\n\n(Lineup subject to change)\nCATERING NEEDS? Have OtG cater your next event! Get started by visiting offthegridsf.com/catering.\nDownload Off the Grid App for amenities around this market! http://offthegridsf.com/app",
      "end_time": "2015-06-15T21:00:00-0700",
      "name": "Off the Grid: Belmont (Monday Dinner)",
      "start_time": "2015-06-15T17:00:00-0700",
      "id": "1017287688306078"
    }
    request2 = {
      "description": "lalalalalala. i like food\nLobsta Truck \n   Curry Up Now\n    \n\n  The Taco Guys\n please come by and eat ok?",
      "name": "Off the Grid: My place joe",
      "start_time": "2015-06-15T17:00:00-0700",
      "id": "10172876234234306078"
    }
    saveEventIntoDB(request)
    saveEventIntoDB(request2)

    tz_aware_date_e = pytz.utc.localize(numpy.datetime64(request['start_time']).tolist())
    tz_aware_date_e2 = pytz.utc.localize(numpy.datetime64(request2['start_time']).tolist())
    e = Event(start_time=tz_aware_date_e, end_time=request['end_time'], location='', name=request['name'], facebook_id=request['id'])
    e2 = Event(start_time=tz_aware_date_e2, end_time=tz_aware_date_e2+timedelta(hours=3), location='', name=request2['name'], facebook_id=request2['id'])
    vendors = Vendor.objects.all()

    #e.vendors.add(Vendor.objects.get(name='Lobsta Truck'), Vendor.objects.get(name='Curry Up Now'), Vendor.objects.get(name='The Taco Guys'))

    test_e = Event.objects.get(facebook_id=request['id'])
    test_e2 = Event.objects.get(facebook_id=request2['id'])

    assert test_e.start_time == e.start_time
    assert test_e2.start_time == e2.start_time

    assert test_e.name == e.name
    assert test_e2.name == e2.name

    assert test_e.facebook_id == e.facebook_id
    assert test_e2.facebook_id == e2.facebook_id

    for v in test_e.vendors.all():
      assert Vendor.objects.get(name=v.name) == v
    for v in test_e2.vendors.all():
      assert Vendor.objects.get(name=v.name) == v

