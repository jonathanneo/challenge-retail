from flask import Flask, session, request, redirect, render_template, Blueprint, jsonify
import pandas as pd
import os
import json
from fbprophet import Prophet
import pickle
import datetime as dt
import markdown as md
from flask_restx import Api, Resource, fields

# create flask app
app = Flask(__name__,static_url_path='/static')

# create api blueprint 
blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, doc="/doc/")
app.register_blueprint(blueprint)

# read in dataset
df = pd.read_csv("retail.csv")

metricMapper = {
    "revenue": "Revenue",
    "cost": "Product cost",
    "profit": "Gross profit"
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/forecast")
def forecasted():
    return render_template("forecasted.html")

@app.route("/report")
def report():
    filename = "report.md"
    readme_file = open(f"articles/{filename}", "r")
    md_template_string = md.markdown(readme_file.read())
    return render_template("report.html", markdown=md_template_string)

@app.route("/changelog")
def changelog():
    filename = ""
    readme_file = open(f"changelog/{filename}", "r")
    md_template_string = md.markdown(readme_file.read())
    # print(md_template_string)


@api.route("/timeseries/<metric>/<years>")
class TimeSeries(Resource):
    def get(self, metric, years):
        return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Year"]).sum()[metricMapper[metric]].to_dict()


@api.route("/country/<metric>/<years>")
class Country(Resource):
    def get(self, metric, years):
        return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Retailer country"]).sum()[metricMapper[metric]].to_dict()


@api.route("/channel/<metric>/<years>")
class Channel(Resource):
    def get(self,metric, years):
        return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Order method type"]).sum()[metricMapper[metric]].to_dict()


@api.route("/product/<metric>/<years>")
class Product(Resource):
    def get(self, metric, years):
        return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Product"]).sum()[metricMapper[metric]].sort_values(ascending=False).head(10).to_dict()


@api.route("/actual_revenue/<country>")
class ActualCountryRevenue(Resource):
    def get(self, country):
        return df[df["Retailer country"].str.lower() == country].groupby(by=["Year"]).sum()["Revenue"].to_dict()


@api.route("/countries")
class Countries(Resource):
    def get(self):
        return {"countries": list(df["Retailer country"].unique())}


@api.route("/forecasted_revenue/<country>")
class ForecastedCountryRevenue(Resource):
    def get(self,country):
        countryClean = country.lower().replace(" ", "")
        with open(f"model/output/{countryClean}.pkl", "rb") as f:
            m = pickle.load(f)
        forecast = m.predict(m.make_future_dataframe(
            periods=365))[-1:][["ds", "yhat", "yhat_lower", "yhat_upper"]].reset_index(drop=True)
        forecast_dict = {
            "date": forecast["ds"][0],
            "yhat": forecast["yhat"][0],
            "yhat_lower": forecast["yhat_lower"][0],
            "yhat_upper": forecast["yhat_upper"][0]
        }
        return jsonify(forecast_dict)


if __name__ == "__main__":
    app.run(debug=True)
