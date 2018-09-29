from django.shortcuts import render
from django.http import HttpResponse

import googlemaps
import requests
import json
# Create your views here.

def myWeather(request):
    return render(request,'MyWeather/MyWayWeather.html')

def userRequest(request):

    if request.method == "POST":
         origin_place = request.POST['origin_place']
         destination_place = request.POST['destination_place']

         #MAKING GOOGLE CLIENT

         gmapclient = googlemaps.Client(key= 'AIzaSyAwx5bqxuLiHc4vyv04xkQp9YGGy1L4xVA')

         #USING GOOGLE CLIENT FOR CALLING DIRECTION API TO GET A LIST OF ROUTES FOR TRAVELLING
         dirs_result = gmapclient.directions(origin_place, destination_place,mode="driving")

         steps_in_leg = dirs_result[0]['legs'][0]['steps']

         weather_points = [] #THIS IS A  ARRAY WHERE EACH ELEM IS DICT CONTAINING INFO ABOUT STEPS

         for i, step_in_leg in enumerate(steps_in_leg):
             if i % 4 == 1 or i % 4 == 2:
                 continue;

             lat = step_in_leg['end_location']['lat']
             lon = step_in_leg['end_location']['lng']

             #------------CALLING WEATHER API NOW-------------

             url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid={}' # use imperial units.
             appid = 'a91a7423c7a5ee0462575bde493b958b'

             weather_res_details = requests.get(url.format(lat,lon,appid)).json()

             weather_point = {
                 'latitude': lat,
                 'longitude': lon,
                 'temperature': weather_res_details['main']['temp'],
                 'pressure': weather_res_details['main']['pressure'],
                 'humidity': weather_res_details['main']['humidity'],
                 'description': weather_res_details['weather'][0]['description'],
                 'icon': weather_res_details['weather'][0]['icon']
             }

             weather_points.append(weather_point) # putting weather points in weather_points list

         context = {'weather_info': json.dumps(weather_points)}
         return HttpResponse(weather_points)

         return render(request,'MyWeather/userRequestResponse.html',context)
    else:
        return render(request,'MyWeather/userRequest.html')
