import webbrowser
import subprocess
import time

# Lancement du serveur Django
server = subprocess.Popen(['python', 'manage.py', 'runserver'])

# Pause pour laisser le serveur démarrer
time.sleep(2)

# Ouvrir le navigateur automatiquement
webbrowser.open('http://127.0.0.1:8000')
