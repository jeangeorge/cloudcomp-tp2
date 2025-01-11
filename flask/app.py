import os
import pickle
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.environ.get("MODEL_PATH", "../local_data/model.pkl")
MODEL_DATE = None
MODEL = None

def load_model():
    global MODEL, MODEL_DATE

    if not os.path.exists(MODEL_PATH):
        return

    file_mod_time = os.path.getmtime(MODEL_PATH)

    with open(MODEL_PATH, 'rb') as f:
        MODEL = pickle.load(f)
    MODEL_DATE = file_mod_time
    print("MODEL reloaded at:", time.ctime(MODEL_DATE))

def get_recommendations(user_songs, max_recs=5, min_conf=0.0):
    if MODEL is None or "rules" not in MODEL:
        return []

    rules = MODEL["rules"]

    user_songs_set = set(user_songs)
    recommended = set()
    
    for (antecedent, consequent, confidence) in rules:
        if confidence < min_conf:
            continue

        if antecedent.issubset(user_songs_set):
            recommended.update(consequent)
            
    recommended.difference_update(user_songs_set)

    recommended_list = list(recommended)

    return recommended_list[:max_recs]

@app.route("/api/recommend", methods=["POST"])
def recommend():
    load_model()

    if MODEL is None:
        return jsonify({"error": "MODEL is not available"}), 500

    body = request.get_json()
    songs = body.get("songs", [])
    if not songs:
        return jsonify({"error": "Please provide songs"}), 400

    recommended_songs = get_recommendations(
        user_songs=songs,
        max_recs=10,
        min_conf=0.3
    )

    response = {
        "songs": recommended_songs,
        "version": "1.0.0",
        "model_date": time.ctime(MODEL_DATE) if MODEL_DATE else "No model loaded"
    }
    return jsonify(response)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 52034))
    app.run(debug=True, host="0.0.0.0", port=port)
