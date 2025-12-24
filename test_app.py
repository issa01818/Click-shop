import pytest
from app import app  # Import de ton application Flask

# Test si l'application charge correctement
def test_index():
    client = app.test_client()  # Crée un client de test pour simuler les requêtes HTTP
    response = client.get('/')  # Envoie une requête GET sur la page d'accueil
    assert response.status_code == 200  # Vérifie si le code de statut HTTP est 200 (OK)

# Test si la page Panier se charge correctement
def test_panier():
    client = app.test_client()
    response = client.get('/panier')
    assert response.status_code == 200
