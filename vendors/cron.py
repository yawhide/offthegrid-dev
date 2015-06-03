import requests, numpy

from datetime import timedelta
from django.http import HttpRequest
from django.db import models
from vendors.models import Event, Vendor

def makeFBApiCall(pathname):
    access_token = '369389913268876|fe4a57f09a1cba6625149d765ee6369d'
    url = 'https://graph.facebook.com/v2.3/{0}'.format(pathname)
    payload = {'access_token': access_token}
    r = requests.get(url, params=payload)
    if r.status_code == requests.codes.ok:
        return r.json()
    return None

def get_facebook_events():
    response = makeFBApiCall('OffTheGridSF/events')
    for event in response['data']:
        saveEventIntoDB(event['id'])


def saveEventIntoDB(event_id):
    response = makeFBApiCall(event_id)
    start_time = numpy.datetime64(response['start_time']).tolist()
    if response.get('end_time'):
        end_time = numpy.datetime64(response['end_time']).tolist()
    else:
        end_time = start_time + timedelta(hours=4)
    location = response.get('location') or ''
    name = response.get('name')
    facebook_id = response.get('id')
    try:
        e = Event.objects.get(facebook_id=facebook_id)
    except Event.DoesNotExist:
        #print("Event with facebook_id {0} does not exist".format(facebook_id))
        e = None
    #print(e)
    if e:
        e.start_time = start_time
        e.end_time = end_time
        e.location = location
        e.name = name
        e.facebook_id = facebook_id
    else:
        e = Event(start_time=start_time, end_time=end_time, location=location, name=name, facebook_id=facebook_id)
    e.save()

    description = response.get('description')
    if description:
        vendors = Vendor.objects.all()
        for vendor in vendors:
            if vendor.name in description:
                try:
                    if e.vendors.get(id=vendor.id):
                        break;
                        #print('vendor {0} already exists'.format(vendor.name))
                except:
                    e.vendors.add(vendor)
                    #print('added vendor:{0} to e:{1}'.format(vendor, e))
