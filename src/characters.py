import json
from typing import Dict, List, Optional

class Character:
    """Represents a character in the dating sim."""
    
    def __init__(self, char_id: str, name: str, age: int, description: str, 
                 personality_traits: Dict[str, int], appearance_path: str):
        self.id = char_id
        self.name = name
        self.age = age
        self.description = description
        self.personality_traits = personality_traits  # e.g., {"kindness": 7, "humor": 5}
        self.appearance_path = appearance_path
        self.relationship = 0  # -100 to 100
        self.is_available = True
        self.events_seen = set()
        self.dialogue_count = 0
        
    def add_relationship(self, amount: int) -> None:
        """Increase or decrease relationship score."""
        from config import RELATIONSHIP_MIN, RELATIONSHIP_MAX
        self.relationship = max(RELATIONSHIP_MIN, min(RELATIONSHIP_MAX, self.relationship + amount))
    
    def get_relationship_status(self) -> str:
        """Get current relationship status label."""
        from config import RELATIONSHIP_THRESHOLD_FRIEND, RELATIONSHIP_THRESHOLD_CLOSE, RELATIONSHIP_THRESHOLD_ROMANTIC
        
        if self.relationship >= RELATIONSHIP_THRESHOLD_ROMANTIC:
            return "Romantic Interest"
        elif self.relationship >= RELATIONSHIP_THRESHOLD_CLOSE:
            return "Close"
        elif self.relationship >= RELATIONSHIP_THRESHOLD_FRIEND:
            return "Friend"
        elif self.relationship > 0:
            return "Acquaintance"
        elif self.relationship == 0:
            return "Neutral"
        else:
            return "Disliked"
    
    def mark_event_seen(self, event_id: str) -> None:
        """Mark an event as seen."""
        self.events_seen.add(event_id)
    
    def has_seen_event(self, event_id: str) -> bool:
        """Check if event has been seen."""
        return event_id in self.events_seen
    
    def to_dict(self) -> dict:
        """Convert character to dictionary for saving."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "description": self.description,
            "personality_traits": self.personality_traits,
            "appearance_path": self.appearance_path,
            "relationship": self.relationship,
            "is_available": self.is_available,
            "events_seen": list(self.events_seen),
            "dialogue_count": self.dialogue_count
        }


class CharacterManager:
    """Manages all characters in the game."""
    
    def __init__(self):
        self.characters: Dict[str, Character] = {}
    
    def load_characters(self, json_path: str) -> None:
        """Load characters from JSON file."""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                for char_data in data.get('characters', []):
                    character = Character(
                        char_id=char_data['id'],
                        name=char_data['name'],
                        age=char_data['age'],
                        description=char_data['description'],
                        personality_traits=char_data['personality_traits'],
                        appearance_path=char_data['appearance_path']
                    )
                    self.characters[character.id] = character
        except FileNotFoundError:
            print(f"Character file not found: {json_path}")
    
    def get_character(self, char_id: str) -> Optional[Character]:
        """Get a character by ID."""
        return self.characters.get(char_id)
    
    def get_all_characters(self) -> List[Character]:
        """Get all characters."""
        return list(self.characters.values())
    
    def get_available_characters(self) -> List[Character]:
        """Get all available characters."""
        return [c for c in self.characters.values() if c.is_available]
    
    def add_character(self, character: Character) -> None:
        """Add a new character."""
        self.characters[character.id] = character
