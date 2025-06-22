import os
import logging
from pyngrok import ngrok
from app import create_app
import socket


app = create_app()

NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")

if __name__ == "__main__":
    try:
        # Find an available port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()

        public_url = ngrok.connect(port, domain=NGROK_DOMAIN)
        logging.info(f"\n\nngrok tunnel available at: {public_url}\n")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        logging.error(f"Failed to start: {e}")
