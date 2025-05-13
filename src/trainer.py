import logging
from typing import Tuple
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

from config import Config
from model_factory import ModelFactory
from prepare_data import DataPreparer

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/training.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Trainer:
    def __init__(self) -> None:
        logger.info("Initialisation du trainer...")
        self.data_preparer = DataPreparer()
        model_factory = ModelFactory(model_name=Config.MODEL_TYPE)
        self.model = model_factory.get_model()
        self.vectorizer = TfidfVectorizer()

    def prepare_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prépare les données et retourne les jeux de données vectorisés"""
        logger.info("Chargement et préparation des données...")
        df: pd.DataFrame = self.data_preparer.prepare()

        X = df['text']
        y = df['label']

        logger.info("Découpage en jeu d'entraînement et de test...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE
        )

        logger.info("Vectorisation des textes avec TF-IDF...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        return X_train_vec, X_test_vec, y_train, y_test

    def train(self) -> None:
        logger.info("Démarrage de l'entraînement du modèle...")
        X_train_vec, X_test_vec, y_train, y_test = self.prepare_data()

        self.model.fit(X_train_vec, y_train)
        logger.info("✅ Entraînement terminé.")

        logger.info("Prédiction sur le jeu de test...")
        y_pred = self.model.predict(X_test_vec)

        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"🎯 Précision du modèle sur le jeu de test : {accuracy * 100:.2f}%")

        self.save_model()

    def evaluate(self) -> None:
        logger.info("Évaluation du modèle - non implémentée dans cette version.")

    def save_model(self) -> None:
        logger.info("Sauvegarde du modèle et du vectoriseur dans le dossier processed...")
        joblib.dump(self.model, Config.MODEL_PATH)
        joblib.dump(self.vectorizer, Config.VECTORIZER_PATH)
        logger.info(f"✅ Modèle sauvegardé dans : {Config.MODEL_PATH}")
        logger.info(f"✅ Vectoriseur sauvegardé dans : {Config.VECTORIZER_PATH}")

if __name__ == "__main__":
    trainer = Trainer()
    trainer.train()
    trainer.evaluate()
    logger.info("Entraînement et évaluation terminés.")