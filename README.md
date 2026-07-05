# Dating Sim Framework

A modular dating simulation game framework built with Python and Pygame. This project provides the core mechanics for building interactive visual novels and dating simulations.

## Features

- **Character Management** - Create and manage characters with personality traits, relationship stats, and dialogue
- **Dialogue System** - Branching dialogue trees with conditional paths based on player choices
- **Relationship Tracking** - Dynamic relationship system that changes based on player interactions
- **Save/Load System** - Persist game state across sessions
- **Visual Novel Engine** - Render scenes, characters, and UI elements
- **Event System** - Trigger events based on relationship levels and choices
- **Music & Sound** - Background music and sound effect support

## Project Structure

```
dating-sim/
├── main.py                 # Entry point
├── config.py              # Game configuration
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   ├── game.py           # Main game loop
│   ├── characters.py     # Character class and management
│   ├── dialogue.py       # Dialogue tree system
│   ├── relationships.py  # Relationship tracking
│   ├── scenes.py         # Scene management
│   ├── ui.py             # UI elements
│   └── save_system.py    # Save/load functionality
├── assets/
│   ├── characters/       # Character images
│   ├── backgrounds/      # Background images
│   ├── music/            # Background music
│   └── sounds/           # Sound effects
├── data/
│   ├── characters.json   # Character definitions
│   ├── dialogues.json    # Dialogue trees
│   └── scenes.json       # Scene definitions
└── saves/                # Save files directory
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Creating Characters

Define characters in `data/characters.json` with personality traits and dialogue options.

## Creating Dialogues

Build dialogue trees in `data/dialogues.json` with branching paths based on player choices.

## License

MIT
