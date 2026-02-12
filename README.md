This Python code implements a side-scrolling platformer game using the Pygame library. The game features a player character that can run, jump, and slide to avoid obstacles such as saws and spikes while collecting coins and energy boosts. The game includes multiple levels with increasing difficulty, different background themes, and a scoring system that tracks the player's progress, coins collected, and levels completed. The player must reach an endpoint flag to complete each level, with game over and level completion screens providing feedback and options to retry or advance. The game also includes a countdown timer at the start and dynamic spawning of obstacles, coins, and energy boosts to enhance gameplay.
---

## Features

- Side-scrolling camera system  
- Player actions: run, jump, slide  
- Sprite-based animation  
- Collision detection for terrain, obstacles, and collectibles  
- Dynamic obstacles (saws, spikes)  
- Collectibles: coins and energy boosts  
- Multi-level progression  
- Countdown before gameplay start  
- Score and coin persistence using file storage  
- Level completion system  
- Game-over and restart flow  

---

## Tech Stack

**Language**
- Python 3

**Library**
- Pygame

**Concepts Demonstrated**
- Real-time game loop design  
- Event handling and input processing  
- Collision detection systems  
- File handling and persistence  
- Modular code organization  
- Game state management  
- Sprite animation and rendering  

---

## Architecture Overview

The game follows a structured loop:

1. Initialize pygame and load assets  
2. Load player, level data, and obstacles  
3. Run main game loop  
4. Handle user input  
5. Update physics and collisions  
6. Render frame  
7. Check win/lose conditions  
8. Save score and progress  

Game states:
- Countdown  
- Playing  
- Level complete  
- Game over  

Persistent storage is handled through text files for scores, coins, and level data.

---



## How to Run

### 1. Clone repository
```bash
git clone https://github.com/RiyaPadwalkar/Side-Scroller-Python-Game.git
cd Side-Scroller-Python-Game
2. Install dependencies
pip install -r requirements.txt
3. Run the game
python main.py

