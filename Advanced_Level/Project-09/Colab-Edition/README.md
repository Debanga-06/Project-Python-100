# 🐦 Twitter Bot

> Automated tweet scheduling & auto-replies using Tweepy · X API v2 · Google Colab

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Tweepy](https://img.shields.io/badge/Tweepy-4.14%2B-1DA1F2?style=flat-square)
![Colab](https://img.shields.io/badge/Run%20on-Google%20Colab-F9AB00?style=flat-square&logo=googlecolab)

---

## 🚀 Features

- **Scheduled Posting** — auto-posts a queue of tweets on a timed interval, no manual posting required
- **Duplicate Protection** — tracks what's already been posted so nothing repeats across runs
- **Rate-Limit Handling** — automatically waits out X's rate limits and retries instead of crashing
- **Dry-Run Mode** — simulate the entire flow with zero API keys and zero real posts, for safe testing
- **Auto-Reply to Mentions** — optional automatic response to anyone who mentions your account
- **Session Persistence** — optional Google Drive mount keeps the queue/log alive across Colab sessions
- **Zero Local Setup** — runs entirely inside one Colab notebook, nothing to install on your machine

---

## 📁 Project Structure

```
twitter_bot/
├── Twitter_Bot_Colab.ipynb    # The entire project — one notebook, run top to bottom
└── README.md
```

Since this is built specifically to run in Google Colab, it's structured as a single notebook rather than a package of scripts. Each section below corresponds to a group of cells inside it:

```
Twitter_Bot_Colab.ipynb
├── 1. Install dependencies         # tweepy, schedule
├── 2. Imports
├── 3. DRY_RUN switch               # test everything with no real API calls
├── 4. Enter API credentials        # secure getpass prompts
├── 5. Connect + verify auth        # tweepy.Client, get_me()
├── 6. (Optional) Google Drive      # persist queue/log across sessions
├── 7. Tweet queue                  # the content the bot will post
├── 8. post_tweet()                 # core posting + rate-limit retry logic
├── 9. post_next_in_queue()         # post one tweet on demand
├── 10. run_scheduler()             # automatic timed posting loop
└── 11. (Optional) auto_reply_to_mentions()
```

---

## ⚙️ Setup

```bash
# 1. Open the notebook in Google Colab
# (upload Twitter_Bot_Colab.ipynb, or open it directly from Drive/GitHub)

# 2. Run the first cell inside Colab — installs dependencies
!pip install -q tweepy schedule
```

You'll also need, before going live:

1. A **Twitter/X Developer account** — https://developer.twitter.com
2. A **Project + App** in the developer portal with **Read and Write** permissions enabled
3. Four credentials from that app:
   - API Key
   - API Key Secret
   - Access Token
   - Access Token Secret

> Twitter/X's free API tier is limited on posting, and access levels have changed over time — check your account's current tier in the developer portal before relying on this.

---

## ▶️ Usage

All usage happens by running notebook cells in order, no command line involved.

```python
# Test everything first — no real API calls, no real posts
DRY_RUN = True

# Add whatever you want posted, in order
new_tweets = [
    "Just automated my Twitter posting with Python.",
    "Working on a side project this week. #buildinpublic",
]

# Post the next queued tweet right now
post_next_in_queue()

# Or let it run on autopilot — one post every 2 hours, up to 10 posts this run
run_scheduler(interval_minutes=120, max_posts=10)

# Optional — reply to recent mentions automatically
auto_reply_to_mentions()
```

Once you've confirmed the dry run behaves the way you want, flip the switch and run the credentials cell:

```python
DRY_RUN = False
```

### Key settings

| Setting            | Default | Description                                          |
|---------------------|---------|-------------------------------------------------------|
| `DRY_RUN`            | `True`  | Simulates posting instead of calling the real API      |
| `USE_DRIVE`          | `False` | Persist the tweet queue + posted log to Google Drive   |
| `interval_minutes`   | `60`    | Minutes to wait between each scheduled post             |
| `max_posts`          | `5`     | Safety cap on how many tweets get sent in one run       |

---

## 📊 Output Files

```
twitter_bot_data/                  # or Drive/twitter_bot/ if USE_DRIVE = True
├── tweet_queue.json               # your tweets + whether each has been posted
└── posted_log.json                # timestamped history of everything actually sent
```

---

## ⚠️ Disclaimer

> This project is for **educational purposes only**.
> Automating posts and replies is subject to X/Twitter's Developer Agreement and automation rules — review their current policies before running this against a real account, and never use it for spam, harassment, or coordinated inauthentic behavior.

Also worth knowing: the scheduler only keeps running while the Colab tab stays open and connected. It is not a substitute for an always-on server if you need continuous, long-term posting.

---

## 📄 License

AGPL-3.0 License — see [LICENSE](LICENSE)
