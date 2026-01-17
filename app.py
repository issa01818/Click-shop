# app.py

# Ajoute cette ligne pour appliquer le patch global pour xmlrpc.client
from defusedxml import xmlrpc  # Patch global pour xmlrpclib

from flask import Flask, render_template, request, redirect, url_for, make_response
import os
# from prometheus_client import start_http_server, Counter, generate_latest  # Commenté pour Render

app = Flask(__name__)

# Liste des produits
produits = [
    {"nom": "Casque Audio", "prix": 45, "couleur": "black", "image": "https://via.placeholder.com/150"},
    {"nom": "Clavier Mécanique", "prix": 34, "couleur": "black", "image": "https://via.placeholder.com/150"},
    {"nom": "Souris Gamer", "prix": 67, "couleur": "red", "image": "https://via.placeholder.com/150"},
    {"nom": "Ecouteurs Sans Fils", "prix": 76, "couleur": "white", "image": "https://via.placeholder.com/150"},
    {"nom": "T-shirt Tech", "prix": 23, "couleur": "gray", "image": "https://via.placeholder.com/150"},
    {"nom": "Sac à Dos", "prix": 64, "couleur": "blue", "image": "https://via.placeholder.com/150"},
]

# Déclaration d'un compteur pour les requêtes HTTP (Prometheus désactivé pour Render)
# REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

# Middleware pour ajouter les headers de sécurité à chaque réponse
@app.after_request
def add_security_headers(response):
    # Contre XSS / injection
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted.cdn.com; "
        "style-src 'self' https://fonts.googleapis.com; "
        "img-src 'self' https://trusted-images.com; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    # Anti-clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    # Protection contre le sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # HSTS (HTTPS uniquement)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Référent strict
    response.headers["Referrer-Policy"] = "no-referrer"
    # Cache-Control
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Page d'accueil
@app.route('/')
def index():
    # REQUESTS.inc()  # compteur Prometheus désactivé pour Render
    return render_template('index.html', produits=produits)

# Page du panier
@app.route('/panier')
def panier():
    # REQUESTS.inc()  # compteur Prometheus désactivé pour Render
    return render_template('panier.html')

# Endpoint métriques Prometheus (optionnel, uniquement local)
# @app.route('/metrics')
# def metrics():
#     return generate_latest()  # Expose les métriques au format Prometheus

# Démarrer l'application
if __name__ == "__main__":
    # Render fournit le port via l'environnement
    port = int(os.environ.get("PORT", 5006))  # fallback à 5006 si local
    debug = os.getenv("FLASK_ENV") == "development"     
    # Prometheus désactivé pour éviter conflit de port
    # start_http_server(8000)
    
    # Flask écoute sur 0.0.0.0 pour Render
    app.run(host="0.0.0.0", port=port, debug=debug)

