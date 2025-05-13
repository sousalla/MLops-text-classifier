import re
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))  # Liste des mots vides en anglais
        self.punctuation = string.punctuation  # Ponctuation à enlever
    
    def remove_punctuation(self, text):
        """Enlève la ponctuation d'un texte."""
        return ''.join([char for char in text if char not in self.punctuation])

    def remove_stopwords(self, text):
        """Enlève les mots vides (stopwords) d'un texte."""
        words = word_tokenize(text.lower())
        return ' '.join([word for word in words if word not in self.stop_words])

    def remove_urls(self, text):
        """Enlève les URLs d'un texte."""
        return re.sub(r'http\S+|www\S+', '', text)

    def remove_numbers(self, text):
        """Enlève les chiffres d'un texte."""
        return re.sub(r'\d+', '', text)

    def to_lowercase(self, text):
        """Convertit tout le texte en minuscules."""
        return text.lower()

    def clean_text(self, text):
        """Applique toutes les étapes de nettoyage sur un texte."""
        text = self.remove_urls(text)
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.remove_stopwords(text)
        text = self.to_lowercase(text)
        return text

    def clean_dataframe(self, df, text_column='text'):
        """Nettoie une colonne de texte d'un DataFrame."""
        if text_column not in df.columns:
            raise ValueError(f"La colonne '{text_column}' est absente dans le DataFrame.")
        
        df[text_column] = df[text_column].apply(self.clean_text)
        return df
