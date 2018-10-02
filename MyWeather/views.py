from django.shortcuts import render
from django.http import HttpResponse

import collections
import googlemaps
import requests
import json
import reverse_geocoder as rg

from .models import MyWeatherDB #Importing the model of database that we made in model.py
# Create your views here.

def myWeather(request):
    return render(request,'MyWeather/MyWayWeather.html')

def userRequest(request):

    if request.method == "POST":
         origin_place = request.POST['origin_place']
         destination_place = request.POST['destination_place']
         #--------------------------REFERENCE---------------------------------------
         # https://djangobook.com/django-models/
         # https://djangobook.com/django-models-basic-data-access/

         weather_db_rec = MyWeatherDB.objects.filter(Origin = origin_place, Destination = destination_place)

         if len(weather_db_rec)> 0:
             weather_points = []
             for rec in weather_db_rec:
                 weather_point = {
                     'origin': rec.Origin,
                     'destination': rec.Destination,
                     'city_name': rec.City,
                     'latitude': float(rec.Latitude),
                     'longitude': float(rec.Longitude),
                     'temperature': rec.Temperature,
                     'humidity': rec.Humidity,
                     'pressure': rec.Pressure,
                     'description': rec.Description,
                     'icon': rec.Icon
                 }
                 weather_points.append(weather_point)

             context = {'weather_info': json.dumps(weather_points)}
             return render(request, 'MyWeather/userRequestResponse.html', context)
         else:
             #MAKING GOOGLE CLIENT
             #https://djangobook.com/django-models/
             #https://djangobook.com/django-models-basic-data-access/
             gmapclient = googlemaps.Client(key= 'AIzaSyAwx5bqxuLiHc4vyv04xkQp9YGGy1L4xVA')

             #USING GOOGLE CLIENT FOR CALLING DIRECTION API TO GET A LIST OF ROUTES FOR TRAVELLING
             dirs_result = gmapclient.directions(origin_place, destination_place,mode="driving")

             steps_in_leg = dirs_result[0]['legs'][0]['steps']

             weather_points = [] #THIS IS A  ARRAY WHERE EACH ELEM IS DICT CONTAINING INFO ABOUT STEPS

             for i, step_in_leg in enumerate(steps_in_leg):
                 if i % 4 == 1 or i % 4 == 2:
                     continue

                 lat = step_in_leg['end_location']['lat']
                 lon = step_in_leg['end_location']['lng']

                 coords = (lat,lon)
                 rev_geo_result = rg.search(coords)
                 city_nam = rev_geo_result[0]['name']

                 #------------CALLING WEATHER API NOW-------------

                 url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid={}' # use imperial units.
                 appid = 'a91a7423c7a5ee0462575bde493b958b'

                 weather_res_details = requests.get(url.format(lat,lon,appid)).json()

                 weather_point = {
                     #'city': city,
                     'city_name': city_nam,
                     'origin': origin_place,
                     'destination': destination_place,
                     'latitude': lat,
                     'longitude': lon,
                     'temperature': weather_res_details['main']['temp'],
                     'pressure': weather_res_details['main']['pressure'],
                     'humidity': weather_res_details['main']['humidity'],
                     'description': weather_res_details['weather'][0]['description'],
                     'icon': weather_res_details['weather'][0]['icon']
                 }

                 weather_points.append(weather_point) # putting weather points in weather_points list
             for weather_point in weather_points:
                 db_temp = MyWeatherDB(
                                     City = weather_point['city_name'],
                                     Origin= weather_point['origin'],
                                     Destination= weather_point['destination'],
                                     Latitude=weather_point['latitude'],
                                     Longitude=weather_point['longitude'],
                                     Temperature=weather_point['temperature'],
                                     Pressure=weather_point['pressure'],
                                     Humidity=weather_point['humidity'],
                                     Description=weather_point['description'],
                                     Icon=weather_point['icon']
                                     )
                 db_temp.save()
             context = {'weather_info': json.dumps(weather_points)}
             #return HttpResponse(weather_points)

             return render(request,'MyWeather/userRequestResponse.html',context)
    else:
         return render(request,'MyWeather/userRequest.html')
