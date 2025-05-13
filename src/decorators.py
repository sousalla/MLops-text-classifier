import time
import functools
import logging
import os


# Création du dossier de logs s'il n'existe pas
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configuration du logger
LOG_FILE = os.path.join(LOG_DIR, "decorators.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()  # Affiche dans la console
    ]
)

# Utilisation standard du logger
logger = logging.getLogger(__name__)

def timeit(func):
    """
    Mesure le temps d'exécution d'une fonction.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"[{func.__name__}] exécutée en {end - start:.4f} secondes.")
        return result
    return wrapper

def exception_logger(func):
    """
    Log les exceptions levées dans une fonction décorée.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception dans {func.__name__}: {e}")
            raise
    return wrapper

def log_call(func):
    """
    Log l'appel d'une fonction avec ses arguments.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Appel de {func.__name__} avec args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper
