# 🎮 Hangman Game (Python)

## 📌 Overview
**Hangman Game** is a Python-based word guessing game with a **graphical interface** built using `Tkinter`.  
Players try to guess a random word **letter by letter**. Wrong guesses are limited to 6. The game resets automatically after a win or loss.

This project demonstrates **Python game logic, file I/O, and GUI programming**, making it suitable for beginners, learning projects, and demo purposes.

---

## ✨ Features
- **Random Word Selection** → Words are loaded dynamically from `words.txt`.  
- **Letter-by-Letter Guessing** → Players can input letters using the **Enter key** or **Guess Button**.  
- **Remaining Attempts Display** → Tracks wrong guesses visually in the GUI.  
- **Automatic Game Reset** → New random word is loaded after win or loss.  
- **Clue-Free Gameplay** → No hints are provided, making the game challenging.  
- **Professional GUI** → Clean, intuitive interface using `Tkinter`.  
- **Cross-Platform** → Works on Windows, Linux, and macOS.  

---

## 💻 Supported Platforms
- **Windows** → Tested on Windows 10/11  
- **Linux** → Ubuntu, Fedora  
- **macOS** → Catalina, Big Sur  
- Requires **Python 3.x** with Tkinter (standard library)

---

## 📦 Requirements
No external libraries are needed. Uses standard Python libraries:  
- `tkinter` → GUI  
- `random` → Word selection  
- `os` → File I/O  
- `messagebox` → Alerts  

Install Python (if not installed) from [https://www.python.org](https://www.python.org)  

---

## ▶️ Usage
1. Clone or download the repository.  
2. Ensure `words.txt` exists. If missing, the program creates it with default words.  
3. Run the game from terminal or command prompt:

```bash
python hangman.py
````

4. Enter a letter in the Entry box and press **Enter** or click **Guess**.
5. Continue guessing until you either guess all letters correctly or reach 6 wrong attempts.

---

## 📂 Project Structure

```
📁 Hangman-Game
 ┣ 📄 README.md           # Project documentation
 ┣ 📄 hangman.py          # Main Python script
 ┣ 📄 words.txt           # Word list for guessing
```

---

## 🚀 Future Improvements

* **Graphical Hangman Figure** → Show step-by-step drawing for wrong guesses.
* **Sound Effects** → Add audio for correct/incorrect guesses and win/loss.
* **Letter History** → Display letters already guessed.
* **Word Categories** → Easy, Medium, Hard categories for better gameplay.
* **Hint System (Optional)** → Provide optional clues or word definitions.
* **Custom Word Lists** → Allow users to add their own word lists dynamically.
* **Score Tracking** → Track wins, losses, and streaks.
* **Multiplayer Mode** → Two-player word input and guessing mode.
* **GUI Enhancements** → Colors, fonts, animations for a polished look.
* **Save & Load** → Save current game progress and resume later.
* **Mobile/Browser Version** → Convert GUI to web-based or mobile-friendly interface.

---

## 👨‍💻 Author

Developed by **Jiban Maji**
📍 Brainware University, Barasat, West Bengal, India

GitHub Profile: [https://github.com/Jiban0507](https://github.com/Jiban0507)

---

## 📝 Notes

* The game is **beginner-friendly** but provides challenge with clue-free guessing.
* Words are case-insensitive.
* Python 3.x recommended. Tkinter must be installed (comes with standard Python).
