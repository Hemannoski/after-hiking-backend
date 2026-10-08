# After Hiking CI 🇮🥾

**After Hiking** est une plateforme communautaire dédiée aux randonneurs en Côte d'Ivoire.
Ce dépôt contient le **Backend API** (développé avec Django) qui alimente l'application mobile, ainsi que le tableau de bord d'administration.

## 🚀 Stack Technique

*   **Langage :** Python 3.13
*   **Framework :** Django 6.1 + Django REST Framework
*   **Base de données :** PostgreSQL 18
*   **Authentification :** Firebase Auth (liée via `firebase_uid`)
*   **Documentation API :** drf-spectacular (OpenAPI/Swagger)
*   **Outils :** Django Debug Toolbar, python-decouple

##  Fonctionnalités Principales

*   **Gestion des utilisateurs :** Profils, abonnements, blocages (liés à Firebase).
*   **Randonnées & Médias :** Publication de récits, upload de photos/vidéos (R2/Mux).
*   **Social :** Likes, commentaires, fil d'actualité personnalisé.
*   **IA & Prédictions :** Estimation de la portée d'une publication avant envoi (Random Forest).
*   **Modération :** Système de signalement et administration via Django Admin.

## 🛠️ Installation et Démarrage

### 1. Prérequis
*   Python 3.13+
*   PostgreSQL 18 installé et démarré

### 2. Cloner et configurer l'environnement
```powershell
# Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt