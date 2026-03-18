import pygame
import os
from tkinter import *

# Initialize pygame mixer
pygame.mixer.init()

# GUI setup
root = Tk()
root.title("Music Player")
root.geometry("400x300")

# Playlist
playlist = os.listdir("song")

current_song = StringVar()
current_song.set("No song selected")

# Functions
def play_music():
    song = listbox.get(ACTIVE)
    pygame.mixer.music.load(f"songs/{song}")
    pygame.mixer.music.play()
    current_song.set(song)

def stop_music():
    pygame.mixer.music.stop()
    current_song.set("Stopped")

# UI Elements
label = Label(root, textvariable=current_song)
label.pack(pady=10)

listbox = Listbox(root)
for song in playlist:
    listbox.insert(END, song)
listbox.pack()

play_btn = Button(root, text="Play", command=play_music)
play_btn.pack(pady=5)

stop_btn = Button(root, text="Stop", command=stop_music)
stop_btn.pack(pady=5)

root.mainloop()