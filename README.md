A 2D side-scrolling platformer built with Python and Pygame that demonstrates core game-development concepts such as real-time game loops, sprite animation, collision detection, and level progression. The player runs through multiple levels, avoids obstacles, and collects coins and boosts while scores and progress are stored persistently.
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

## Gameplay Flow

<table>
<tr>

<td align="center">
<img src="Game Flow/step1.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step2.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step3.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step4.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step5.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step6.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step7.png" width="160">
</td>
<td align="center"><b>→</b></td>

<td align="center">
<img src="Game Flow/step8.png" width="160">
</td>

</tr>
</table>

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

