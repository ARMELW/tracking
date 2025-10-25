# Object Tracking System - YOLO + ByteTrack/BoT-SORT

Un programme Python de vision par ordinateur avancé pour suivre et détecter des objets en temps réel avec YOLO et des algorithmes de tracking professionnels (ByteTrack/BoT-SORT).

## 📚 Documentation Rapide / Quick Links

- **[🚀 Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes / Commencez en 5 minutes
- **[📖 Usage Examples](USAGE_EXAMPLES.md)** - Code examples and best practices / Exemples et bonnes pratiques
- **[🎮 Demo Script](demo.py)** - Run a synthetic video demo / Démo avec vidéo synthétique

## 🎯 Fonctionnalités

### 🆕 Nouveau : YOLO + ByteTrack/BoT-SORT Tracking
- **Détection YOLO** : Utilise les derniers modèles YOLO (YOLOv11) pour une détection d'objets robuste
- **ByteTrack/BoT-SORT** : Algorithmes de tracking professionnels pour un suivi précis
- **Multi-objets** : Détecte et suit plusieurs objets simultanément avec IDs uniques
- **Sélection de zone** : Capture une région spécifique de l'écran pour le tracking
- **Trajectoires visuelles** : Affiche l'historique de mouvement de chaque objet
- **Marquage d'objets** : Cliquez sur un objet pour le suivre spécifiquement

### Fonctionnalités originales (Cup Tracking)
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

### 🆕 YOLO Object Tracker (Recommandé)

**Tracking avec ByteTrack (par défaut) :**
```bash
python yolo_tracker.py
```

**Tracking avec BoT-SORT :**
```bash
python yolo_tracker.py --tracker botsort
```

**Options avancées :**
```bash
# Utiliser un modèle YOLO plus précis
python yolo_tracker.py --model yolo11m.pt --tracker bytetrack

# Ajuster les seuils de détection
python yolo_tracker.py --conf 0.3 --iou 0.5

# Voir toutes les options
python yolo_tracker.py --help
```

**Modèles YOLO disponibles :**
- `yolo11n.pt` - Nano (plus rapide, moins précis)
- `yolo11s.pt` - Small
- `yolo11m.pt` - Medium
- `yolo11l.pt` - Large
- `yolo11x.pt` - Extra Large (plus lent, très précis)

### Version Standard (Cup Tracking)

```bash
python cup_tracker.py
```

### Version Avancée (avec optical flow)

```bash
python advanced_tracker.py
```

### Étapes d'utilisation :

#### 🆕 YOLO Tracker

1. **Sélection de la région** : Au démarrage, sélectionnez la zone de l'écran à tracker
   - Cliquez et glissez pour créer un rectangle
   - Appuyez sur ENTRÉE pour confirmer
   - Appuyez sur ESC pour annuler

2. **Marquage d'un objet** :
   - Cliquez sur n'importe quel objet détecté pour le marquer
   - L'objet sera mis en surbrillance et suivi spécifiquement
   - Les trajectoires de tous les objets sont affichées en temps réel

3. **Contrôles** :
   - `Click` : Marquer un objet pour suivi spécifique
   - `R` : Réinitialiser le marquage
   - `Q` : Quitter l'application

#### Cup Tracker (Original)

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

### 🆕 YOLO + ByteTrack/BoT-SORT Tracking

Le nouveau système YOLO utilise des technologies de pointe :

1. **Détection YOLO** :
   - Utilise les modèles YOLOv11 pré-entraînés
   - Détecte automatiquement 80 classes d'objets (personnes, véhicules, animaux, etc.)
   - Haute précision et vitesse de détection

2. **ByteTrack/BoT-SORT** :
   - Algorithmes de tracking professionnels utilisés dans la compétition
   - Assignation d'IDs uniques à chaque objet détecté
   - Suivi robuste même avec occlusions partielles
   - Re-identification automatique après disparition temporaire

3. **Sélection de zone** :
   - Capture uniquement la zone d'intérêt pour optimiser les performances
   - Fonctionne avec n'importe quelle application ou jeu à l'écran

### Détection des gobelets (Original)

Le système utilise plusieurs techniques de vision par ordinateur :
- **Détection de contours** : Identifie les formes des gobelets
- **Filtrage par taille et ratio** : Élimine les faux positifs
- **Tri spatial** : Ordonne les gobelets de gauche à droite

### Tracking (Original)

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
├── README.md                 # Documentation
├── requirements.txt          # Dépendances Python
├── yolo_tracker.py           # 🆕 YOLO + ByteTrack/BoT-SORT tracker (recommandé)
├── cup_tracker.py            # Tracker standard
├── advanced_tracker.py       # Tracker avancé avec optical flow
├── test_yolo_tracker.py      # Tests pour YOLO tracker
└── test_tracker.py           # Tests pour trackers originaux
└── advanced_tracker.py      # Tracker avancé avec optical flow
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
