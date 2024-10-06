import flask
import requests


app = flask.Flask(__name__)


TREFLE_API_KEY = "loBhFQsqFf_9Buj7cLauIOQ_dLbLyuWmpXVKnNjl9jg"


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
