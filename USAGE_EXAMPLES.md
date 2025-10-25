# Usage Examples / Exemples d'Utilisation

## Example 1: Using Standard Cup Tracker / Utilisation du Tracker Standard

```python
from cup_tracker import CupTracker

# Create tracker instance
tracker = CupTracker()

# Run the tracker (will prompt for screen region selection)
tracker.run()
```

## Example 2: Pre-defined Screen Region / Région d'Écran Pré-définie

```python
from cup_tracker import CupTracker

# Define screen region coordinates
screen_region = {
    "top": 100,      # Y coordinate of top-left corner
    "left": 100,     # X coordinate of top-left corner
    "width": 800,    # Width of capture region
    "height": 600    # Height of capture region
}

# Create tracker with pre-defined region
tracker = CupTracker(screen_region=screen_region)
tracker.run()
```

## Example 3: Using Advanced Tracker / Utilisation du Tracker Avancé

```python
from advanced_tracker import AdvancedCupTracker

# Create advanced tracker with optical flow
tracker = AdvancedCupTracker()
tracker.run()
```

## Example 4: Programmatic Control / Contrôle Programmatique

```python
import cv2
from cup_tracker import CupTracker

# Create tracker
tracker = CupTracker()
tracker.screen_region = {"top": 0, "left": 0, "width": 640, "height": 480}

# Process frames manually
for i in range(100):  # Process 100 frames
    frame = tracker.capture_frame()
    
    # Set ball position programmatically
    if i == 0:
        tracker.last_known_ball_position = 1  # Ball under cup 2
    
    # Annotate frame
    annotated = tracker.annotate_frame(frame)
    
    # Display or save
    cv2.imshow("Tracker", annotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

## Example 5: Custom Detection Parameters / Paramètres de Détection Personnalisés

```python
import cv2
import numpy as np
from cup_tracker import CupTracker

