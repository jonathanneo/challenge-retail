from flask import Flask, session, request, redirect, render_template, jsonify
import pandas as pd 
import os 
import json 

# create flask app 
app = Flask(__name__)

df = pd.read_csv("retail.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/timeseries/<metric>/<years>")
def time_series(metric, years):
    if metric.lower() == "revenue":
        return df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Year"]).sum()["Revenue"].to_dict()

@app.route("/api/country/<metric>/<years>")
def country(metric, years):
    if metric.lower() == "revenue":
        return  df[df["Year"].isin(map(int,years.split(",")))].groupby(by=["Retailer country"]).sum()["Revenue"].sort_values().to_dict()


if __name__ == "__main__":
    app.run(debug=True)