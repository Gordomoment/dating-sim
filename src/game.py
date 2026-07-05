import pygame
from typing import Optional
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_WHITE, COLOR_BLACK
from src.characters import CharacterManager
from src.dialogue import DialogueManager
from src.relationships import RelationshipManager
from src.scenes import SceneManager
from src.save_system import SaveManager, GameState
from src.ui import TextBox, DialogueChoiceMenu, CharacterStatus

class GameStateEnum:
    """Main game state and logic."""
    
    MAIN_MENU = "main_menu"
    IN_GAME = "in_game"
    CHARACTER_SELECT = "character_select"
    DIALOGUE = "dialogue"
    PAUSE_MENU = "pause_menu"

class DatingSimGame:
    """Main game class."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dating Sim Framework")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameStateEnum.MAIN_MENU
        
        # Game managers
        self.character_manager = CharacterManager()
        self.dialogue_manager = DialogueManager()
        self.relationship_manager = RelationshipManager()
        self.scene_manager = SceneManager()
        self.save_manager = SaveManager()
        
        # UI elements
        self.dialogue_box = TextBox(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
        self.choice_menu = DialogueChoiceMenu(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 150)
        self.character_status = CharacterStatus(SCREEN_WIDTH - 250, 50, 200, 120)
        
        # Game variables
        self.current_character = None
        self.playtime = 0
        self.available_characters = []
        
        self.load_game_data()
    
    def load_game_data(self) -> None:
        """Load all game data (characters, dialogues, scenes)."""
        try:
            self.character_manager.load_characters('data/characters.json')
            self.dialogue_manager.load_dialogues('data/dialogues.json')
            self.scene_manager.load_scenes('data/scenes.json')
            
            # Initialize relationships for all characters
            for character in self.character_manager.get_all_characters():
                self.relationship_manager.initialize_character(character.id)
            
            self.available_characters = self.character_manager.get_all_characters()
        except Exception as e:
            print(f"Error loading game data: {e}")
    
    def handle_events(self) -> None:
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
    
    def handle_mouse_click(self, pos) -> None:
        """Handle mouse click events."""
        if self.game_state == GameStateEnum.CHARACTER_SELECT:
            self.handle_character_select_click(pos)
        elif self.game_state == GameStateEnum.DIALOGUE:
            self.choice_menu.handle_click(pos)
    
    def handle_character_select_click(self, pos) -> None:
        """Handle character selection clicks."""
        # Character buttons are drawn at y positions starting from 150
        button_height = 60
        button_spacing = 20
        button_x = SCREEN_WIDTH // 2 - 150
        button_width = 300
        
        for i, character in enumerate(self.available_characters):
            button_y = 150 + i * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                self.start_dialogue(character.id)
                break
    
    def handle_key_press(self, key) -> None:
        """Handle keyboard events."""
        if key == pygame.K_ESCAPE:
            if self.game_state == GameStateEnum.DIALOGUE:
                self.end_dialogue()
                self.game_state = GameStateEnum.CHARACTER_SELECT
            elif self.game_state == GameStateEnum.IN_GAME or self.game_state == GameStateEnum.CHARACTER_SELECT:
                self.game_state = GameStateEnum.MAIN_MENU
        elif key == pygame.K_SPACE:
            if self.game_state == GameStateEnum.MAIN_MENU:
                self.game_state = GameStateEnum.CHARACTER_SELECT
    
    def update(self) -> None:
        """Update game logic."""
        self.playtime += 1 / FPS
        
        if self.game_state == GameStateEnum.DIALOGUE:
            mouse_pos = pygame.mouse.get_pos()
            self.choice_menu.update(mouse_pos)
    
    def draw(self) -> None:
        """Draw game screen."""
        self.screen.fill(COLOR_WHITE)
        
        if self.game_state == GameStateEnum.MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GameStateEnum.CHARACTER_SELECT:
            self.draw_character_select()
        elif self.game_state == GameStateEnum.DIALOGUE:
            self.draw_dialogue_scene()
        elif self.game_state == GameStateEnum.PAUSE_MENU:
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_main_menu(self) -> None:
        """Draw main menu."""
        font_title = pygame.font.Font(None, 72)
        text = font_title.render("Dating Sim", True, COLOR_BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 180, 100))
        
        font_subtitle = pygame.font.Font(None, 36)
        text_start = font_subtitle.render("Press SPACE to Start", True, COLOR_BLACK)
        self.screen.blit(text_start, (SCREEN_WIDTH // 2 - 180, 300))
        
        font_small = pygame.font.Font(None, 24)
        text_info = font_small.render("Press ESC to Quit", True, COLOR_BLACK)
        self.screen.blit(text_info, (SCREEN_WIDTH // 2 - 100, 400))
    
    def draw_character_select(self) -> None:
        """Draw character selection screen."""
        font_title = pygame.font.Font(None, 48)
        text = font_title.render("Select a Character", True, COLOR_BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, 50))
        
        button_height = 60
        button_spacing = 20
        button_x = SCREEN_WIDTH // 2 - 150
        button_width = 300
        
        for i, character in enumerate(self.available_characters):
            button_y = 150 + i * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Draw button
            pygame.draw.rect(self.screen, (200, 200, 255), button_rect)
            pygame.draw.rect(self.screen, COLOR_BLACK, button_rect, 2)
            
            # Draw character name
            font = pygame.font.Font(None, 32)
            text = font.render(character.name, True, COLOR_BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 20)
        text_info = font_small.render("Press ESC to go back", True, COLOR_BLACK)
        self.screen.blit(text_info, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 50))
    
    def draw_dialogue_scene(self) -> None:
        """Draw dialogue scene."""
        # Draw character name at top
        font = pygame.font.Font(None, 32)
        if self.current_character:
            text = font.render(self.current_character.name, True, COLOR_BLACK)
            self.screen.blit(text, (50, 20))
        
        self.dialogue_box.draw(self.screen)
        self.choice_menu.draw(self.screen)
        self.character_status.draw(self.screen)
    
    def draw_pause_menu(self) -> None:
        """Draw pause menu."""
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSED - Press ESC to Resume", True, COLOR_BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
    
    def start_dialogue(self, character_id: str) -> None:
        """Start dialogue with a character."""
        self.current_character = self.character_manager.get_character(character_id)
        if self.current_character:
            node = self.dialogue_manager.start_dialogue(character_id)
            if node:
                self.game_state = GameStateEnum.DIALOGUE
                self.show_dialogue_node(node)
    
    def show_dialogue_node(self, node) -> None:
        """Display a dialogue node."""
        # Display character name and relationship
        if self.current_character:
            rel = self.relationship_manager.get_relationship(self.current_character.id)
            status = self._get_relationship_status(rel)
            self.character_status.set_character_info(
                self.current_character.name,
                rel,
                status
            )
        
        # Display dialogue text
        speaker = node.character if node.character else "Unknown"
        full_text = f"{speaker}: {node.content}"
        self.dialogue_box.set_text(full_text)
        
        # Display choices
        self.choice_menu.clear_choices()
        
        if node.choices:
            for choice in node.choices:
                def make_callback(choice_id):
                    def callback():
                        self.advance_dialogue(choice_id)
                    return callback
                
                self.choice_menu.add_choice(
                    choice.text,
                    make_callback(choice.id)
                )
        else:
            # If no choices, add a "Continue" button
            def continue_callback():
                self.end_dialogue()
                self.game_state = GameStateEnum.CHARACTER_SELECT
            
            self.choice_menu.add_choice("Continue", continue_callback)
    
    def advance_dialogue(self, choice_id: str) -> None:
        """Advance dialogue based on choice."""
        current_node = self.dialogue_manager.get_current_node()
        if current_node:
            # Apply relationship changes
            for choice in current_node.choices:
                if choice.id == choice_id:
                    if self.current_character:
                        rel_change = choice.relationship_change
                        self.relationship_manager.change_relationship(
                            self.current_character.id,
                            rel_change,
                            f"Dialogue choice: {choice.text}"
                        )
                        print(f"Relationship changed by {rel_change}!")
                    break
        
        next_node = self.dialogue_manager.advance_dialogue(choice_id)
        if next_node:
            self.show_dialogue_node(next_node)
        else:
            self.end_dialogue()
            self.game_state = GameStateEnum.CHARACTER_SELECT
    
    def end_dialogue(self) -> None:
        """End current dialogue."""
        self.dialogue_manager.end_dialogue()
        self.current_character = None
    
    def _get_relationship_status(self, relationship: int) -> str:
        """Get relationship status label."""
        if relationship >= 75:
            return "Romantic Interest"
        elif relationship >= 50:
            return "Close"
        elif relationship >= 20:
            return "Friend"
        elif relationship > 0:
            return "Acquaintance"
        elif relationship == 0:
            return "Neutral"
        else:
            return "Disliked"
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
