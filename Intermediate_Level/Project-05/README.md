# Project-05: Feedback Email Sender

## 🌟 About the Project
This project is developed by **Jiban Maji** as part of his Python learning journey.  
It is a practical application that allows users to send feedback messages through a simple GUI form.  
The feedback is securely delivered to the developer's Gmail account using **SMTP** and **Google App Passwords**.  

---

## 🚀 What I Have Done
- Built a **Tkinter GUI** where users can enter their email and feedback message.
- Integrated **Gmail SMTP** for sending emails securely.
- Enabled **2-Step Verification** and used **App Passwords** for authentication.
- Stored sensitive data (email, password) in a `.env` file for security.
- Added a `.gitignore` file to ensure `.env` and other unnecessary files are not pushed to GitHub.
- Created a **requirements.txt** file so anyone can install dependencies easily.
- Wrote this **README.md** for clear documentation and project promotion.

---

## 🛠️ Requirements
- Python 3.x
- Libraries:
  - `python-dotenv` (for environment variables)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
Project-05/
├── EmailSender.py        # Main Python code
├── .env                  # Environment variables (NOT pushed to GitHub)
├── .gitignore            # Ignore sensitive files
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Project-05.git
   cd Project-05
   ```

2. Create a `.env` file in the project root:
   ```env
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_16_digit_app_password
   RECEIVER_EMAIL=your_email@gmail.com
   ```

3. Run the application:
   ```bash
   python EmailSender.py
   ```

---

## 🖥️ Usage
- Enter your email and feedback in the GUI form.
- Click **Submit**.
- The feedback will be sent directly to the developer's Gmail inbox.

---

## 🔒 Security Notes
- Do **not** share your `.env` file publicly.
- Always enable **2-Step Verification** in Gmail.
- Use **App Passwords** instead of your main Gmail password.

---

## 📧 Example
When a user submits feedback:
```
Feedback from: user@example.com

Message:
This project is very useful!
```

---

## 👨‍💻 Developer
**Name:** Jiban Maji  
**Focus:** Building robust Python projects with automation, documentation, and security.  

---

## ✅ Future Improvements
- Add logging for sent feedback.
- Store feedback in a local database.
- Create a web-based version using Flask/Django.
```
