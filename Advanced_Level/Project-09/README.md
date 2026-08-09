# 🐦 Twitter (X) Auto Posting Bot (Demo Version)

> A Python-based automation project that demonstrates **API Integration**, **Task Scheduling**, and **Automation** by simulating a Twitter (X) bot using a free public API.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Demo-orange)
[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Automation](https://img.shields.io/badge/Automation-Enabled-success)
![API](https://img.shields.io/badge/API-Free%20Public%20API-blueviolet)

---

## 📖 Overview

This project is designed to demonstrate the core concepts behind a Twitter automation bot without requiring paid Twitter (X) API access.

Instead of posting real tweets, the application fetches random quotes from a free public API and displays them as **simulated tweets** at scheduled intervals.

It is a great project for learning:

* REST API Integration
* Python Automation
* Scheduling Tasks
* Logging
* Modular Programming
* Error Handling

---

## ✨ Features

* 🔹 API Integration
* 🔹 Automated Data Fetching
* 🔹 Scheduled Execution
* 🔹 Clean Modular Code
* 🔹 Logging Support
* 🔹 Error Handling
* 🔹 Beginner Friendly
* 🔹 Easy to Extend

---

## 📂 Project Structure

```text
Project-09/
│
├── main.py               # Main application
├── twitter_api.py        # API handling
├── tweets.csv            # Sample tweet data
├── .env                  # API credentials (for real Twitter bot)
├── requirements.txt
├── README.md
└── bot.log               # Generated automatically
```

---

## ⚙️ Requirements

* Python 3.10+
* Internet Connection

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Project-Python-100.git
```

Move into the project directory:

```bash
cd Project-Python-100/Advanced_Level/Project-09
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install tweepy python-dotenv pandas schedule requests
```

---

## ▶️ Run

```bash
python main.py
```

---

## 🖥 Sample Output

```text
==================================================
      Twitter (X) Auto Posting Bot
==================================================

Bot Started Successfully...
Demo Mode Enabled
Posting every 30 seconds...

--------------------------------------

✅ Demo API Connected Successfully!

Fetching data from Free API...

==============================
🐦 Twitter Bot (Demo)
==============================
Tweet : Success is not final.
Author: Winston Churchill
✅ Tweet Posted Successfully (Simulation)
==============================
```

---

## 🔄 How It Works

```text
Start Application
        │
        ▼
Connect to API
        │
        ▼
Fetch Random Quote
        │
        ▼
Display as Demo Tweet
        │
        ▼
Write Log
        │
        ▼
Wait for Scheduled Time
        │
        ▼
Repeat
```

---

## 🛠 Technologies Used

* Python
* Requests
* Tweepy
* Schedule
* Pandas
* Python-dotenv
* Logging

---

## 📝 Logging

Every execution is recorded in:

```text
bot.log
```

This helps track execution history and debug issues.

---

## 🔧 Configuration

You can modify the execution interval in **main.py**.

Example:

```python
schedule.every(30).seconds.do(send_tweet)
```

You may also use:

```python
schedule.every(5).minutes.do(send_tweet)
```

or

```python
schedule.every().day.at("10:00").do(send_tweet)
```

---

# 🚀 Convert This Demo into a Real Twitter (X) Bot

The current version is a **simulation**.

To publish real tweets on X (Twitter), you need your own **X Developer API** credentials.

### Step 1

Create an X Developer account.

### Step 2

Create an App.

### Step 3

Generate:

* API Key
* API Secret
* Access Token
* Access Token Secret

### Step 4

Open the `.env` file and replace the placeholder values with your own credentials.

```env
API_KEY=YOUR_API_KEY
API_SECRET=YOUR_API_SECRET
ACCESS_TOKEN=YOUR_ACCESS_TOKEN
ACCESS_SECRET=YOUR_ACCESS_SECRET
```

### Step 5

Update the API implementation to use the official X API for publishing tweets.

> **Important:** The credentials are **not included** in this repository. Every user must provide their own API keys to enable real Twitter posting.

---

## ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes**.

The default implementation **does not publish tweets to Twitter (X)**.

It demonstrates API integration, scheduling, automation, and modular Python development using a free public API.

---

## 🤝 Contributing

Contributions are always welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

---

## 📜 License

This project is licensed under the AGPL-3.0 License.

---

# 👨‍💻 Author

**Jiban Maji**

Computer Science & Engineering (AI & ML)

Python Developer • API Integration • Automation • Open Source Learning

⭐ If you found this project helpful, consider giving it a **Star** on GitHub.
