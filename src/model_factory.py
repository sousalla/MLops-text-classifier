from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

class ModelFactory:
    """
    Classe pour instancier dynamiquement des modèles de classification.
    """

    def __init__(self, model_name: str = "logistic_regression"):
        """
        Initialise la classe avec le modèle à utiliser.

        Args:
            model_name (str): Le nom du modèle à instancier (par défaut 'logistic_regression').
        """
        self.model_name = model_name.lower()
    
    def get_model(self):
        """
        Retourne une instance du modèle spécifié.
        
        Returns:
            Un modèle scikit-learn prêt à être entraîné.
        """
        if self.model_name == "logistic_regression":
            return LogisticRegression(solver='liblinear', random_state=42)
        
        elif self.model_name == "naive_bayes":
            return MultinomialNB()
        
        elif self.model_name == "svm":
            return LinearSVC(random_state=42)
        
        elif self.model_name == "random_forest":
            return RandomForestClassifier(n_estimators=100, random_state=42)
        
        else:
            raise ValueError(f"Modèle non supporté : {self.model_name}")
