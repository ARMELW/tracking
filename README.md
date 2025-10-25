# Cup Tracking System - 3 Cup Shell Game Tracker

Un programme Python de vision par ordinateur pour suivre et prédire la position de la balle dans le jeu des 3 gobelets (shell game).

## 📚 Documentation Rapide / Quick Links

- **[🚀 Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes / Commencez en 5 minutes
- **[📖 Usage Examples](USAGE_EXAMPLES.md)** - Code examples and best practices / Exemples et bonnes pratiques
- **[🎮 Demo Script](demo.py)** - Run a synthetic video demo / Démo avec vidéo synthétique

## 🎯 Fonctionnalités

- **Capture d'écran en temps réel** : Capture une région spécifique de l'écran
- **Détection des gobelets** : Détection automatique des 3 gobelets
- **Numérotation automatique** : Chaque gobelet est numéroté (1, 2, 3)
- **Annotation de position** : Marque la dernière position connue de la balle
- **Tracking intelligent** : Suit le mouvement des gobelets avec trajectoires visuelles
- **Prédiction** : Prédit la position de la balle après le mélange

## 📋 Prérequis

- Python 3.7+
- Webcam ou accès à l'écran
- Système d'exploitation : Windows, Linux, ou macOS

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/ARMELW/tracking.git
cd tracking
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Extracteur de Frames Vidéo (Nouveau!)

Extrayez des frames individuelles à partir d'un fichier vidéo :

```bash
# Extraire tous les frames d'une vidéo
python video_to_images.py video.mp4

# Extraire avec un dossier de sortie spécifique
python video_to_images.py video.mp4 -o mes_frames/

# Extraire un frame sur 5 au format JPG
python video_to_images.py video.mp4 --step 5 --format jpg

# Extraire les frames 100 à 200
python video_to_images.py video.mp4 --start 100 --end 200

# Extraire les 50 premiers frames seulement
python video_to_images.py video.mp4 --max 50

# Extraire des frames spécifiques
python video_to_images.py video.mp4 --frames 0 10 20 30 40

# Exécuter une démo
python video_to_images_demo.py
```

### Version Standard

```bash
python cup_tracker.py
```

### Version Avancée (avec optical flow)

```bash
python advanced_tracker.py
```

### Étapes d'utilisation :

1. **Sélection de la région** : Au démarrage, sélectionnez la zone de l'écran contenant les gobelets
   - Cliquez et glissez pour créer un rectangle
   - Appuyez sur ENTRÉE pour confirmer
   - Appuyez sur ESC pour annuler

2. **Marquage de la balle** :
   - Appuyez sur `1`, `2`, ou `3` pour indiquer sous quel gobelet se trouve la balle
   - Le système commence à suivre les mouvements

3. **Observation de la prédiction** :
   - Le système affiche en rouge le gobelet prédit
   - Les trajectoires des gobelets sont affichées en couleur

4. **Contrôles** :
   - `1` : Marquer la balle sous le gobelet 1
   - `2` : Marquer la balle sous le gobelet 2
   - `3` : Marquer la balle sous le gobelet 3
   - `R` : Réinitialiser le tracking
   - `Q` : Quitter l'application

## 🎥 Vidéo de Référence / Reference Video

Voir la vidéo d'exemple du jeu des 3 gobelets:
https://github.com/user-attachments/assets/1f9d1d2c-efec-4073-b17b-f29ff46973be

## 🎮 Comment ça marche

### Détection des gobelets

Le système utilise plusieurs techniques de vision par ordinateur :
- **Détection de contours** : Identifie les formes des gobelets
- **Filtrage par taille et ratio** : Élimine les faux positifs
- **Tri spatial** : Ordonne les gobelets de gauche à droite

### Tracking

Deux méthodes de tracking sont disponibles :

1. **Version Standard** (`cup_tracker.py`) :
   - Détection de contours frame par frame
   - Historique des trajectoires
   - Suivi basique par position

2. **Version Avancée** (`advanced_tracker.py`) :
   - Optical flow (flux optique) pour un suivi précis
   - Détection basée sur les couleurs
   - Re-détection périodique pour éviter la perte de tracking

### Prédiction

Le système prédit la position de la balle en :
- Suivant le gobelet initialement marqué
- Analysant les trajectoires de mouvement
- Maintenant l'historique des positions

## 📁 Structure du projet

```
tracking/
├── README.md                    # Documentation
├── requirements.txt             # Dépendances Python
├── cup_tracker.py              # Tracker standard
├── advanced_tracker.py         # Tracker avancé avec optical flow
├── video_to_images.py          # Extracteur de frames vidéo
├── video_to_images_demo.py     # Démo de l'extracteur
├── test_tracker.py             # Tests du tracker
└── test_video_to_images.py     # Tests de l'extracteur
```

## 🔧 Configuration

### Personnalisation de la détection

Dans `cup_tracker.py`, vous pouvez ajuster :

```python
# Seuil de détection de contours
edges = cv2.Canny(blurred, 50, 150)  # Ajustez 50 et 150

# Taille minimale des gobelets
if area > 500:  # Changez 500 pour ajuster la sensibilité
```

### Personnalisation du tracking

Dans `advanced_tracker.py` :

```python
# Longueur de l'historique des trajectoires
self.position_history = {0: deque(maxlen=50), ...}  # Changez 50

# Fréquence de re-détection
if self.frame_count % 10 == 1:  # Re-détecte tous les 10 frames
```

## 🎬 Extracteur de Frames Vidéo

L'outil `video_to_images.py` permet d'extraire des frames individuelles à partir de fichiers vidéo. C'est utile pour :
- Analyser des vidéos du jeu des 3 gobelets frame par frame
- Préparer des données d'entraînement pour l'apprentissage machine
- Créer des captures d'écran à partir de vidéos
- Déboguer et améliorer les algorithmes de tracking

### Fonctionnalités

- **Extraction complète** : Tous les frames d'une vidéo
- **Extraction par pas** : Un frame sur N (ex: 1 sur 5)
- **Extraction par plage** : Frames entre deux indices
- **Frames spécifiques** : Liste de numéros de frames précis
- **Limite de frames** : Nombre maximum de frames à extraire
- **Formats supportés** : PNG (par défaut) ou JPG
- **Vidéos supportées** : MP4, AVI, MOV, et autres formats OpenCV

### Exemples d'utilisation

```bash
# Analyser une vidéo du jeu des 3 gobelets
python video_to_images.py cup_game.mp4 -o analysis_frames/

# Créer un GIF animé (extraire 1 frame sur 3)
python video_to_images.py video.mp4 --step 3 --format jpg

# Analyser seulement le moment du mélange (frames 100-300)
python video_to_images.py game.mp4 --start 100 --end 300
```

## 🐛 Dépannage

### Les gobelets ne sont pas détectés

- Assurez-vous que la région sélectionnée contient bien les 3 gobelets
- Ajustez les seuils de détection dans le code
- Vérifiez que l'éclairage est suffisant
- Essayez la version avancée avec détection par couleur

### Le tracking est imprécis

- Utilisez `advanced_tracker.py` pour un meilleur suivi
- Réduisez la vitesse de mouvement des gobelets
- Assurez-vous d'un bon contraste entre gobelets et fond

### Performance lente

- Réduisez la taille de la région de capture
- Augmentez l'intervalle de re-détection dans advanced_tracker.py
- Fermez les autres applications gourmandes en ressources

## 🎥 Exemple d'utilisation

1. Lancez le programme
2. Sélectionnez la zone de jeu avec les 3 gobelets
3. Avant le début du mélange, appuyez sur le chiffre correspondant au gobelet contenant la balle
4. Observez les trajectoires colorées pendant le mélange
5. Le système affiche en continu sa prédiction de la position de la balle

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation

## 📝 Licence

Ce projet est open source et disponible sous licence MIT.

## 👤 Auteur

ARMEL W.

## 🙏 Remerciements

- OpenCV pour les outils de vision par ordinateur
- MSS pour la capture d'écran efficace
