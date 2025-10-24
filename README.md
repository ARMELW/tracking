# Cup Tracking System - 3 Cup Shell Game Tracker

Un programme Python de vision par ordinateur pour suivre et prédire la position de la balle dans le jeu des 3 gobelets (shell game).

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
├── README.md                 # Documentation
├── requirements.txt          # Dépendances Python
├── cup_tracker.py           # Tracker standard
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
