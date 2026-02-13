import time
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            return

        if random.random() < 0.1:
            logging.error("Simulated random failure!")
        else:
            logging.info("Handled request successfully.")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from sample-app")

def run():
    server = HTTPServer(("0.0.0.0", 8081), Handler)
    logging.info("Starting server on port 8081...")
    server.serve_forever()

if __name__ == "__main__":
    run()
