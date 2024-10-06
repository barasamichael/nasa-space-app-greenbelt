import csv
import flask
import requests
from flask_caching import Cache

app = flask.Flask(__name__)

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
cache = Cache(app)

TREFLE_API_KEY = "loBhFQsqFf_9Buj7cLauIOQ_dLbLyuWmpXVKnNjl9jg"


def read_csv(file_path, value_column_name):
    data = {}
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year = row["Year"]
            month_value = float(row[value_column_name])
            if year not in data:
                data[year] = []
            data[year].append(month_value)
    return data


@cache.cached(timeout=1500)
@app.route("/climate_data", methods=["GET"])
def get_climate_data():
    # Paths to your CSV files
    rainfall_file = "static/data/rainfall.csv"
    temperature_file = "static/data/temperature.csv"

    # Read data from both CSV files
    rainfall_data = read_csv(rainfall_file, "Rainfall - (MM)")
    temperature_data = read_csv(temperature_file, "Temperature - (Celsius)")

    # Combine the data into the desired format
    combined_data = {}
    for year in rainfall_data.keys():
        combined_data[year] = {
            "temperature": temperature_data.get(year, []),
            "rainfall": rainfall_data.get(year, []),
        }

    return flask.jsonify(combined_data)


@app.route("/api/plants", methods=["GET"])
def get_plants():
    climate_zone = "tropical"
    latitude = "-1.286389"
    longitude = "36.817223"

    trefle_url = (
        "https://trefle.io/api/v1/plants?filter[climate_zone]="
        + f"{climate_zone}&filter[latitude]={latitude}&filter[longitude]="
        + f"{longitude}&token={TREFLE_API_KEY}"
    )

    try:
        response = requests.get(trefle_url)
        response.raise_for_status()
        data = response.json()
        return flask.jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return (
            flask.jsonify(
                {
                    "error": "Failed to fetch data from Trefle API",
                    "details": str(e),
                }
            ),
            500,
        )


@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/climate")
def climate():
    return flask.render_template("climate.html")


if __name__ == "__main__":
    app.run(debug=True)
