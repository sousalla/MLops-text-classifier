from prometheus_client import start_http_server, Gauge, Counter
import time
import random
import sys

# --- Métriques globales exportables ---
REQUEST_COUNT = Counter(
    'app_request_count_total',
    'Nombre total de requêtes traitées'
)

MEMORY_USAGE = Gauge(
    'app_memory_usage_megabytes',
    'Utilisation de la mémoire en Mo'
)


# --- Fonctions exportables ---
def monitor_inference():
    """Simule un appel d'inférence et met à jour les métriques."""
    REQUEST_COUNT.inc()
    MEMORY_USAGE.set(random.uniform(50.0, 500.0))


def start_metrics_server(port: int = 8000, interval: int = 5):
    """Démarre le serveur Prometheus et met à jour les métriques périodiquement."""
    start_http_server(port)
    print(f"Serveur Prometheus démarré sur http://localhost:{port}/metrics")

    try:
        while True:
            monitor_inference()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n Arrêt du serveur Prometheus.")
        sys.exit(0)
