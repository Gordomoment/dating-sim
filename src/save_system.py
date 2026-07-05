import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class GameState:
    """Represents the complete game state for saving/loading."""
    
    def __init__(self):
        self.playtime = 0  # in seconds
        self.current_scene_id = None
        self.characters_data = {}
        self.player_choices = []
        self.achievements = []
        self.save_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary."""
        return {
            "playtime": self.playtime,
            "current_scene_id": self.current_scene_id,
            "characters_data": self.characters_data,
            "player_choices": self.player_choices,
            "achievements": self.achievements,
            "save_time": self.save_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create game state from dictionary."""
        state = cls()
        state.playtime = data.get('playtime', 0)
        state.current_scene_id = data.get('current_scene_id')
        state.characters_data = data.get('characters_data', {})
        state.player_choices = data.get('player_choices', [])
        state.achievements = data.get('achievements', [])
        state.save_time = data.get('save_time', datetime.now().isoformat())
        return state

class SaveManager:
    """Manages game saves and loads."""
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        self.auto_save_slot = "autosave.json"
        self.max_saves = 10
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, game_state: GameState, slot_name: str = None) -> bool:
        """Save game to file."""
        try:
            if slot_name is None:
                file_path = os.path.join(self.save_dir, self.auto_save_slot)
            else:
                file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            
            with open(file_path, 'w') as f:
                json.dump(game_state.to_dict(), f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot_name: str = None) -> Optional[GameState]:
        """Load game from file."""
        try:
            if slot_name is None:
                file_path = os.path.join(self.save_dir, self.auto_save_slot)
            else:
                file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return GameState.from_dict(data)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def get_save_files(self) -> list:
        """Get list of available save files."""
        save_files = []
        try:
            for filename in os.listdir(self.save_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(self.save_dir, filename)
                    save_time = os.path.getmtime(file_path)
                    save_files.append({
                        "filename": filename,
                        "save_time": save_time
                    })
        except Exception as e:
            print(f"Error reading save files: {e}")
        
        return sorted(save_files, key=lambda x: x['save_time'], reverse=True)
    
    def delete_save(self, slot_name: str) -> bool:
        """Delete a save file."""
        try:
            file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting save: {e}")
        
        return False
