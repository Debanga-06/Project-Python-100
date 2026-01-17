# Simple Stopwatch ⏱️   ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)

A feature-rich stopwatch application built with Python's tkinter GUI library. This project demonstrates time module usage, GUI programming, and control flow implementation.

## 📋 Features

### Core Functionality
- ⏯️ **Start/Stop**: Start and pause the stopwatch with a single button
- 🔄 **Reset**: Reset the stopwatch to zero
- 🏁 **Lap Times**: Record multiple lap times with split time calculations
- 🎯 **Precise Timing**: Updates every 10ms for smooth and accurate display
- 📊 **Lap History**: View all recorded laps in a scrollable list

### User Interface
- Clean and modern dark theme design
- Large, easy-to-read time display
- Color-coded buttons (Green=Start, Red=Stop/Reset, Orange=Lap)
- Scrollable lap times list
- Confirmation dialog for reset during active timing

### Time Display
- Format: `HH:MM:SS.CS` (Hours:Minutes:Seconds.Centiseconds)
- Shows lap times and split times
- Auto-scrolling lap list

## 🎓 Learning Objectives

This project demonstrates:

1. **Time Module**:
   - `time.time()` - Get current timestamp
   - Calculating elapsed time
   - Time formatting and conversion

2. **GUI Programming (tkinter)**:
   - Creating windows and widgets
   - Button controls and event handling
   - Labels, frames, and listboxes
   - Layout management with pack() and grid()
   - Widget states and configuration
   - Scrollbars and scrollable widgets

3. **Control Flow**:
   - If/else statements for state management
   - While loop simulation with `.after()` method
   - Boolean flags for state tracking
   - Conditional button states
   - Event-driven programming

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Verify tkinter Installation

```bash
python -m tkinter
```

If a small window appears, tkinter is installed correctly.

### Install tkinter (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
tkinter is included with Python by default.

## 💻 Usage

### Running the Stopwatch

Simply run the script:
```bash
python stopwatch.py
```

### Controls

1. **START Button** (Green):
   - Click to start timing
   - Changes to STOP (Red) when running
   - Click again to pause

2. **LAP Button** (Orange):
   - Records current time as a lap
   - Shows split time since last lap
   - Only enabled while stopwatch is running

3. **RESET Button** (Red):
   - Resets stopwatch to 00:00:00.00
   - Clears all lap times
   - Shows confirmation if stopwatch is running

### Keyboard Shortcuts (Optional Enhancement)

You can add these by modifying the code:
- `Space` - Start/Stop
- `L` - Record Lap
- `R` - Reset

## 📸 Screenshots

```
┌─────────────────────────────────────┐
│         ⏱️  STOPWATCH               │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │                               │  │
│  │      00:05:23.45             │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
│   [START]   [LAP]   [RESET]        │
│                                     │
│  ┌─ Lap Times ───────────────────┐ │
│  │ Lap 1: 00:01:23.45 (...)     │ │
│  │ Lap 2: 00:02:45.12 (...)     │ │
│  │ Lap 3: 00:05:23.45 (...)     │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🔧 Code Structure

### Main Components

```python
class Stopwatch:
    def __init__(self, root)          # Initialize GUI and variables
    def setup_ui(self)                # Create all GUI elements
    def format_time(self, seconds)    # Format time display
    def update_time(self)             # Update display every 10ms
    def start_stop(self)              # Toggle start/stop state
    def record_lap(self)              # Record and display lap times
    def reset(self)                   # Reset to initial state
    def run(self)                     # Start main event loop
```

### State Variables

```python
self.running = False          # Is stopwatch running?
self.start_time = 0          # When did we start?
self.elapsed_time = 0        # Total elapsed time
self.lap_count = 0           # Number of laps recorded
self.laps = []               # List of lap timestamps
```

## 🎨 Customization

### Change Colors

Modify the color scheme in `setup_ui()`:

```python
# Current theme colors
bg_main = '#2c3e50'      # Dark blue-grey
bg_display = '#34495e'   # Lighter grey
color_time = '#3498db'   # Blue
color_start = '#27ae60'  # Green
color_lap = '#f39c12'    # Orange
color_reset = '#e74c3c'  # Red
```

### Adjust Update Frequency

Change the update interval in `update_time()`:

```python
# Current: Updates every 10ms
self.root.after(10, self.update_time)

# Slower: Updates every 100ms (less CPU usage)
self.root.after(100, self.update_time)
```

### Modify Window Size

In `__init__()`:

```python
self.root.geometry("400x300")  # Width x Height
```

### Add Keyboard Shortcuts

Add this to `__init__()`:

```python
self.root.bind('<space>', lambda e: self.start_stop())
self.root.bind('l', lambda e: self.record_lap())
self.root.bind('r', lambda e: self.reset())
```

## 📚 Advanced Features to Add

Here are some ideas to extend the project:

1. **Save/Load Sessions**:
   - Export lap times to CSV
   - Save stopwatch state

2. **Sound Effects**:
   - Beep on lap recording
   - Alert when target time reached

3. **Countdown Timer Mode**:
   - Set a target time
   - Count down instead of up

4. **Statistics**:
   - Average lap time
   - Fastest/slowest lap
   - Lap time graph

5. **Themes**:
   - Light/Dark mode toggle
   - Custom color schemes

6. **Multiple Stopwatches**:
   - Run multiple timers simultaneously
   - Tabbed interface

## 🐛 Troubleshooting

### tkinter Not Found

**Error:** `ModuleNotFoundError: No module named 'tkinter'`

**Solution:** Install tkinter using the commands in the Installation section.

### Window Doesn't Appear

**Issue:** Script runs but no window appears

**Solution:**
- Check if you're in a headless environment (SSH without X11)
- Verify tkinter installation: `python -m tkinter`
- Try running with `sudo` on Linux if permission issues exist

### Time Display Not Updating

**Issue:** Time stays at 00:00:00.00

**Solution:**
- Click the START button
- Check console for error messages
- Ensure `update_time()` is being called

### Buttons Not Responding

**Issue:** Clicking buttons does nothing

**Solution:**
- Check if cursor changes to hand when hovering
- Look for errors in console
- Verify event bindings in `setup_ui()`

## 📖 Learning Resources

### Python Time Module
- [Official Python time documentation](https://docs.python.org/3/library/time.html)
- Understanding timestamps and time calculations

### tkinter GUI Programming
- [Official tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [TkDocs tutorial](https://tkdocs.com/tutorial/)
- Widget reference and examples

### Control Flow
- Conditional statements (if/elif/else)
- State management in GUI applications
- Event-driven programming concepts

## 📝 Project Files

```
stopwatch-project/
├── stopwatch.py       # Main application file
├── README.md         # This file
└── requirements.txt  # No external requirements (uses stdlib)
```

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:

- Improve the UI design
- Add more time formats
- Implement data persistence
- Create unit tests
- Add internationalization

## 📄 License

This project is open source and available for educational purposes.

## 💡 Tips for Beginners

1. **Start Simple**: Run the basic version first, then add features
2. **Experiment**: Try changing colors, sizes, and layouts
3. **Debug**: Use print statements to understand the flow
4. **Read the Code**: Comments explain each section
5. **Ask Questions**: Understanding is more important than memorizing

## 🎯 Practice Challenges

1. Add a millisecond display (3 decimal places)
2. Implement keyboard shortcuts
3. Add a "Split" button (lap without stopping)
4. Create a dark/light theme toggle
5. Export lap times to a text file
6. Add lap comparison (faster/slower indicator)

---

**Happy Timing! ⏱️✨**

Made with ❤️ for learning Python GUI programming