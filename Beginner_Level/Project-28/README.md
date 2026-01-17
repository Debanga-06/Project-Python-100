# Stopwatch with History

A simple GUI-based stopwatch application built with Python's Tkinter. It allows you to start, stop, and reset the timer, and keeps a history of up to 10 recorded times using a First-In-First-Out (FIFO) queue.

## Features

- **Start/Stop/Reset**: Control the stopwatch timer.
- **Time Display**: Shows elapsed time in MM:SS:MS format (minutes:seconds:milliseconds).
- **History Tracking**: Automatically saves the time when stopped, storing up to 10 entries (oldest are removed first).
- **Save History Manually**: Button to save the current time to history.
- **Clear History**: Remove all saved times.
- **GUI Interface**: User-friendly buttons and labels.

## Requirements

- Python 3.x with Tkinter (Tkinter is included in most Python installations).

## How to Run

1. Ensure Python is installed.
2. Run the `Stopwatch.py` script:
   ```
   python Stopwatch.py
   ```
3. The GUI window will open. Use the buttons to control the stopwatch.

## Usage

- Click **Start** to begin timing.
- Click **Stop** to pause and auto-save the time to history.
- Click **Reset** to reset the timer to 00:00:00.
- Click **Save History** to manually add the current time to history.
- Click **Clear History** to empty the history list.
- The history is displayed below the buttons, showing the last 10 saved times.

## Example

1. Start the app.
2. Click Start, wait a few seconds, click Stop → Time is saved to history.
3. Repeat to build a list of times.
4. View the history in the GUI.

## Notes

- History uses a FIFO queue (deque with maxlen=10), so only the most recent 10 times are kept.
- Times are saved in MM:SS:MS format.
- The app runs in a window; close the window to exit.