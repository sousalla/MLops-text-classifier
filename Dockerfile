# Étape 1 : Image de base
FROM python:3.13-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers du projet
COPY . /app

# Étape 4 : Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Étape 5 : Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 6 : Initialiser DVC (optionnel si déjà initialisé)
RUN dvc init --no-scm || true
RUN dvc pull -f

# Étape 7 : Exposer le port de l’API Flask
EXPOSE 5000

# Étape 8 : Définir la commande de démarrage
CMD ["python", "api/api.py"]


