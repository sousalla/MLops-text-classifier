import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask

app = Flask(__name__)

# Clé secrète pour signer les JWT
SECRET_KEY = os.getenv('SECRET_KEY', 'votre_clé_secrète')

# Simuler une base de données d'utilisateurs (exemple simple)
USERS_DB = {
    "user1": {
        "password": generate_password_hash("password123"),  # Mot de passe haché
        "role": "admin"
    },
    "user2": {
        "password": generate_password_hash("password456"),
        "role": "user"
    }
}

# Générer un token JWT
def generate_token(username):
    """Générer un JWT pour un utilisateur."""
    expiration = datetime.utcnow() + timedelta(hours=1)  # Expiration dans 1 heure
    payload = {
        "sub": username,  # Sujet (utilisateur)
        "exp": expiration  # Expiration du token
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Décoder un token JWT
def decode_token(token):
    """Décoder et vérifier le token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide

# Authentification avec JWT (exemple d'endpoint pour se connecter)
def login():
    """Authentification avec nom d'utilisateur et mot de passe."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = USERS_DB.get(username)

    if user and check_password_hash(user["password"], password):
        # Générer un token JWT si les identifiants sont corrects
        token = generate_token(username)
        return jsonify({"message": "Connexion réussie", "token": token}), 200
    else:
        return jsonify({"message": "Identifiants incorrects"}), 401

# Vérification de l'authentification avec JWT pour accéder aux ressources protégées
def token_required(f):
    """Décorateur pour protéger les endpoints nécessitant un token JWT valide."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extraire le token de l'en-tête

        if not token:
            return jsonify({"message": "Token manquant"}), 403

        decoded_payload = decode_token(token)

        if not decoded_payload:
            return jsonify({"message": "Token invalide ou expiré"}), 403

        # Ajouter les informations de l'utilisateur décodées à la requête
        request.user = decoded_payload["sub"]
        return f(*args, **kwargs)

    return decorated_function

# Exemple d'un endpoint protégé
@app.route("/protected", methods=["GET"])
@token_required
def protected_route():
    """Exemple de route protégée nécessitant un token valide."""
    return jsonify({"message": f"Bonjour {request.user}, vous avez accès à cette ressource protégée."})

# Endpoint pour la connexion
@app.route("/login", methods=["POST"])
def user_login():
    return login()

if __name__ == "__main__":
    # Routes API
    app.add_url_rule('/login', 'login', user_login, methods=['POST'])
    app.add_url_rule('/protected', 'protected_route', protected_route, methods=['GET'])

    # Lancer l'application
    app.run(debug=True)

