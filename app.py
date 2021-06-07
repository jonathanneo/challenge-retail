from flask import Flask, session, request, redirect, render_template
import pandas as pd
import os
import json
from fbprophet import Prophet
import pickle
import datetime as dt

# create flask app
app = Flask(__name__)

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


@app.route("/api/timeseries/<metric>/<years>")
def time_series(metric, years):
    return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Year"]).sum()[metricMapper[metric]].to_dict()


@app.route("/api/country/<metric>/<years>")
def country(metric, years):
    return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Retailer country"]).sum()[metricMapper[metric]].to_dict()


@app.route("/api/channel/<metric>/<years>")
def channel(metric, years):
    return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Order method type"]).sum()[metricMapper[metric]].to_dict()


@app.route("/api/product/<metric>/<years>")
def product(metric, years):
    return df[df["Year"].isin(map(int, years.split(",")))].groupby(by=["Product"]).sum()[metricMapper[metric]].sort_values(ascending=False).head(10).to_dict()


@app.route("/api/predict/<country>")
def predict(country):
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
    return forecast_dict


if __name__ == "__main__":
    app.run(debug=True)
