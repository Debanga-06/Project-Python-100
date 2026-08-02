import requests

QUOTE_API = "https://dummyjson.com/quotes/random"


def create_api():
    """
    Demo API Connection
    """
    print("✅ Demo API Connected Successfully!")
    return True


def post_tweet(api, message=None):
    """
    Simulate Twitter Post using Free API
    """

    try:
        response = requests.get(QUOTE_API, timeout=10)

        if response.status_code == 200:
            data = response.json()

            quote = data["quote"]
            author = data["author"]

            print("\n==============================")
            print("🐦 Twitter Bot (Demo)")
            print("==============================")
            print(f"Tweet : {quote}")
            print(f"Author: {author}")
            print("✅ Tweet Posted Successfully (Simulation)")
            print("==============================\n")

        else:
            print("❌ Failed to fetch quote.")

    except Exception as e:
        print("API Error:", e)