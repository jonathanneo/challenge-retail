from flask import Flask, session, request, redirect, render_template
import pandas as pd 
import os 
import json 

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
    return df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Year"]).sum()[metricMapper[metric]].to_dict()

@app.route("/api/country/<metric>/<years>")
def country(metric, years):
    return  df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Retailer country"]).sum()[metricMapper[metric]].to_dict()


@app.route("/api/channel/<metric>/<years>")
def channel(metric, years):
    return df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Order method type"]).sum()[metricMapper[metric]].to_dict()

@app.route("/api/product/<metric>/<years>")
def product(metric, years):
    return df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Product"]).sum()[metricMapper[metric]].sort_values(ascending=False).head(10).to_dict()


if __name__ == "__main__":
    app.run(debug=True)