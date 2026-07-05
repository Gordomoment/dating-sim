import json
from typing import Dict, List, Optional, Callable
from enum import Enum

class DialogueType(Enum):
    """Types of dialogue nodes."""
    TEXT = "text"
    CHOICE = "choice"
    CONDITION = "condition"
    EVENT = "event"

class DialogueNode:
    """Represents a single dialogue node."""
    
    def __init__(self, node_id: str, node_type: DialogueType, content: str = ""):
        self.id = node_id
        self.type = node_type
        self.content = content
        self.character = None  # Who is speaking
        self.choices: List['DialogueChoice'] = []
        self.next_node_id: Optional[str] = None
        self.condition: Optional[Callable] = None
        self.action: Optional[Callable] = None
        self.relationship_change = 0
        self.background = None
        self.music = None
        self.sound_effect = None
    
    def add_choice(self, choice: 'DialogueChoice') -> None:
        """Add a choice option."""
        self.choices.append(choice)
    
    def should_show(self, context: dict) -> bool:
        """Check if this node should be shown based on conditions."""
        if self.condition:
            return self.condition(context)
        return True

class DialogueChoice:
    """Represents a player dialogue choice."""
    
    def __init__(self, choice_id: str, text: str, next_node_id: str, 
                 relationship_change: int = 0, action: Optional[Callable] = None):
        self.id = choice_id
        self.text = text
        self.next_node_id = next_node_id
        self.relationship_change = relationship_change
        self.action = action
        self.condition: Optional[Callable] = None
    
    def is_available(self, context: dict) -> bool:
        """Check if this choice should be available."""
        if self.condition:
            return self.condition(context)
        return True

class DialogueTree:
    """Manages a dialogue tree for a character."""
    
    def __init__(self, character_id: str):
        self.character_id = character_id
        self.nodes: Dict[str, DialogueNode] = {}
        self.root_node_id: Optional[str] = None
    
    def add_node(self, node: DialogueNode) -> None:
        """Add a node to the tree."""
        self.nodes[node.id] = node
        if self.root_node_id is None:
            self.root_node_id = node.id
    
    def get_node(self, node_id: str) -> Optional[DialogueNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_root(self) -> Optional[DialogueNode]:
        """Get the root node."""
        if self.root_node_id:
            return self.nodes.get(self.root_node_id)
        return None
    
    def load_from_dict(self, data: dict) -> None:
        """Load dialogue tree from dictionary."""
        for node_data in data.get('nodes', []):
            node = DialogueNode(
                node_id=node_data['id'],
                node_type=DialogueType(node_data['type']),
                content=node_data.get('content', '')
            )
            node.character = node_data.get('character')
            node.next_node_id = node_data.get('next_node_id')
            node.relationship_change = node_data.get('relationship_change', 0)
            node.background = node_data.get('background')
            node.music = node_data.get('music')
            node.sound_effect = node_data.get('sound_effect')
            
            # Add choices if this is a choice node
            for choice_data in node_data.get('choices', []):
                choice = DialogueChoice(
                    choice_id=choice_data['id'],
                    text=choice_data['text'],
                    next_node_id=choice_data['next_node_id'],
                    relationship_change=choice_data.get('relationship_change', 0)
                )
                node.add_choice(choice)
            
            self.add_node(node)
        
        # Set root node
        if data.get('root_node_id'):
            self.root_node_id = data['root_node_id']

class DialogueManager:
    """Manages all dialogue trees in the game."""
    
    def __init__(self):
        self.dialogue_trees: Dict[str, DialogueTree] = {}
        self.current_tree: Optional[DialogueTree] = None
        self.current_node: Optional[DialogueNode] = None
    
    def load_dialogues(self, json_path: str) -> None:
        """Load all dialogues from JSON file."""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                for char_id, tree_data in data.items():
                    tree = DialogueTree(char_id)
                    tree.load_from_dict(tree_data)
                    self.dialogue_trees[char_id] = tree
        except FileNotFoundError:
            print(f"Dialogue file not found: {json_path}")
    
    def start_dialogue(self, character_id: str) -> Optional[DialogueNode]:
        """Start a dialogue with a character."""
        self.current_tree = self.dialogue_trees.get(character_id)
        if self.current_tree:
            self.current_node = self.current_tree.get_root()
            return self.current_node
        return None
    
    def get_current_node(self) -> Optional[DialogueNode]:
        """Get the current dialogue node."""
        return self.current_node
    
    def advance_dialogue(self, choice_id: Optional[str] = None) -> Optional[DialogueNode]:
        """Advance to the next dialogue node."""
        if not self.current_node:
            return None
        
        if choice_id and self.current_node.choices:
            # Find the chosen option
            for choice in self.current_node.choices:
                if choice.id == choice_id:
                    next_node_id = choice.next_node_id
                    break
            else:
                return None
        else:
            next_node_id = self.current_node.next_node_id
        
        if next_node_id and self.current_tree:
            self.current_node = self.current_tree.get_node(next_node_id)
            return self.current_node
        
        return None
    
    def get_available_choices(self, context: dict) -> List[DialogueChoice]:
        """Get available choices for current node."""
        if not self.current_node or not self.current_node.choices:
            return []
        return [choice for choice in self.current_node.choices if choice.is_available(context)]
    
    def end_dialogue(self) -> None:
        """End the current dialogue."""
        self.current_tree = None
        self.current_node = None
