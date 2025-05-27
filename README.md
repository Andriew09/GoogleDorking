# DorkScope

**DorkScope** est une application web développée avec **Django**, dans le cadre du projet **BlueHack AC - Hacking**.  
Elle permet de rechercher, visualiser et analyser des "Google Dorks" via une interface conviviale.

## Structure du projet
DorkScope/
├── core/ # Application principale
├── dorkscope_web/ # Réglages du projet Django
├── db.sqlite3 # Base de données SQLite
├── env/ # Environnement virtuel Python (non versionné)
├── manage.py # Commandes Django


##  Installation et exécution

1. Cloner le projet

```bash
git clone git@github.com:Andriew09/BlueHack-404BlueTeam-DorkScope.git
cd DorkScope

2. Créer un environnement virtuel Python

python -m venv env
source env/bin/activate      # Linux / macOS
env\Scripts\activate         # Windows

3. Installer les dépendances

pip install -r requirements.txt

4. Appliquer les migrations

python manage.py migrate

5. Lancer l’application

python manage.py runserver

Ensuite, ouvre ton navigateur à l’adresse suivante :
http://127.0.0.1:8000

 Auteur

    Andriew, étudiant en Sécurité Informatique

    
