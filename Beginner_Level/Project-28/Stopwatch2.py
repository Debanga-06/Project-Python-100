"""
Simple Stopwatch Application
Demonstrates: Time Module, GUI (tkinter), Control Flow
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time


class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Stopwatch")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Stopwatch state variables
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_count = 0
        self.laps = []
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Create and configure GUI elements"""
        
        # Title Label
        title_label = tk.Label(
            self.root,
            text="⏱️ STOPWATCH",
            font=('Helvetica', 16, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Time Display Frame
        display_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=3)
        display_frame.pack(pady=15, padx=20, fill=tk.BOTH)
        
        self.time_label = tk.Label(
            display_frame,
            text="00:00:00.00",
            font=('Digital-7', 48, 'bold'),
            bg='#34495e',
            fg='#3498db'
        )
        self.time_label.pack(pady=20)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # Start/Stop Button
        self.start_stop_btn = tk.Button(
            button_frame,
            text="START",
            command=self.start_stop,
            font=('Helvetica', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.start_stop_btn.grid(row=0, column=0, padx=5)
        
        # Lap Button
        self.lap_btn = tk.Button(
            button_frame,
            text="LAP",
            command=self.record_lap,
            font=('Helvetica', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.lap_btn.grid(row=0, column=1, padx=5)
        
        # Reset Button
        self.reset_btn = tk.Button(
            button_frame,
            text="RESET",
            command=self.reset,
            font=('Helvetica', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.reset_btn.grid(row=0, column=2, padx=5)
        
        # Lap Times Frame
        lap_frame = tk.LabelFrame(
            self.root,
            text="Lap Times",
            font=('Helvetica', 10, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1',
            relief=tk.GROOVE,
            bd=2
        )
        lap_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar for lap times
        scrollbar = tk.Scrollbar(lap_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for lap times
        self.lap_listbox = tk.Listbox(
            lap_frame,
            font=('Courier', 10),
            bg='#34495e',
            fg='#ecf0f1',
            selectbackground='#3498db',
            yscrollcommand=scrollbar.set,
            height=4
        )
        self.lap_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.lap_listbox.yview)
        
    def format_time(self, seconds):
        """Format time in HH:MM:SS.CS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centiseconds = int((seconds % 1) * 100)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"
    
    def update_time(self):
        """Update the time display"""
        if self.running:
            # Calculate elapsed time
            current_time = time.time()
            self.elapsed_time = (current_time - self.start_time)
            
            # Update display
            formatted_time = self.format_time(self.elapsed_time)
            self.time_label.config(text=formatted_time)
            
            # Schedule next update (every 10ms for smooth display)
            self.root.after(10, self.update_time)
    
    def start_stop(self):
        """Toggle between start and stop states"""
        if not self.running:
            # Start the stopwatch
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_stop_btn.config(text="STOP", bg='#c0392b')
            self.lap_btn.config(state=tk.NORMAL)
            self.update_time()
        else:
            # Stop the stopwatch
            self.running = False
            self.start_stop_btn.config(text="START", bg='#27ae60')
            self.lap_btn.config(state=tk.DISABLED)
    
    def record_lap(self):
        """Record a lap time"""
        if self.running:
            self.lap_count += 1
            lap_time = self.elapsed_time
            
            # Calculate split time (time since last lap)
            if self.laps:
                split_time = lap_time - self.laps[-1]
            else:
                split_time = lap_time
            
            self.laps.append(lap_time)
            
            # Format lap information
            lap_info = f"Lap {self.lap_count}: {self.format_time(lap_time)} (Split: {self.format_time(split_time)})"
            
            # Add to listbox
            self.lap_listbox.insert(tk.END, lap_info)
            self.lap_listbox.see(tk.END)  # Auto-scroll to bottom
    
    def reset(self):
        """Reset the stopwatch to initial state"""
        # Confirm reset if stopwatch is running
        if self.running:
            response = messagebox.askyesno(
                "Confirm Reset",
                "Stopwatch is running. Are you sure you want to reset?"
            )
            if not response:
                return
        
        # Reset all variables
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_count = 0
        self.laps = []
        
        # Reset display
        self.time_label.config(text="00:00:00.00")
        self.start_stop_btn.config(text="START", bg='#27ae60')
        self.lap_btn.config(state=tk.DISABLED)
        
        # Clear lap times
        self.lap_listbox.delete(0, tk.END)
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


def main():
    """Main function to run the stopwatch application"""
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    stopwatch.run()


if __name__ == "__main__":
    main()