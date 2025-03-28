"""."""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from client_server import ClientServer


def main():
    """."""
    server = ClientServer('localhost', 8080)

    server.run()


main()
