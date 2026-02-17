import time
import logging
import random
import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def busy_work(n: int = 5_000_000):
    x = 0
    for i in range(n):
        x += i
    return x


def cpu_hog():
    while True:
        pass

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        busy_work(5_000_000)
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
    for _ in range(4):
        multiprocessing.Process(target=cpu_hog).start()

    server = HTTPServer(("0.0.0.0", 8081), Handler)
    logging.info("Starting server on port 8081...")
    server.serve_forever()

if __name__ == "__main__":
    run()
