import smtplib
from email.mime.text import MIMEText
from tkinter import Tk, Label, Entry, Text, Button, END
from dotenv import load_dotenv
import os

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ==========================
# Email Sending Function
# ==========================
def send_feedback(user_email, feedback_text):
    try:
        body = f"Feedback from: {user_email}\n\nMessage:\n{feedback_text}"
        msg = MIMEText(body)
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "New Project Feedback"

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ Feedback sent successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==========================
# GUI Setup
# ==========================
def submit_feedback():
    user_email = email_entry.get().strip()
    feedback = text_box.get("1.0", END).strip()
    if user_email and feedback:
        send_feedback(user_email, feedback)
        email_entry.delete(0, END)
        text_box.delete("1.0", END)

root = Tk()
root.title("Project Feedback")

Label(root, text="Your Email:", font=("Arial", 12)).pack(pady=5)
email_entry = Entry(root, width=40)
email_entry.pack(pady=5)

Label(root, text="Your Feedback:", font=("Arial", 12)).pack(pady=5)
text_box = Text(root, height=10, width=50)
text_box.pack(pady=5)

Button(root, text="Submit", command=submit_feedback).pack(pady=10)

root.mainloop()