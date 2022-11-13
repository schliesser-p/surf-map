import folium
import csv
import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# data_path = "./spot_location.csv"
data_path = "spot_location.csv" 

pdf = pd.read_csv(data_path, encoding="utf-8")
    

def add_marker_to_map(m, lat, lon, popup):
    folium.Marker(location=[lat, lon], popup=popup).add_to(m)

def create_map(data, spot):
    map = folium.Map(location=[1, 1], zoom_start=3, tiles="Stamen Toner")
    if spot is not None:
        spot_data = pdf.loc[pdf["Name"] == spot]
        lon = spot_data["Longitude__X_"]
        lat = spot_data["Latitude__Y_"]
        add_marker_to_map(map, lat, lon, spot)
    else:
        for index, row in pdf.iterrows():
            name = row.loc["Name"]
            lon = row.loc["Longitude__X_"]
            lat = row.loc["Latitude__Y_"]
            add_marker_to_map(map, lat, lon, name)

    return map._repr_html_()

@app.route('/')
def index():    
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['search'] or None
    processed_text = text
    return render_template("index.html", result=create_map(pdf, processed_text))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
