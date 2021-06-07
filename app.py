from flask import Flask, session, request, redirect, render_template
import pandas as pd
import os
import json
from fbprophet import Prophet
import pickle
import datetime as dt
import markdown as md

# create flask app
app = Flask(__name__,static_url_path='/static')

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

# @app.route("/report")
# def report():
#     return render_template("report.html")

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


@app.route("/api/actual_revenue/<country>")
def actual_country_revenue(country):
    print(country)
    return df[df["Retailer country"].str.lower() == country].groupby(by=["Year"]).sum()["Revenue"].to_dict()


@app.route("/api/countries")
def countries():
    return {"countries": list(df["Retailer country"].unique())}


@app.route("/api/forecasted_revenue/<country>")
def forecasted_country_revenue(country):
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
