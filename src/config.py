import os
from datetime import timedelta

class Config:
    # === Répertoires ===
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Répertoire de base (là où ce fichier est situé)
    RAW_DATA_PATH = os.path.join(BASE_DIR, "../data/raw/data.csv")  # Chemin vers les données brutes
    PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "../data/processed/data.csv")  # Chemin vers les données traitées
    MODEL_PATH = os.path.join(BASE_DIR, "../models/spam_classifier.pkl")  # Chemin vers le modèle sauvegardé
    VECTORIZER_PATH = os.path.join(BASE_DIR, "../models/vectorizer.pkl")  # Chemin vers le vecteur de transformation

    # === Entraînement ===
    TEST_SIZE = 0.2  # Proportion des données pour le test
    RANDOM_STATE = 42  # Valeur de la graine aléatoire pour la reproductibilité
    MODEL_TYPE = "logistic_regression"  # Type de modèle utilisé (Options : "naive_bayes", "svm", "random_forest", etc.)

    # === Authentification JWT ===
    JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret_change_me")  # Secret pour JWT, à remplacer en production
    JWT_ALGORITHM = "HS256"  # Algorithme de chiffrement pour JWT
    TOKEN_EXPIRE_MINUTES = 30  # Durée de validité du token en minutes
    ACCESS_TOKEN_EXPIRE = timedelta(minutes=TOKEN_EXPIRE_MINUTES)  # Délai d'expiration du token

    # === Monitoring (Prometheus + Grafana) ===
    METRICS_PORT = 8001  # Port d'écoute pour les métriques Prometheus

    # === Paramètres supplémentaires ===
    LOGGING_LEVEL = "INFO"  # Niveau de log (par exemple "INFO", "DEBUG", "ERROR")
    DEBUG_MODE = True  # Mode débogage activé ou non
    TIMEZONE = "UTC"  # Fuseau horaire par défaut

    # === Base de données (si applicable) ===
    DB_HOST = os.environ.get("DB_HOST", "localhost")  # Hôte de la base de données
    DB_PORT = os.environ.get("DB_PORT", 5432)  # Port de la base de données
    DB_NAME = os.environ.get("DB_NAME", "mlops_db")  # Nom de la base de données
    DB_USER = os.environ.get("DB_USER", "root")  # Utilisateur de la base de données
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")  # Mot de passe de la base de données

    # === API Configuration ===
    API_HOST = os.environ.get("API_HOST", "0.0.0.0")  # Hôte de l'API
    API_PORT = os.environ.get("API_PORT", 8080)  # Port de l'API
    API_PREFIX = "/api/v1"  # Préfixe des routes de l'API

    # === Autres configurations ===
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # Taille maximale des fichiers à télécharger (10MB)
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Format de log
    LOGGING_DATEFMT = "%Y-%m-%d %H:%M:%S"  # Format de la date dans les logs
