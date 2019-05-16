from prometheus_client import start_http_server
from metrics.eskom import Exporter as Eskom_Exporter
import threading
import signal
import sys

from prometheus_client.core import REGISTRY


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


if __name__ == '__main__':
    # Exporters go here. Eskom example provided

    REGISTRY.register(
        Eskom_Exporter()
    )

    # Start up the server to expose the metrics.
    start_http_server(8000)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    forever = threading.Event()
    forever.wait()

