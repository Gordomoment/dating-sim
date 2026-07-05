from typing import Dict, List, Optional
import json

class Scene:
    """Represents a game scene."""
    
    def __init__(self, scene_id: str, name: str, background_path: str):
        self.id = scene_id
        self.name = name
        self.background_path = background_path
        self.characters_present: Dict[str, tuple] = {}  # character_id -> (x, y)
        self.music = None
        self.description = ""
        self.time_of_day = "day"  # day, evening, night
    
    def add_character(self, character_id: str, x: int, y: int) -> None:
        """Add a character to the scene."""
        self.characters_present[character_id] = (x, y)
    
    def remove_character(self, character_id: str) -> None:
        """Remove a character from the scene."""
        if character_id in self.characters_present:
            del self.characters_present[character_id]
    
    def get_character_position(self, character_id: str) -> Optional[tuple]:
        """Get a character's position in the scene."""
        return self.characters_present.get(character_id)

class SceneManager:
    """Manages all scenes in the game."""
    
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
    
    def load_scenes(self, json_path: str) -> None:
        """Load scenes from JSON file."""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                for scene_data in data.get('scenes', []):
                    scene = Scene(
                        scene_id=scene_data['id'],
                        name=scene_data['name'],
                        background_path=scene_data['background_path']
                    )
                    scene.description = scene_data.get('description', '')
                    scene.time_of_day = scene_data.get('time_of_day', 'day')
                    scene.music = scene_data.get('music')
                    self.scenes[scene.id] = scene
        except FileNotFoundError:
            print(f"Scene file not found: {json_path}")
    
    def add_scene(self, scene: Scene) -> None:
        """Add a new scene."""
        self.scenes[scene.id] = scene
    
    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get a scene by ID."""
        return self.scenes.get(scene_id)
    
    def set_current_scene(self, scene_id: str) -> bool:
        """Set the current scene."""
        scene = self.get_scene(scene_id)
        if scene:
            self.current_scene = scene
            return True
        return False
    
    def get_current_scene(self) -> Optional[Scene]:
        """Get the current scene."""
        return self.current_scene
