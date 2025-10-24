# Quick Start Guide / Guide de Démarrage Rapide

## English

### 5-Minute Setup

1. **Install Python** (3.7 or higher)
   ```bash
   python3 --version  # Should show 3.7+
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/ARMELW/tracking.git
   cd tracking
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the tracker**
   ```bash
   python3 cup_tracker.py
   ```

### First Use

1. **Select Region**
   - When the program starts, it will show your full screen
   - Click and drag to select the area with the 3 cups
   - Press ENTER to confirm

2. **Mark the Ball**
   - Before shuffling starts, press `1`, `2`, or `3` to mark which cup has the ball
   - The number corresponds to the cup position (left=1, middle=2, right=3)

3. **Watch the Prediction**
   - As cups move, you'll see colored trajectory lines
   - The predicted cup will be highlighted in red
   - The system shows "Ball -> Cup #X" at the top

4. **Controls**
   - `Q`: Quit
   - `R`: Reset tracking
   - `1/2/3`: Mark ball position

---

## Français

### Configuration en 5 Minutes

1. **Installer Python** (3.7 ou plus)
   ```bash
   python3 --version  # Devrait afficher 3.7+
   ```

2. **Cloner le dépôt**
   ```bash
   git clone https://github.com/ARMELW/tracking.git
   cd tracking
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer le tracker**
   ```bash
   python3 cup_tracker.py
   ```

### Première Utilisation

1. **Sélectionner la Région**
   - Au démarrage, le programme affiche votre écran complet
   - Cliquez et glissez pour sélectionner la zone avec les 3 gobelets
   - Appuyez sur ENTRÉE pour confirmer

2. **Marquer la Balle**
   - Avant le début du mélange, appuyez sur `1`, `2`, ou `3` pour marquer le gobelet avec la balle
   - Le numéro correspond à la position (gauche=1, milieu=2, droite=3)

3. **Observer la Prédiction**
   - Pendant le mouvement, vous verrez des lignes de trajectoire colorées
   - Le gobelet prédit sera surligné en rouge
   - Le système affiche "Ball -> Cup #X" en haut

4. **Contrôles**
   - `Q`: Quitter
   - `R`: Réinitialiser le suivi
   - `1/2/3`: Marquer la position de la balle

---

## Troubleshooting / Dépannage

### Problem: "Module not found"
**Solution:** Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "No screen region selected"
**Solution:** You must select a region when prompted. Press ENTER after selecting.

### Problem: Cups not detected
**Solution:** 
- Ensure good lighting
- Make sure cups are clearly visible
- Try the advanced tracker: `python3 advanced_tracker.py`

### Problème: "Module introuvable"
**Solution:** Assurez-vous d'avoir installé les dépendances:
```bash
pip install -r requirements.txt
```

### Problème: "Aucune région d'écran sélectionnée"
**Solution:** Vous devez sélectionner une région. Appuyez sur ENTRÉE après sélection.

### Problème: Gobelets non détectés
**Solution:**
- Assurez un bon éclairage
- Vérifiez que les gobelets sont clairement visibles
- Essayez le tracker avancé: `python3 advanced_tracker.py`

---

## Video Tutorial / Tutoriel Vidéo

For a visual guide, check the video linked in the issue:
https://github.com/user-attachments/assets/1f9d1d2c-efec-4073-b17b-f29ff46973be

Pour un guide visuel, consultez la vidéo liée dans l'issue.

---

## Next Steps / Prochaines Étapes

- Read the full [README.md](README.md) for detailed documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for advanced usage
- Run tests: `python3 test_tracker.py`

- Lisez le [README.md](README.md) complet pour la documentation détaillée
- Consultez [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) pour l'utilisation avancée
- Lancez les tests: `python3 test_tracker.py`
