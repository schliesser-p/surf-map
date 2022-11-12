import folium
import json
from flask import Flask, render_template, request
import git
import sys

path = '/home/vipete/surf-map/'
if path not in sys.path:
   sys.path.insert(0, path)

app = Flask(__name__)

with open("./spots_location.json", "r") as f:
    js = json.load(f)

def add_marker_to_map(m, lat, long, popup):
    folium.Marker(location=[lat, long], popup=popup).add_to(m)

def create_map(data, country):
    map = folium.Map(location=[1, 1], zoom_start=3, tiles="Stamen Toner", prefer_canvas=True)
    for spot, value in data[country].items():
        if value is not None:
            lat = value["lat"] 
            lon = value["lon"]
            popup = value["display_name"]

            add_marker_to_map(map, lat, lon, popup)

    return map._repr_html_()

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./surf-map')
        origin = repo.remotes.origin
        repo.create_head('master', 
    origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        origin.pull()
        return 'Updated', 200
    else:
        return 'Something went wrong...', 400

@app.route('/input')
def index():    
    return render_template("input-form.html")

@app.route('/map', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text
    return create_map(js, processed_text)


if __name__ == '__main__':
    app.run()
