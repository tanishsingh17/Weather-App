from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"

API_KEY = "8eb15a1ae15a5a52ff66bfa0b6fed138"

with open("cities.json", "r") as f:
    cities_data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        country = request.form["country"]
        city = request.form["city"]

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
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
                session["weather_data"] = {"error": "City not found"}

        except:
            session["weather_data"] = {"error": "Internet or API error"}

        return redirect(url_for("index"))

    weather_data = session.pop("weather_data", None)

    return render_template("index.html", weather=weather_data, cities_data=cities_data)


if __name__ == "__main__":
    app.run(debug=True)
