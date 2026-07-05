import pygame
from typing import List, Tuple, Optional, Callable
from config import (
    FONT_SIZE_DIALOGUE, FONT_SIZE_CHOICE, FONT_SIZE_UI,
    COLOR_WHITE, COLOR_BLACK, COLOR_TEXT, COLOR_CHOICE_BG, 
    COLOR_CHOICE_HOVER, SCREEN_WIDTH, SCREEN_HEIGHT
)

class UIElement:
    """Base class for UI elements."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the UI element."""
        pass
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle mouse click. Return True if clicked."""
        return self.rect.collidepoint(pos)

class TextBox(UIElement):
    """Displays text with word wrapping."""
    
    def __init__(self, x: int, y: int, width: int, height: int, font_size: int = FONT_SIZE_DIALOGUE):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text = ""
        self.text_color = COLOR_TEXT
        self.bg_color = COLOR_WHITE
        self.padding = 10
    
    def set_text(self, text: str) -> None:
        """Set the text to display."""
        self.text = text
    
    def wrap_text(self) -> List[str]:
        """Wrap text to fit the box width."""
        words = self.text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_width = self.font.size(test_line)[0]
            
            if text_width > self.width - self.padding * 2:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the text box."""
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        
        lines = self.wrap_text()
        y_offset = self.y + self.padding
        
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.x + self.padding, y_offset))
            y_offset += self.font.get_height() + 5

class Button(UIElement):
    """Clickable button UI element."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 callback: Optional[Callable] = None, font_size: int = FONT_SIZE_CHOICE):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.bg_color = COLOR_CHOICE_BG
        self.hover_color = COLOR_CHOICE_HOVER
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update button hover state."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle mouse click."""
        if self.rect.collidepoint(pos):
            if self.callback:
                self.callback()
            return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button."""
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class DialogueChoiceMenu(UIElement):
    """Menu for displaying dialogue choices."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.choices: List[Button] = []
        self.button_height = 50
        self.button_spacing = 10
    
    def add_choice(self, text: str, callback: Callable) -> None:
        """Add a choice button."""
        y_pos = self.y + len(self.choices) * (self.button_height + self.button_spacing)
        button = Button(
            self.x, y_pos, self.width, self.button_height,
            text, callback, FONT_SIZE_CHOICE
        )
        self.choices.append(button)
    
    def clear_choices(self) -> None:
        """Clear all choices."""
        self.choices = []
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update all choice buttons."""
        for choice in self.choices:
            choice.update(mouse_pos)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle click on any choice."""
        for choice in self.choices:
            if choice.handle_click(pos):
                return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all choice buttons."""
        for choice in self.choices:
            choice.draw(surface)

class CharacterStatus(UIElement):
    """Displays character status and relationship information."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, FONT_SIZE_UI)
        self.character_name = ""
        self.relationship_level = 0
        self.status_text = ""
    
    def set_character_info(self, name: str, relationship: int, status: str) -> None:
        """Set character information to display."""
        self.character_name = name
        self.relationship_level = relationship
        self.status_text = status
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw character status."""
        pygame.draw.rect(surface, COLOR_WHITE, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 1)
        
        name_text = self.font.render(self.character_name, True, COLOR_TEXT)
        surface.blit(name_text, (self.x + 10, self.y + 10))
        
        status_text = self.font.render(f"Status: {self.status_text}", True, COLOR_TEXT)
        surface.blit(status_text, (self.x + 10, self.y + 35))
        
        rel_text = self.font.render(f"Relationship: {self.relationship_level}", True, COLOR_TEXT)
        surface.blit(rel_text, (self.x + 10, self.y + 60))
