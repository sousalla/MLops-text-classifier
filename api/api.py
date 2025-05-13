from flask import Flask, request, jsonify
from jose import jwt, JWTError
import joblib
import datetime
import os
import sys

# === Ajout des chemins ===
sys.path.append(os.path.abspath("src"))
from config import Config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitoring.metrics_exporter import REQUEST_COUNT, monitor_inference, start_metrics_server

# === Initialisation ===
app = Flask(__name__)
SECRET_KEY = Config.JWT_SECRET
ALGORITHM = "HS256"

# === Chargement du modèle et vectorizer ===
model = joblib.load(Config.MODEL_PATH)
vectorizer = joblib.load(Config.VECTORIZER_PATH)

# === Démarrer Prometheus ===
start_metrics_server(Config.METRICS_PORT)

# === JWT : Création & Vérification ===
def create_token(identity: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.TOKEN_EXPIRE_MINUTES)
    payload = {"sub": identity, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None

# === Authentification ===
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        token = create_token(username)
        return jsonify(access_token=token)
    return jsonify({"msg": "Identifiants invalides"}), 401

# === API de prédiction protégée ===
@app.route("/predict", methods=["POST"])
@monitor_inference
def predict():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Token manquant ou invalide"}), 401

    token = auth_header.split(" ")[1]
    user = verify_token(token)
    if not user:
        return jsonify({"msg": "Token expiré ou invalide"}), 401

    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Aucun texte fourni"}), 400

        vect_text = vectorizer.transform([text])
        prediction = model.predict(vect_text)[0]
        result = "spam" if prediction == 1 else "non-spam"

        REQUEST_COUNT.labels(method="POST", endpoint="/predict", status_code="200").inc()
        return jsonify({"text": text, "prediction": result})

    except Exception as e:
        REQUEST_COUNT.labels(method="POST", endpoint="/predict", status_code="500").inc()
        return jsonify({"error": str(e)}), 500

# === Lancement de l'API ===
if __name__ == "__main__":
    print("API démarrée sur http://localhost:5001")
    print("Métriques Prometheus : http://localhost:8001/metrics")
    app.run(host="0.0.0.0", port=5001, debug=True)
