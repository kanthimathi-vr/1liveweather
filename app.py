from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_KEY = "27bcd20e66321d03615c489ac5cdb54d"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Default cities
CITIES = ["New York,US", "London,UK", "Tokyo,JP", "Delhi,IN", "Chennai,IN"]

@app.route("/")
def index():
    return render_template("index.html", cities=CITIES, page_title="Live Weather", default_city="Chennai,IN")

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city", "Chennai,IN")
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Unknown error")}), 400
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "status": data["weather"][0]["description"].title()
        }
        return jsonify(weather)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
