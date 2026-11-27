## 03 Septembre

Fait
- Lecture des événements sur l'event bus

Suite
- Générer les fichiers PDF selon le routeur key
- Sauvegarder les fichiers PDF 
- Pouvoir consulter les fichiers PDF

## 22 Octobre

Fait
- Création du README.md
- Ajout d'une classe de base pour les modèles (`BaseModel`)
- Ajout de `Event` pour les retours de l'event bus
- Ajout de `Config` pour rendre statique les variables du fichier d'environnement


## 28 Octobre

Fait
- Ajout de `Storage` pour gérer un dossier de stockage
- Ajout de `Worker` pour l'orchestration de la lecture des messages et de la génération des PDFs
- Ajout de la sauvegarde dans la classe `BaseModel`
- Création du modèle `BookingConfirmation` pour les confirmations de réservation
- Fix de l'import dans `Consumer`
- Correction de la fonction pour l'arrêt du `Consumer`

Suite
- Crée les modèles pour les entrées et sorties du service `Access`
- Mettre en place le CI/CD

## 18 Novembre

Fait
- Ajout d'un logger et des fichiers de logs
- Finalisation des modèles PDF

Suite
- Mettre en place le CI/CD

## 25 Novembre

Fait
- Ajout d'une api pour les routes `/health` `/metrics`
- Threading de l'api et le worker de l'évent bus

Suite
- Mettre en place le CI/CD

## 27 Novembre

Fait
- Ajout des routes pour télécharger un document
