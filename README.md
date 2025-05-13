# 📧 Spam Email Classifier - MLOps Project

## 🔍 Description

Ce projet a pour objectif de classifier automatiquement des emails comme **spam** ou **non spam**, en utilisant des techniques de machine learning. Il suit une architecture modulaire inspirée des pratiques MLOps, intégrant un pipeline complet de traitement, d'entraînement, d'évaluation et de déploiement.

---

## 📁 Architecture du projet

```
.
├── api/
│   ├── api.py                # Endpoints de l'API Flask
│   └── auth.py               # Authentification et sécurité de l'API
├── data/                     # Données brutes ou prétraitées
├── logs/                     # Fichiers de logs
├── models/                   # Modèles ML sauvegardés (pickle)
├── monitoring/               # Scripts de surveillance (drift, métriques...)
├── src/
│   ├── config.py             # Configuration globale du projet
│   ├── data_loader.py        # Chargement des données
│   ├── decorators.py         # Décorateurs utiles (log, cache, etc.)
│   ├── eda_dashboard.py      # Dashboard EDA Streamlit
│   ├── evaluate.py           # Évaluation du modèle
│   ├── main.py               # Script principal du pipeline ML
│   ├── model_factory.py      # Création et gestion des modèles
│   ├── prepare_data.py       # Nettoyage et préparation des données
│   ├── text_cleaner.py       # Fonctions de nettoyage de texte
│   └── trainer.py            # Entraînement du modèle
├── templates/
│   └── index.html            # Interface utilisateur web (Flask)
├── app.py                    # Application Flask principale
├── Dockerfile                # Fichier Docker pour conteneuriser le projet
├── dvc.yaml                  # Pipeline DVC (Data Version Control)
├── requirements.txt          # Liste des dépendances Python
└── README.md                 # déscription de projet
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer le dashboard d'analyse exploratoire (EDA)

```bash
streamlit run src/eda_dashboard.py
```

### 4. Lancer l'application Flask

```bash
python app.py
```

---

## 🧪 Fonctionnalités principales

* Nettoyage automatique du texte (ponctuation, stopwords, etc.).
* Vectorisation avec TF-IDF.
* Classification par modèles ML (Naive Bayes, SVM, etc.).
* Interface web conviviale via Flask.
* Visualisation interactive des données avec **Streamlit**.
* Traçabilité et reproductibilité via **DVC**.
* Conteneurisation du projet avec **Docker**.

---

## 🛠️ Technologies utilisées

| Outil / Librairie | Rôle principal                           |
| ----------------- | ---------------------------------------- |
| Flask             | Interface web pour la classification     |
| Streamlit         | Dashboard interactif pour l'analyse EDA  |
| scikit-learn      | Machine learning, preprocessing          |
| DVC               | Suivi des versions de données & pipeline |
| Docker            | Déploiement portable                     |
| Pandas / NumPy    | Manipulation de données                  |

---

## 📊 Exemple d'utilisation

* L'utilisateur saisit le contenu d’un email dans l’interface web.
* Le texte est nettoyé, vectorisé puis classifié.
* Le résultat s’affiche : **SPAM** ou **NON-SPAM**.

---

## 📈 Monitoring & Amélioration

* 📉 Suivi de la performance avec `evaluate.py`.
* 📊 Surveillance des dérives futures (drift) via `monitoring/`.
* 🔁 Possibilité d’ajouter d’autres modèles dans `model_factory.py`.

---

## 📦 Déploiement avec Docker

```bash
docker build -t spam-classifier .
docker run -p 5000:5000 spam-classifier
```

---

## 👨‍💻 Auteur

Soufiane Aalla
Master Data Science & Sécurité des Systèmes d’Information
Université Sultan Moulay Slimane - Beni Mellal

