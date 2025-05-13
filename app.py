from flask import Flask, request, render_template
import joblib
import os
import sys

# === Ajout des chemins ===
sys.path.append(os.path.abspath("src"))
from config import Config

# === Initialisation de Flask ===
app = Flask(__name__)

# === Chargement du modèle et vectorizer ===
model = joblib.load(Config.MODEL_PATH)
vectorizer = joblib.load(Config.VECTORIZER_PATH)

# === Page d'accueil ===
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html") 

# === Prédiction via le formulaire HTML ===
@app.route("/predict-form", methods=["POST"])
def predict_form():
    text = request.form.get("text", "")
    if not text:
        return render_template("index.html", prediction="Erreur : aucun texte fourni.")

    vect_text = vectorizer.transform([text])
    prediction = model.predict(vect_text)[0]
    result = "SPAM" if prediction == 1 else "NON-SPAM"
    return render_template("index.html", prediction=result)

# === Lancement de l'application ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
