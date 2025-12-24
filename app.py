from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Liste des produits
produits = [
    {"nom": "Casque Audio", "prix": 45, "couleur": "black", "image": "https://t3.ftcdn.net/jpg/02/41/39/06/360_F_241390620_hihddCG15N7I8HyPWUiv1eUH85D2SN9z.jpg"},
    {"nom": "Clavier Mécanique", "prix": 34, "couleur": "black", "image": "https://via.placeholder.com/150"},
    {"nom": "Souris Gamer", "prix": 67, "couleur": "red", "image": "https://via.placeholder.com/150"},
    {"nom": "Ecouteurs Sans Fils", "prix": 76, "couleur": "white", "image": "https://via.placeholder.com/150"},
    {"nom": "T-shirt Tech", "prix": 23, "couleur": "gray", "image": "https://via.placeholder.com/150"},
    {"nom": "Sac à Dos", "prix": 64, "couleur": "blue", "image": "https://via.placeholder.com/150"},
]

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html', produits=produits)

# Page du panier
@app.route('/panier')
def panier():
    # Tu peux ajouter ici le panier de l'utilisateur (en session, etc.)
    return render_template('panier.html')

# Démarrer l'application
if __name__ == '__main__':
    app.run(debug=True, port=5006)
