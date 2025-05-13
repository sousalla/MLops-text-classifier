import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging
from wordcloud import WordCloud
from config import Config
from text_cleaner import TextCleaner


# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/eda.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Chargement des données avec cache
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(Config.PROCESSED_DATA_PATH)
        logger.info("Données chargées depuis %s", Config.PROCESSED_DATA_PATH)
        return df
    except FileNotFoundError:
        logger.warning("Fichier non trouvé : %s", Config.PROCESSED_DATA_PATH)
        return None

# Affichage de la distribution des classes
def plot_class_distribution(df):
    st.subheader("Répartition des classes")
    class_counts = df['label'].value_counts()
    st.bar_chart(class_counts)
    logger.info("Affichage du graphique de répartition des classes.")

def plot_message_length(df):
    st.subheader("📏 Longueur des messages")

    # Remplacer les valeurs nulles par une chaîne vide
    df['text'] = df['text'].fillna("")

    # Calculer la longueur après conversion explicite en chaîne
    df['length'] = df['text'].apply(lambda x: len(str(x).split()))

    st.line_chart(df['length'])
    logger.info("Affichage de l'histogramme des longueurs de messages.")


# Affichage du nuage de mots
def plot_wordcloud(df):
    st.subheader("Nuage de mots")
    text = " ".join(df['text'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    logger.info("Affichage du nuage de mots.")

# Fonction principale
def main():
    st.title("Tableau de bord EDA - Spam Classifier")
    logger.info("Lancement de l'application EDA.")

    df = load_data()
    if df is None:
        st.warning("Aucune donnée trouvée. Veuillez exécuter la phase de prétraitement d'abord.")
        logger.warning("Aucune donnée disponible pour l'EDA.")
        return

    st.dataframe(df.head())
    logger.info("Aperçu des premières lignes du dataset affiché.")

    with st.expander("Aperçu du jeu de données"):
        st.write(df.describe(include='all'))
        logger.info("Résumé statistique du dataset affiché.")

    plot_class_distribution(df)
    plot_message_length(df)
    plot_wordcloud(df)
    logger.info("EDA terminée avec succès.")

if __name__ == "__main__":
    main()
