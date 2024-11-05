from flask import Flask, render_template, jsonify
from network_scanner import NetworkScanner
import threading
import requests

app = Flask(__name__)
scanner = NetworkScanner()

@app.route('/')
def index():
    return render_template('index.html')  # Zwróć stronę główną

@app.route('/scan')
def scan():
    # Rozpocznij skanowanie w nowym wątku
    thread = threading.Thread(target=scanner.scan_network_for_devices)
    thread.start()
    thread.join()  # Czekaj na zakończenie skanowania
    return jsonify(scanner.devices)  # Zwróć znalezione urządzenia jako JSON


if __name__ == '__main__':
    app.run(debug=True)  # Uruchom serwer
