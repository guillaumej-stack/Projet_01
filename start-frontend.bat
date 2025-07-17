@echo off
echo 🚀 Démarrage du Frontend Reddit Agents...

cd Frontend

echo 📦 Vérification des dépendances...
if not exist "node_modules" (
    echo Installation des dépendances...
    npm install
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
)

echo 🔧 Vérification du fichier .env.local...
if not exist ".env.local" (
    echo Création du fichier .env.local...
    copy env.example .env.local
)

echo 🌐 Démarrage du serveur de développement...
echo.
echo 📋 Informations :
echo - Frontend : http://localhost:3000
echo - Backend attendu : http://localhost:8000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

npm run dev

pause 