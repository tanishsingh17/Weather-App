from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "fallbacksecret")
API_KEY = os.getenv("API_KEY")

with open("cities.json", "r") as f:
    cities_data = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        country = request.form.get("country")
        city = request.form.get("city")

        if not country or not city:
            session["weather_data"] = {
                "error": "Please select both country and city"
            }

            return redirect(url_for("index"))

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"

        try:

            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code == 200:

                session["weather_data"] = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"]
                }

            else:

                session["weather_data"] = {
                    "error": "City not found"
                }

        except Exception as e:

            session["weather_data"] = {
                "error": "Internet or API error"
            }

        return redirect(url_for("index"))

    weather_data = session.pop("weather_data", None)

    return render_template(
        "index.html",
        weather=weather_data,
        cities_data=cities_data
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
