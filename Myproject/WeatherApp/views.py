import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3b9127cebd2dcc5262ce0c36a7546b5d'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in this world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "City added succesfully!"
            message_class = "is-success"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r["main"]["temp"],
            'description': r["weather"][0]["description"],
            'icon': r["weather"][0]["icon"],
            'humidity': r["main"]["humidity"],
            'pressure': r["main"]["pressure"],
            'clouds': r["clouds"]["all"],
            'wind': r["wind"]["speed"],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')


def index1(request):
    url = 'https://lab4-443e5-default-rtdb.firebaseio.com/test.json'

    city_weather = requests.get(url).json()
    weather = {
        'temperature': city_weather['temp'],
        'humidity': city_weather['humidity'],
    }
    context = {'weather': weather}
    print('weather', weather['temperature'])

    return render(request, 'weather/weather1.html', context)
