import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple
from config import Config
import logging
import os

# Configuration du dossier de log
LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "data_loader.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataLoader:
    def __init__(self, config: type = Config):
        self.config = config
        self.raw_data_path: str = config.RAW_DATA_PATH
        self.processed_data_path: str = config.PROCESSED_DATA_PATH
        self.test_size: float = config.TEST_SIZE
        self.random_state: int = config.RANDOM_STATE

    def load_data(self, processed: bool = True) -> pd.DataFrame:
        """
        Charge les données à partir d'un fichier CSV (brut ou traité).
        """
        path: str = self.processed_data_path if processed else self.raw_data_path
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError as e:
            logging.error(f"Fichier non trouvé : {path}")
            raise FileNotFoundError(f"Fichier non trouvé : {path}") from e
        except Exception as e:
            logging.error(f"Erreur inattendue lors du chargement du fichier : {e}")
            raise

    def get_train_test_split(self, processed: bool = True) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        """
        Retourne X_train, X_test, y_train, y_test à partir des données.
        """
        df = self.load_data(processed)

        if 'text' not in df.columns or 'label' not in df.columns:
            msg = "Les colonnes 'text' et 'label' sont requises."
            logging.error(msg)
            raise ValueError(msg)

        X = df['text']
        y = df['label']
        return train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
