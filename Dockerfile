# Utiliser l'image officielle Python comme image de base
FROM python:3.9-slim

# Définir un répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /app/

# Installer les dépendances Python à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le répertoire de travail
COPY . /app/

# Exposer le port 5006
EXPOSE 5006

# Commande par défaut pour démarrer l'application
CMD ["python", "app.py"]

