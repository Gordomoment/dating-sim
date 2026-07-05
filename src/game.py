import pygame
from typing import Optional
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_WHITE, COLOR_BLACK
from src.characters import CharacterManager
from src.dialogue import DialogueManager
from src.relationships import RelationshipManager
from src.scenes import SceneManager
from src.save_system import SaveManager, GameState
from src.ui import TextBox, DialogueChoiceMenu, CharacterStatus

class GameState:
    """Main game state and logic."""
    
    MAIN_MENU = "main_menu"
    IN_GAME = "in_game"
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
        self.game_state = GameState.MAIN_MENU
        
        # Game managers
        self.character_manager = CharacterManager()
        self.dialogue_manager = DialogueManager()
        self.relationship_manager = RelationshipManager()
        self.scene_manager = SceneManager()
        self.save_manager = SaveManager()
        
        # UI elements
        self.dialogue_box = TextBox(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 150)
        self.choice_menu = DialogueChoiceMenu(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 150)
        self.character_status = CharacterStatus(SCREEN_WIDTH - 200, 50, 150, 100)
        
        # Game variables
        self.current_character = None
        self.playtime = 0
        
        self.load_game_data()
    
    def load_game_data(self) -> None:
        """Load all game data (characters, dialogues, scenes)."""
        self.character_manager.load_characters('data/characters.json')
        self.dialogue_manager.load_dialogues('data/dialogues.json')
        self.scene_manager.load_scenes('data/scenes.json')
        
        # Initialize relationships for all characters
        for character in self.character_manager.get_all_characters():
            self.relationship_manager.initialize_character(character.id)
    
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
        if self.game_state == GameState.DIALOGUE:
            self.choice_menu.handle_click(pos)
    
    def handle_key_press(self, key) -> None:
        """Handle keyboard events."""
        if key == pygame.K_ESCAPE:
            if self.game_state == GameState.DIALOGUE:
                self.end_dialogue()
                self.game_state = GameState.IN_GAME
            elif self.game_state == GameState.IN_GAME:
                self.game_state = GameState.PAUSE_MENU
    
    def update(self) -> None:
        """Update game logic."""
        self.playtime += 1 / FPS
        
        if self.game_state == GameState.DIALOGUE:
            mouse_pos = pygame.mouse.get_pos()
            self.choice_menu.update(mouse_pos)
    
    def draw(self) -> None:
        """Draw game screen."""
        self.screen.fill(COLOR_WHITE)
        
        if self.game_state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GameState.IN_GAME:
            self.draw_game_scene()
        elif self.game_state == GameState.DIALOGUE:
            self.draw_dialogue_scene()
        elif self.game_state == GameState.PAUSE_MENU:
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_main_menu(self) -> None:
        """Draw main menu."""
        font = pygame.font.Font(None, 72)
        text = font.render("Dating Sim", True, COLOR_BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, 100))
        
        font_small = pygame.font.Font(None, 36)
        text_start = font_small.render("Press SPACE to Start", True, COLOR_BLACK)
        self.screen.blit(text_start, (SCREEN_WIDTH // 2 - 150, 300))
    
    def draw_game_scene(self) -> None:
        """Draw main game scene."""
        # Draw background
        font = pygame.font.Font(None, 36)
        text = font.render("Game Scene", True, COLOR_BLACK)
        self.screen.blit(text, (50, 50))
    
    def draw_dialogue_scene(self) -> None:
        """Draw dialogue scene."""
        self.dialogue_box.draw(self.screen)
        self.choice_menu.draw(self.screen)
        self.character_status.draw(self.screen)
    
    def draw_pause_menu(self) -> None:
        """Draw pause menu."""
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSED - Press ESC to Resume", True, COLOR_BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    
    def start_dialogue(self, character_id: str) -> None:
        """Start dialogue with a character."""
        self.current_character = self.character_manager.get_character(character_id)
        if self.current_character:
            node = self.dialogue_manager.start_dialogue(character_id)
            if node:
                self.game_state = GameState.DIALOGUE
                self.show_dialogue_node(node)
    
    def show_dialogue_node(self, node) -> None:
        """Display a dialogue node."""
        self.dialogue_box.set_text(node.content)
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
    
    def advance_dialogue(self, choice_id: str) -> None:
        """Advance dialogue based on choice."""
        current_node = self.dialogue_manager.get_current_node()
        if current_node:
            # Apply relationship changes
            for choice in current_node.choices:
                if choice.id == choice_id:
                    if self.current_character:
                        self.relationship_manager.change_relationship(
                            self.current_character.id,
                            choice.relationship_change,
                            f"Dialogue choice: {choice.text}"
                        )
                    break
        
        next_node = self.dialogue_manager.advance_dialogue(choice_id)
        if next_node:
            self.show_dialogue_node(next_node)
        else:
            self.end_dialogue()
    
    def end_dialogue(self) -> None:
        """End current dialogue."""
        self.dialogue_manager.end_dialogue()
        self.current_character = None
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
