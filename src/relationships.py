from typing import Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RelationshipEvent:
    """Represents a relationship change event."""
    character_id: str
    amount: int
    reason: str
    timestamp: datetime

class RelationshipManager:
    """Manages relationships between the player and characters."""
    
    def __init__(self):
        self.relationships: Dict[str, int] = {}
        self.relationship_history: Dict[str, list] = {}
    
    def initialize_character(self, character_id: str, starting_relationship: int = 0) -> None:
        """Initialize a character's relationship score."""
        self.relationships[character_id] = starting_relationship
        self.relationship_history[character_id] = []
    
    def get_relationship(self, character_id: str) -> int:
        """Get current relationship score."""
        return self.relationships.get(character_id, 0)
    
    def change_relationship(self, character_id: str, amount: int, reason: str = "") -> None:
        """Change relationship score and record the event."""
        if character_id not in self.relationships:
            self.initialize_character(character_id)
        
        self.relationships[character_id] += amount
        
        event = RelationshipEvent(
            character_id=character_id,
            amount=amount,
            reason=reason,
            timestamp=datetime.now()
        )
        self.relationship_history[character_id].append(event)
    
    def get_relationship_history(self, character_id: str) -> list:
        """Get relationship change history for a character."""
        return self.relationship_history.get(character_id, [])
    
    def get_all_relationships(self) -> Dict[str, int]:
        """Get all relationship scores."""
        return self.relationships.copy()
    
    def calculate_compatibility(self, character_id: str, player_personality: Dict[str, int]) -> float:
        """Calculate compatibility score based on personality traits."""
        # This is a simplified example
        # In a real implementation, you'd have character personality data
        compatibility_score = 0.5  # Base compatibility
        return min(1.0, compatibility_score)  # Clamp to 0-1
