import argparse
from trainer import Trainer
from prepare_data import TextCleaner
from data_loader import DataLoader
from decorators import log_call, exception_logger, timeit


@log_call
@exception_logger
@timeit
def run_cleaning() -> None:
    print("=== Nettoyage des données brutes ===")
    loader = DataLoader()
    cleaner = TextCleaner()
    df_raw = loader.load_raw_data()
    df_clean = cleaner.clean_dataframe(df_raw, text_column="text")
    loader.save_processed_data(df_clean)
    print("Données nettoyées et enregistrées.")


@log_call
@exception_logger
@timeit
def run_preview() -> None:
    print("=== Aperçu des données traitées ===")
    loader = DataLoader()
    df = loader.load_processed_data()
    print(df.head())


@log_call
@exception_logger
@timeit
def run_training() -> None:
    print("=== Démarrage de l'entraînement du modèle ===")
    trainer = Trainer()
    trainer.train()
    print("Entraînement terminé et modèle sauvegardé.")


def main() -> None:
    parser = argparse.ArgumentParser(description="MLOps Text Classifier")
    parser.add_argument('--train', action='store_true', help="Lancer l'entraînement du modèle")
    parser.add_argument('--clean', action='store_true', help="Nettoyer les données brutes")
    parser.add_argument('--preview', action='store_true', help="Aperçu des données après nettoyage")
    args = parser.parse_args()

    if args.clean:
        run_cleaning()
    if args.preview:
        run_preview()
    if args.train:
        run_training()


if __name__ == "__main__":
    main()

