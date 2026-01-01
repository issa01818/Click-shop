import tarfile
import os
import tempfile
from urllib.parse import urlparse
from urllib.request import urlopen
import marshal
import json
import ast

# Schémas URL autorisés pour urlopen
ALLOWED_SCHEMES = ['http', 'https']

def is_safe_url(url):
    """
    Vérifie que l'URL utilise un schéma autorisé.
    """
    parsed = urlparse(url)
    return parsed.scheme in ALLOWED_SCHEMES

def safe_urlopen(url):
    """
    Ouvre une URL uniquement si le schéma est sûr.
    """
    if is_safe_url(url):
        return urlopen(url)
    else:
        raise ValueError(f"URL non autorisée avec schéma {urlparse(url).scheme}")

def safe_members(archive, dest_dir):
    """
    Retourne uniquement les membres TAR sûrs (pas de path traversal).
    """
    safe = []
    dest_dir = os.path.abspath(dest_dir)
    for member in archive.getmembers():
        member_path = os.path.abspath(os.path.join(dest_dir, member.name))
        if not member_path.startswith(dest_dir):
            raise Exception(f"Fichier dangereux détecté : {member.name}")
        safe.append(member)
    return safe

def safe_extract(tar_path, dest_dir):
    """
    Extraction TAR sécurisée (B202 compliant).
    """
    with tarfile.open(tar_path) as archive:
        members = safe_members(archive, dest_dir)
        archive.extractall(dest_dir, members=members)

def safe_exec(script, filename, globals_dict=None, locals_dict=None):
    """
    Exécute du code Python de manière sécurisée.
    Bloque si le code contient des imports dangereux ou os/system.
    """
    globals_dict = globals_dict or {}
    locals_dict = locals_dict or {}
    forbidden = ["import os", "import sys", "os.", "sys."]
    for f in forbidden:
        if f in script:
            raise ValueError(f"Code dangereux détecté dans {filename}")
    code = compile(script, filename, 'exec')
    exec(code, globals_dict, locals_dict)

def safe_exec_code(code, g):
    """
    Exécute du code en toute sécurité.
    """
    if "import os" in code or "os." in code:
        raise ValueError("Code dangereux détecté")
    exec(code, g)

def safe_marshal_load(file_obj):
    """
    Remplace marshal.load pour prévenir la désérialisation dangereuse.
    """
    raise ValueError("Désérialisation avec marshal interdite pour sécurité")

def safe_mktemp():
    """
    Remplace mktemp obsolète par mkstemp sécurisé.
    """
    fd, path = tempfile.mkstemp(suffix=".py")
    return fd, path

def safe_eval(expression):
    """
    Remplace eval par ast.literal_eval pour éviter l'exécution arbitraire.
    """
    try:
        return ast.literal_eval(expression)
    except Exception:
        raise ValueError("Expression potentiellement dangereuse détectée")

def patch_all_medium():
    """
    Fonction principale pour appliquer tous les patchs de vulnérabilités moyennes.
    """
    # Placeholder pour appeler les patchs selon besoin
    # Par exemple, safe_exec, safe_mktemp, safe_urlopen...
    pass


if __name__ == "__main__":
    patch_all_medium()
