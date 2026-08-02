"""
===========================================
Twitter (X) Auto Posting Bot (Demo Version)
Project: API Integration + Automation + Scheduling
Author: Jiban Maji
===========================================
"""

import time
import logging
import schedule

from twitter_api import create_api, post_tweet


# -----------------------------------------
# Logging Configuration
# -----------------------------------------
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------------------
# Main Tweet Function
# -----------------------------------------
def send_tweet():

    print("\n--------------------------------------")

    # Connect to Demo API
    api = create_api()

    if api is None:
        logging.error("API Connection Failed")
        return

    print("Fetching data from Free API...")

    # Simulated Tweet Posting
    post_tweet(api)

    logging.info("Demo Tweet Posted Successfully")


# -----------------------------------------
# Scheduler
# -----------------------------------------
def start_scheduler():

    print("=" * 50)
    print("      Twitter (X) Auto Posting Bot")
    print("=" * 50)
    print("Bot Started Successfully...")
    print("Demo Mode Enabled")
    print("Posting every 30 seconds...\n")

    # First execution immediately
    send_tweet()

    # Then every 30 seconds
    schedule.every(30).seconds.do(send_tweet)

    while True:
        schedule.run_pending()
        time.sleep(1)


# -----------------------------------------
# Main Function
# -----------------------------------------
def main():

    try:
        start_scheduler()

    except KeyboardInterrupt:
        print("\nBot Stopped Successfully.")
        logging.info("Bot Stopped by User")

    except Exception as e:
        print("Unexpected Error:", e)
        logging.error(e)


# -----------------------------------------
# Program Entry
# -----------------------------------------
if __name__ == "__main__":
    main()