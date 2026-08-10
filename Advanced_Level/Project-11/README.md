# 🎙️ Voice Assistant

> Browser-mic voice assistant with speech recognition & spoken replies · SpeechRecognition · gTTS · Google Colab

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-3.10%2B-4B8BBE?style=flat-square)
![Colab](https://img.shields.io/badge/Run%20on-Google%20Colab-F9AB00?style=flat-square&logo=googlecolab)

---

## 🚀 Features

- **Browser Mic Recording** — captures your voice through a small JavaScript bridge, since Colab has no direct hardware mic access
- **Speech-to-Text** — transcribes recordings with `SpeechRecognition` (Google's free Web Speech API, no key required)
- **Rule-Based Command Router** — handles common intents out of the box: time, date, jokes, greetings, name, goodbye
- **Text-to-Speech Replies** — speaks responses back using `gTTS`, played inline right in the notebook
- **Multi-Turn Conversation Loop** — keeps listening and replying until you say "bye", "exit", or "stop"
- **Text-Only Test Mode** — test the response + voice logic without recording audio each time
- **LLM-Ready** — the command router is a drop-in point for swapping in an LLM for open-ended chat
- **Zero Local Setup** — runs entirely inside one Colab notebook, nothing to install on your machine

---

## 📁 Project Structure

```
voice_assistant/
├── Voice_Assistant.ipynb    # The entire project — one notebook, run top to bottom
└── README.md
```

Since this is built specifically to run in Google Colab, it's structured as a single notebook rather than a package of scripts. Each section below corresponds to a group of cells inside it:

```
Voice_Assistant.ipynb
├── 1. Install dependencies        # SpeechRecognition, gTTS, pydub, ffmpeg
├── 2. Imports
├── 3. record_audio()              # JS bridge to your browser's microphone
├── 4. transcribe_audio()          # speech-to-text via Google Web Speech API
├── 5. speak()                     # text-to-speech via gTTS, plays inline
├── 6. get_response()              # rule-based command router (time, jokes, greetings...)
├── 7. voice_turn()                # one full record → transcribe → respond → speak cycle
├── 8. run_assistant()             # multi-turn conversation loop
└── 9. text_turn()                 # text-only test mode, no mic needed
```

---

## ⚙️ Setup

```bash
# 1. Open the notebook in Google Colab
# (upload Voice_Assistant.ipynb, or open it directly from Drive/GitHub)

# 2. Run the first cell inside Colab — installs dependencies
!pip install -q SpeechRecognition gTTS pydub
!apt-get -qq install -y ffmpeg
```

No API keys or accounts needed. When you run a recording cell, your browser will ask for microphone permission — allow it, then click the on-page button to start/stop recording.

---

## ▶️ Usage

All usage happens by running notebook cells in order, no command line involved.

```python
# One full voice exchange: record, transcribe, respond, speak
voice_turn()

# Keep the conversation going until you say "bye", "exit", or "stop"
run_assistant(max_turns=10)

# Test the response + voice logic without touching the mic
text_turn("tell me a joke")
```

### Key settings

| Setting        | Default | Description                                          |
|-----------------|---------|--------------------------------------------------------|
| `lang`           | `'en'`  | Language passed to gTTS for the spoken reply             |
| `max_turns`      | `10`    | Safety cap on how many exchanges `run_assistant()` allows |
| `COMMANDS` logic | rule-based | Add new `if` branches in `get_response()` for new intents |

---

## 📊 Output Files

```
input.wav      # your most recent recorded voice input
reply.mp3      # the assistant's most recent spoken reply
```

Both are overwritten each turn — copy them out (or mount Drive) if you want to keep a history.

---

## ⚠️ Disclaimer

> This project is for **educational purposes only**.
> `recognize_google()` uses Google's free, rate-limited Web Speech API — fine for demos and learning, not intended for production or high-volume use. `gTTS` also requires an internet connection and calls Google's Translate TTS endpoint under the hood.

Also worth knowing: the mic-recording JS bridge only works in Colab's browser-connected hosted runtime, and won't work with a local runtime that lacks a browser mic path.

---

## 🚀 Features

- **Browser Mic Recording** — captures your voice through a small JavaScript bridge, since Colab has no direct hardware mic access
- **Speech-to-Text** — transcribes recordings with `SpeechRecognition` (Google's free Web Speech API, no key required)
- **Rule-Based Command Router** — handles common intents out of the box: time, date, jokes, greetings, name, goodbye
- **Text-to-Speech Replies** — speaks responses back using `gTTS`, played inline right in the notebook
- **Multi-Turn Conversation Loop** — keeps listening and replying until you say "bye", "exit", or "stop"
- **Text-Only Test Mode** — test the response + voice logic without recording audio each time
- **LLM-Ready** — the command router is a drop-in point for swapping in an LLM for open-ended chat
- **Zero Local Setup** — runs entirely inside one Colab notebook, nothing to install on your machine

---

## 📁 Project Structure

```
voice_assistant/
├── Voice_Assistant.ipynb    # The entire project — one notebook, run top to bottom
└── README.md
```

Since this is built specifically to run in Google Colab, it's structured as a single notebook rather than a package of scripts. Each section below corresponds to a group of cells inside it:

```
Voice_Assistant.ipynb
├── 1. Install dependencies        # SpeechRecognition, gTTS, pydub, ffmpeg
├── 2. Imports
├── 3. record_audio()              # JS bridge to your browser's microphone
├── 4. transcribe_audio()          # speech-to-text via Google Web Speech API
├── 5. speak()                     # text-to-speech via gTTS, plays inline
├── 6. get_response()              # rule-based command router (time, jokes, greetings...)
├── 7. voice_turn()                # one full record → transcribe → respond → speak cycle
├── 8. run_assistant()             # multi-turn conversation loop
└── 9. text_turn()                 # text-only test mode, no mic needed
```

---

## ⚙️ Setup

```bash
# 1. Open the notebook in Google Colab
# (upload Voice_Assistant.ipynb, or open it directly from Drive/GitHub)

# 2. Run the first cell inside Colab — installs dependencies
!pip install -q SpeechRecognition gTTS pydub
!apt-get -qq install -y ffmpeg
```

No API keys or accounts needed. When you run a recording cell, your browser will ask for microphone permission — allow it, then click the on-page button to start/stop recording.

---

## ▶️ Usage

All usage happens by running notebook cells in order, no command line involved.

```python
# One full voice exchange: record, transcribe, respond, speak
voice_turn()

# Keep the conversation going until you say "bye", "exit", or "stop"
run_assistant(max_turns=10)

# Test the response + voice logic without touching the mic
text_turn("tell me a joke")
```

### Key settings

| Setting        | Default | Description                                          |
|-----------------|---------|--------------------------------------------------------|
| `lang`           | `'en'`  | Language passed to gTTS for the spoken reply             |
| `max_turns`      | `10`    | Safety cap on how many exchanges `run_assistant()` allows |
| `COMMANDS` logic | rule-based | Add new `if` branches in `get_response()` for new intents |

---

## 📊 Output Files

```
input.wav      # your most recent recorded voice input
reply.mp3      # the assistant's most recent spoken reply
```

Both are overwritten each turn — copy them out (or mount Drive) if you want to keep a history.

---

## ⚠️ Disclaimer

> This project is for **educational purposes only**.
> `recognize_google()` uses Google's free, rate-limited Web Speech API — fine for demos and learning, not intended for production or high-volume use. `gTTS` also requires an internet connection and calls Google's Translate TTS endpoint under the hood.

Also worth knowing: the mic-recording JS bridge only works in Colab's browser-connected hosted runtime, and won't work with a local runtime that lacks a browser mic path.

---

## 📄 License

AGPL-3.0 License — see [LICENSE](LICENSE)