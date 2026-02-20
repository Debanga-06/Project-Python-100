# 🐍 Snake Game (Python + Pygame)

A classic **Snake Game** built in Python using **Pygame**.  
This project demonstrates fundamental **game development concepts** such as event handling, rendering, collision detection, and game loops. It’s simple, interactive, and a great starting point for learning game development.

---

## 📖 Overview
In this Snake Game, the player controls a snake that moves around the screen.  
- The snake grows longer each time it eats food.  
- The game ends if the snake collides with the **border** or with itself.  
- The score is displayed at the top of the screen.  
- After losing, the player can **restart** or **quit**.  

This project is designed to be **easy to understand and extend**, making it perfect for students and beginners in game development.

---

## 🚀 Features
- **Snake Movement**: Controlled with arrow keys (`↑`, `↓`, `←`, `→`).  
- **Food Mechanics**: Randomly placed food increases snake length when eaten.  
- **Collision Detection**: Game ends if snake hits the border or itself.  
- **Border**: A green border surrounds the play area.  
- **Score Tracking**: Displays score in real time.  
- **Replay Option**: Press `C` to play again or `Q` to quit after losing.  

---

## 🛠️ Requirements
- Python **3.8+**  
- **Pygame** library  

Install pygame with:
```bash
pip install pygame
```

---

## ▶️ How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Jiban0507/snake-game.git
   ```
2. Navigate to the project folder:
   ```bash
   cd snake-game
   ```
3. Run the game:
   ```bash
   python snake_game.py
   ```

---

## 🎮 Controls
- **Arrow Keys** → Move the snake  
- **C** → Play again after losing  
- **Q** → Quit the game  

---

## 📂 Example Gameplay Flow
1. **Start**: Snake appears at the center, food spawns randomly.  
2. **During Play**: Snake grows longer as it eats food.  
3. **Game Over**: Message displayed with options to replay or quit.  

---

## 🧠 How It Works (for learners)
- **Game Loop**: Keeps the game running until quit.  
- **Event Handling**: Detects key presses for movement.  
- **Rendering**: Snake, food, border, and score are drawn each frame.  
- **Collision Detection**: Checks if snake hits border or itself.  
- **Backtracking Logic**: Snake list grows when food is eaten, shrinks when moving forward.  

---

## 👨‍💻 Author
**Jiban**  
- 🎓 Student at Brainware University, Barasat, West Bengal, India  
- 🔗 GitHub: [github.com/Jiban0507](https://github.com/Jiban0507)  

---

## 📌 Future Improvements
- Add **levels** with increasing speed.  
- Introduce **obstacles** for more challenge.  
- Add **sound effects** for eating and collisions.  
- Create a **GUI menu** for start and exit options.  
- Add **high score tracking** across sessions.  

---

## 💡 Learning Outcomes
By studying this project, you will learn:
- How to use **Pygame** for game development.  
- How to implement a **game loop**.  
- How to handle **keyboard events**.  
- How to manage **collision detection**.  
- How to structure a simple **interactive game** in Python.  
