## 📄 README.md

```markdown
# 🎥 Screen Recorder Project

## 📌 Overview
The **Screen Recorder Project** is a Python-based application that captures your computer screen and saves it as a video file (`.mp4` or `.avi`).  
It also provides advanced functionality to:
- Extract frames from the recorded video.
- Convert video formats for broader compatibility.
- Automatically create organized folders (`recordings`, `frames`) for saving outputs.

This project is designed to be **professional, scalable, and beginner-friendly**, making it ideal for both personal use and collaborative learning.

---

## ✨ Features
- **Screen Recording** → Captures everything happening on your screen in real-time and saves it as a video file.  
- **Frame Extraction** → Breaks down the recorded video into individual images (`.jpg`), useful for analysis, datasets, or thumbnails.  
- **Format Conversion** → Converts `.mp4` recordings into `.avi` format for compatibility with different players.  
- **Auto Folder Creation** → Automatically creates `recordings` and `frames` folders if they do not exist.  
- **Customizable Duration** → Users can set how long the recording should run.  

---

## 💻 Supported Platforms
- **Windows** (tested extensively)  
- **Linux**  
- **macOS**  

👉 Works on any platform that supports Python and OpenCV.

---

## 📦 Requirements
Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Main libraries used:
- `opencv-python`
- `numpy`
- `pyautogui` (basic screen capture)
- `mss` (GPU-rendered screen capture for dynamic content)

---

## ▶️ Usage
Run the project from the terminal inside the project folder:
```bash
python screen_recorder.py
```

By default:
- Screen recording runs for **10 seconds**.  
- Output video is saved at:  
  `recordings/output.mp4`  
- Extracted frames are saved at:  
  `frames/frame_*.jpg`  
- Converted video is saved at:  
  `recordings/output.avi`  

---

## ⏱️ Customizing Recording Duration
You can increase or decrease the recording time by modifying:
```python
recorder.start_recording(duration=60)  # Records for 1 minute
```

---

## 📂 Project Structure
```
📁 Screen-Recorder
 ┣ 📄 README.md
 ┣ 📄 requirements.txt
 ┣ 📄 screen_recorder.py
 ┣ 📁 recordings   # Recorded videos
 ┣ 📁 frames       # Extracted frames
 ┣ 📁 utils        # Helper scripts (future expansion)
 ┗ 📁 tests        # Test files (future expansion)
```

---

## 🚀 Future Improvements
- Add audio recording support.  
- Record specific windows or applications.  
- Build a GUI interface for easier use.  

---

## 👨‍💻 Author
Developed by **Jiban Maji**  
📍 Brainware University, Barasat, West Bengal, India  

GitHub Profile: [https://github.com/Jiban0507](https://github.com/Jiban0507)  
GitHub Repository: `https://github.com/Jiban0507/screen-recorder` [(github.com in Bing)](https://github.com/Jiban0507/Project-Python-100/tree/main/Intermediate_Level/Project-20)


