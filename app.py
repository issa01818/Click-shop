from defusedxml import xmlrpc  # Patch global pour xmlrpclib

from flask import Flask, render_template, request, redirect, url_for, make_response
import os

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

# Middleware pour ajouter les headers de sécurité à chaque réponse
@app.after_request
def add_security_headers(response):
    # Contre XSS / injection
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "  # Utilisation de 'self' pour toutes les ressources par défaut
        "script-src 'self' https://trusted.cdn.com; "  # Scripts provenant de sources sûres
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "  # Styles provenant de sources sûres (unsafe-inline si nécessaire)
        "img-src 'self' https://trusted-images.com; "  # Images provenant de sources sûres
        "font-src 'self' https://fonts.gstatic.com; "  # Polices provenant de sources sûres
        "object-src 'none'; "  # Empêcher le chargement des objets (ex : flash, applets)
        "frame-src 'none'; "  # Empêcher l'utilisation de frames (protection contre le clickjacking)
        "connect-src 'self' https://trusted-api.com; "  # API externes de confiance
        "media-src 'none'; "  # Empêcher le chargement des médias (audio/vidéo)
        "child-src 'none'; "  # Empêcher les sources d'iframe ou de Web Workers
        "form-action 'self'; "  # Limiter l'action des formulaires à l'origine du site
        "upgrade-insecure-requests;"  # Demander le passage en HTTPS si une ressource est demandée en HTTP
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
    return render_template('index.html', produits=produits)

# Page du panier
@app.route('/panier')
def panier():
    return render_template('panier.html')

# Démarrer l'application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5006))  # fallback à 5006 si local
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)

