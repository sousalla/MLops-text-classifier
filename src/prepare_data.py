import os
import pandas as pd
import logging
from config import Config
from text_cleaner import TextCleaner

# Créer le dossier logs s'il n'existe pas
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Définir le chemin du fichier log
log_file = os.path.join(log_dir, "data_preparation.log")

# Configuration du logging
logging.basicConfig(
    filename=log_file,             # Enregistrer dans le fichier
    filemode='a',                  # Ajouter au fichier (append)
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class DataPreparer:
    def __init__(self):
        self.cleaner = TextCleaner()

    def load_raw_data(self, path=None):
        """Charger les données brutes depuis le fichier CSV."""
        path = path or Config.RAW_DATA_PATH
        if not os.path.exists(path):
            logger.error(f"Fichier brut non trouvé : {path}")
            raise FileNotFoundError(f"Fichier brut non trouvé : {path}")
        logger.info(f"Fichier brut chargé depuis : {path}")
        return pd.read_csv(path)

    def convert_dataset(self, df):
        """Convertir le dataset en format attendu avec les colonnes 'label' et 'text'."""
        # Vérifier que les colonnes 'v1' et 'v2' existent
        if 'v1' not in df.columns or 'v2' not in df.columns:
            logger.error("Les colonnes 'v1' et 'v2' doivent être présentes dans les données brutes.")
            raise ValueError("Les colonnes 'v1' et 'v2' doivent être présentes dans les données brutes.")
        
        # Sélectionner et renommer les colonnes nécessaires
        df_transformed = df[['v1', 'v2']].copy()
        df_transformed.columns = ['label', 'text']

        # Convertir les labels en valeurs numériques : 'spam' = 1, 'ham' = 0
        df_transformed['label'] = df_transformed['label'].map({'ham': 0, 'spam': 1})

        # Vérification
        if df_transformed['label'].isnull().any():
            logger.warning("Certaines étiquettes n'ont pas pu être converties (valeurs inattendues dans 'label').")

        logger.info("Dataset converti avec 'label' numérique (spam=1, ham=0) et colonne 'text'.")
        return df_transformed

    def save_processed_data(self, df, path=None):
        """Sauvegarder les données nettoyées dans un fichier CSV."""
        path = path or Config.PROCESSED_DATA_PATH
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        logger.info(f"Données nettoyées enregistrées dans : {path}")

    def prepare(self):
        """Préparer et nettoyer les données."""
        logger.info("Chargement des données brutes...")
        df = self.load_raw_data()

        logger.info("Conversion du dataset...")
        # Convertir les données en format 'label' et 'text'
        df_transformed = self.convert_dataset(df)

        if 'text' not in df_transformed.columns:
            logger.error("Colonne 'text' manquante dans les données converties.")
            raise ValueError("Colonne 'text' manquante dans les données converties.")

        logger.info("🧹 Nettoyage du texte...")
        df_cleaned = self.cleaner.clean_dataframe(df_transformed, text_column='text')

        logger.info("💾 Sauvegarde des données nettoyées...")
        self.save_processed_data(df_cleaned)

        return df_cleaned


if __name__ == "__main__":
    preparer = DataPreparer()
    preparer.prepare()
    logger.info("Préparation des données terminée.")