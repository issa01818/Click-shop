# app.py

# Ajoute cette ligne pour appliquer le patch global pour xmlrpc.client
from defusedxml import xmlrpc  # Patch global pour xmlrpclib

from flask import Flask, render_template, request, redirect, url_for
import os
from prometheus_client import start_http_server, Counter, generate_latest

app = Flask(__name__)

# ----- AJOUT DE TOUS LES HEADERS DE SECURITE -----
@app.after_request
def set_security_headers(response):
    # Content Security Policy (CSP)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    # Headers de protection supplémentaires
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Headers pour désactiver le cache des pages sensibles
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
# -----------------------------------------------

# Liste des produits
produits = [
    {"nom": "Casque Audio", "prix": 45, "couleur": "black", "image": "https://via.placeholder.com/150"},
    {"nom": "Clavier Mécanique", "prix": 34, "couleur": "black", "image": "https://via.placeholder.com/150"},
    {"nom": "Souris Gamer", "prix": 67, "couleur": "red", "image": "https://via.placeholder.com/150"},
    {"nom": "Ecouteurs Sans Fils", "prix": 76, "couleur": "white", "image": "https://via.placeholder.com/150"},
    {"nom": "T-shirt Tech", "prix": 23, "couleur": "gray", "image": "https://via.placeholder.com/150"},
    {"nom": "Sac à Dos", "prix": 64, "couleur": "blue", "image": "https://via.placeholder.com/150"},
]

# Déclaration d'un compteur pour les requêtes HTTP (pour Prometheus)
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

# Page d'accueil
@app.route('/')
def index():
    REQUESTS.inc()  # Incrémente le compteur à chaque requête sur la page d'accueil
    return render_template('index.html', produits=produits)

# Page du panier
@app.route('/panier')
def panier():
    REQUESTS.inc()  # Incrémente le compteur à chaque requête sur la page du panier
    return render_template('panier.html')

# Endpoint pour exposer les métriques à Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest()  # Expose les métriques au format Prometheus

# Démarrer l'application
if __name__ == '__main__':
    # Démarre un serveur HTTP pour exposer les métriques sur le port 8000
    start_http_server(8000)  # Ce serveur expose les métriques sur /metrics

    # Vérifie si l'environnement est 'development' ou 'production'
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=5006)  # Ton application Flask tourne sur 5006

