import tkinter as tk
import time
from collections import deque

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch with FIFO History")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        # FIFO queue with max length 10
        self.history = deque(maxlen=10)

        # Label to display time
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        # Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", padx=10)

        self.save_button = tk.Button(root, text="Save History", command=self.save_history)
        self.save_button.pack(side="left", padx=10)

        self.clear_button = tk.Button(root, text="Clear History", command=self.clear_history)
        self.clear_button.pack(side="left", padx=10)

        # History display
        self.history_label = tk.Label(root, text="History:\n", font=("Helvetica", 12), justify="left")
        self.history_label.pack(pady=20)

    def update_time(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            milliseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
            self.label.config(text=f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}")
            self.root.after(50, self.update_time)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_time()

    def stop(self):
        if self.running:
            self.running = False
            # Auto-save when stopped
            self.save_history()

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.label.config(text="00:00:00")

    def save_history(self):
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        milliseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
        formatted_time = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
        self.history.append(formatted_time)  # FIFO queue handles deletion automatically
        self.update_history_label()

    def clear_history(self):
        self.history.clear()
        self.update_history_label()

    def update_history_label(self):
        if self.history:
            history_text = "History:\n" + "\n".join(self.history)
        else:
            history_text = "History:\n(empty)"
        self.history_label.config(text=history_text)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()