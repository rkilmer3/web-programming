from flask import Flask, jsonify, render_template
from mongita import MongitaClientDisk

# create a mongita client connection
client = MongitaClientDisk()

# open then movie database
movie_db = client.movie_db

app = Flask(__name__)

@app.route("/data/movies/scifi")
def get_data_movies_scifi():
    # with open("classic_sci_fi_movies.json","r") as f:
    #     data = json.load(f)
    # open the scifi collection
    scifi_collection = movie_db.scifi_collection
    data = list(scifi_collection.find({}))
    for item in data:
        del item["_id"] 
    return jsonify(data)

@app.route('/')
def serve_index():
    return send_from_directory('.', "index.html")

@app.route("/movies")
def get_movies():
    scifi_collection = movie_db.scifi_collection
    data = list(scifi_collection.find({}))
    for item in data:
        del item["_id"] 
    movies = jsonify(data)
    return render_template("movies.html", movies)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)
