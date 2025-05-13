import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from joblib import load
from config import Config
from data_loader import get_train_test_data


class ModelEvaluator:
    """Classe d'évaluation d'un modèle de classification."""

    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = self._load_model(model_path)
        self.vectorizer = self._load_vectorizer(vectorizer_path)

    @staticmethod
    def _load_model(path: str):
        try:
            return load(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Modèle non trouvé à l'emplacement : {path}")

    @staticmethod
    def _load_vectorizer(path: str):
        try:
            return load(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Vectorizer non trouvé à l'emplacement : {path}")

    def evaluate(self, X_test: pd.Series, y_test: pd.Series) -> dict:
        """Évalue le modèle sur les données de test."""
        X_vectorized = self.vectorizer.transform(X_test)
        y_pred = self.model.predict(X_vectorized)

        report = classification_report(y_test, y_pred, output_dict=True)
        accuracy = accuracy_score(y_test, y_pred)
        matrix = confusion_matrix(y_test, y_pred)

        return {
            "accuracy": accuracy,
            "classification_report": report,
            "confusion_matrix": matrix.tolist(),  # Pour une meilleure lisibilité JSON
        }


if __name__ == "__main__":
    print("🔍 Chargement des données de test...")
    _, X_test, _, y_test = get_train_test_data(processed=True)

    evaluator = ModelEvaluator(
        model_path=Config.MODEL_PATH,
        vectorizer_path=Config.VECTORIZER_PATH
    )

    print("📊 Évaluation du modèle...")
    results = evaluator.evaluate(X_test, y_test)

    print(f"✅ Accuracy : {results['accuracy']:.4f}")
    print("📄 Classification Report :")
    for label, metrics in results["classification_report"].items():
        if isinstance(metrics, dict):
            print(f"{label}: {metrics}")
    print("🧮 Matrice de confusion :")
    print(results["confusion_matrix"])
