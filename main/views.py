import requests, math
from django.conf import settings
from django.shortcuts import render

def kelvin_to_celsius(k):  # helper
    return math.trunc(k - 273.15)

def index(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={settings.OWM_KEY}&lang=pt_br"
            )
            resp = requests.get(url, timeout=5).json()

            if resp.get("cod") == 200:
                context = {
                    "city": resp["name"],
                    "country": resp["sys"]["country"],
                    "icon": resp["weather"][0]["icon"],
                    "description": resp["weather"][0]["description"].title(),
                    "temp": kelvin_to_celsius(resp["main"]["temp"]),
                    "feels": kelvin_to_celsius(resp["main"]["feels_like"]),
                    "humidity": resp["main"]["humidity"],
                    "pressure": resp["main"]["pressure"],
                }
            else:
                context["error"] = (
                    f"Cidade não encontrada ({resp.get('message', '')})."
                )
    return render(request, "main/index.html", context)


# Create your views here.
