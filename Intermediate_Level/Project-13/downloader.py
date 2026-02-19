import os
import subprocess
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from pytube import YouTube
from pytube.exceptions import PytubeError
import threading

# =======================
# Main App Class
# =======================
class YouTubeDownloader:

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - Python 3.14 Compatible")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.save_path = StringVar()
        self.url = StringVar()
        self.progress = StringVar()

        self.create_widgets()

    # =======================
    # UI Components
    # =======================
    def create_widgets(self):
        Label(self.root, text="YouTube Video URL:", font=("Arial", 12)).pack(pady=10)
        Entry(self.root, textvariable=self.url, width=60).pack()

        Button(self.root, text="Select Download Folder", command=self.select_folder).pack(pady=10)
        Label(self.root, textvariable=self.save_path, fg="blue").pack()

        Button(self.root, text="Download Video (MP4)", command=self.download_video).pack(pady=5)
        Button(self.root, text="Download Audio (MP3)", command=self.download_audio).pack(pady=5)

        Label(self.root, textvariable=self.progress, fg="green", font=("Arial", 12)).pack(pady=15)

    # =======================
    # Folder Selection
    # =======================
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)

    # =======================
    # Progress Function
    # =======================
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int(bytes_downloaded / total_size * 100)
        self.progress.set(f"Downloading... {percentage}%")
        self.root.update_idletasks()

    # =======================
    # Video Download
    # =======================
    def download_video(self):
        threading.Thread(target=self._download_video).start()

    def _download_video(self):
        try:
            url = self.url.get()
            path = self.save_path.get()

            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return

            if not path:
                messagebox.showerror("Error", "Please select a folder")
                return

            yt = YouTube(url, on_progress_callback=self.on_progress)

            # Progressive MP4 stream (video + audio combined)
            stream = yt.streams.filter(progressive=True, file_extension='mp4') \
                               .order_by('resolution').desc().first()

            if not stream:
                messagebox.showerror("Error", "No suitable video stream found")
                return

            self.progress.set("Starting video download...")
            out_file = stream.download(output_path=path)

            self.progress.set("Download Completed!")
            messagebox.showinfo("Success", f"Video downloaded:\n{out_file}")

        except PytubeError as e:
            messagebox.showerror("Error", f"Pytube Error: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    # =======================
    # Audio Download (MP3 using ffmpeg)
    # =======================
    def download_audio(self):
        threading.Thread(target=self._download_audio).start()

    def _download_audio(self):
        try:
            url = self.url.get()
            path = self.save_path.get()

            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return

            if not path:
                messagebox.showerror("Error", "Please select a folder")
                return

            yt = YouTube(url, on_progress_callback=self.on_progress)

            # Only audio stream
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            if not stream:
                messagebox.showerror("Error", "No suitable audio stream found")
                return

            self.progress.set("Starting audio download...")
            out_file = stream.download(output_path=path)

            # Convert to mp3 using ffmpeg CLI
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"

            subprocess.run([
                "ffmpeg", "-y", "-i", out_file, new_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            os.remove(out_file)  # Remove original downloaded file

            self.progress.set("Audio Download Completed!")
            messagebox.showinfo("Success", f"Audio downloaded:\n{new_file}")

        except PytubeError as e:
            messagebox.showerror("Error", f"Pytube Error: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Something went wrong:\n{e}")


# =======================
# Run App
# =======================
if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