class CustomCupTracker(CupTracker):
    """Custom tracker with adjusted detection parameters."""
    
    def detect_cups(self, frame: np.ndarray):
        """Override with custom detection logic."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # Larger blur
        edges = cv2.Canny(blurred, 30, 100)  # Different thresholds
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cups = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 800:  # Higher minimum area
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                if 0.4 < aspect_ratio < 3.0 and w > 40 and h > 40:
                    cups.append((x, y, w, h))
        
        cups = sorted(cups, key=lambda c: c[0])
        if len(cups) > 3:
            cups = sorted(cups, key=lambda c: c[2] * c[3], reverse=True)[:3]
            cups = sorted(cups, key=lambda c: c[0])
        
        return cups

# Use custom tracker
tracker = CustomCupTracker()
tracker.run()
```

## Example 6: Save Tracking Data / Sauvegarder les Données de Tracking

```python
import json
from cup_tracker import CupTracker

tracker = CupTracker()
tracker.screen_region = {"top": 0, "left": 0, "width": 640, "height": 480}

# Track for some time and save trajectory data
tracking_data = {
    "cup_trajectories": {},
    "predictions": []
}

for i in range(200):
    frame = tracker.capture_frame()
    annotated = tracker.annotate_frame(frame)
    
    # Save trajectory data
    if i % 10 == 0:  # Save every 10 frames
        tracking_data["cup_trajectories"][i] = {
            cup_id: list(trajectory)
            for cup_id, trajectory in tracker.cup_trajectories.items()
        }
        
        prediction = tracker.predict_ball_position()
        tracking_data["predictions"].append({
            "frame": i,
            "predicted_cup": prediction
        })

# Save to file
with open("/tmp/tracking_data.json", "w") as f:
    json.dump(tracking_data, f, indent=2)

print("Tracking data saved to /tmp/tracking_data.json")
```

## Example 7: Video to Images - Extract All Frames / Extraire Tous les Frames

```python
from video_to_images import VideoToImages

# Extract all frames from a video
converter = VideoToImages("cup_game.mp4", output_dir="frames/", format="png")
num_frames = converter.extract_frames()

print(f"Extracted {num_frames} frames")
```

## Example 8: Video to Images - Extract Every Nth Frame / Extraire un Frame sur N

```python
from video_to_images import VideoToImages

# Extract every 5th frame as JPG
converter = VideoToImages(
    video_path="cup_game.mp4",
    output_dir="frames_jpg/",
    format="jpg",
    prefix="cup_frame"
)

# Extract every 5th frame
num_frames = converter.extract_frames(step=5)
print(f"Extracted {num_frames} frames")
```

## Example 9: Video to Images - Extract Frame Range / Extraire une Plage de Frames

```python
from video_to_images import VideoToImages

# Extract frames 100 to 300 (the shuffling part)
converter = VideoToImages("cup_game.mp4", output_dir="shuffle_frames/")

# Extract only the shuffling sequence
num_frames = converter.extract_frames(start_frame=100, end_frame=300)
print(f"Extracted {num_frames} frames from shuffling sequence")
```

## Example 10: Video to Images - Extract Specific Frames / Extraire des Frames Spécifiques

```python
from video_to_images import VideoToImages

# Extract specific key frames
converter = VideoToImages("cup_game.mp4", output_dir="key_frames/")

# Extract frames at specific timestamps
key_frames = [0, 30, 60, 90, 120, 150]  # Every 1 second at 30 FPS
num_frames = converter.extract_specific_frames(key_frames)
print(f"Extracted {num_frames} key frames")
```

## Example 11: Video to Images - Command Line Usage / Utilisation en Ligne de Commande

```bash
# Extract all frames
python video_to_images.py video.mp4

# Custom output directory
python video_to_images.py video.mp4 -o my_frames/

# Extract every 10th frame as JPG
python video_to_images.py video.mp4 --step 10 --format jpg

# Extract first 100 frames
python video_to_images.py video.mp4 --max 100

# Extract frames 50-150
python video_to_images.py video.mp4 --start 50 --end 150

# Extract specific frames
python video_to_images.py video.mp4 --frames 0 15 30 45 60

# Run demo
python video_to_images_demo.py
```

## Example 12: Analyze Cup Game Video Frame by Frame / Analyser une Vidéo Frame par Frame

```python
from video_to_images import VideoToImages
from cup_tracker import CupTracker
import cv2
import os

# Step 1: Extract frames from video
print("Step 1: Extracting frames...")
converter = VideoToImages("cup_game_video.mp4", output_dir="game_frames/")
num_frames = converter.extract_frames()

# Step 2: Analyze each frame with the tracker
print("Step 2: Analyzing frames...")
tracker = CupTracker(screen_region={"top": 0, "left": 0, "width": 640, "height": 480})
tracker.last_known_ball_position = 0  # Ball starts under cup 1

analysis_dir = "analyzed_frames/"
os.makedirs(analysis_dir, exist_ok=True)

frame_files = sorted([f for f in os.listdir("game_frames/") if f.endswith('.png')])

for i, frame_file in enumerate(frame_files):
    # Load frame
    frame = cv2.imread(os.path.join("game_frames/", frame_file))
    
    # Analyze with tracker
    annotated = tracker.annotate_frame(frame)
    
    # Save annotated frame
    output_path = os.path.join(analysis_dir, f"analyzed_{frame_file}")
    cv2.imwrite(output_path, annotated)
    
    if (i + 1) % 10 == 0:
        print(f"Analyzed {i + 1}/{len(frame_files)} frames...")

print(f"\nAnalysis complete! Check {analysis_dir}/ for annotated frames")
```

## Tips for Best Results / Conseils pour Meilleurs Résultats

### 1. Screen Capture Setup / Configuration de Capture d'Écran
- Make sure the cups are clearly visible in the selected region
- Use good lighting conditions
- Minimize background clutter
- Assurez-vous que les gobelets sont clairement visibles
- Utilisez un bon éclairage
- Minimisez l'encombrement de l'arrière-plan

### 2. Marking Ball Position / Marquer la Position de la Balle
- Mark the ball position BEFORE the shuffling starts
- Press the number key (1, 2, or 3) corresponding to the cup with the ball
- Marquez la position AVANT le début du mélange
- Appuyez sur le chiffre (1, 2, ou 3) correspondant au gobelet avec la balle

### 3. Tracking Performance / Performance du Tracking
- For fast movements, use the advanced tracker
- Adjust detection thresholds if cups aren't detected
- Use good contrast between cups and background
- Pour mouvements rapides, utilisez le tracker avancé
- Ajustez les seuils si les gobelets ne sont pas détectés
- Utilisez un bon contraste entre gobelets et fond

### 4. Testing / Tests
- Test with slow movements first
- Gradually increase speed as tracking improves
- Watch trajectory lines to verify tracking
- Testez d'abord avec mouvements lents
- Augmentez progressivement la vitesse
- Observez les lignes de trajectoire pour vérifier le suivi
