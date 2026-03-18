import tkinter as tk
from tkinter import ttk, messagebox
from translate import Translator

# Supported languages
languages = {
    "English": "en",
    "Bengali": "bn",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# GUI Setup
root = tk.Tk()
root.title("Language Translator")
root.geometry("600x400")

# Input Text
input_label = tk.Label(root, text="Enter text:", font=("Helvetica", 12))
input_label.pack(pady=5)

input_text = tk.Text(root, height=5, width=60)
input_text.pack(pady=5)

# Language Selection
lang_frame = tk.Frame(root)
lang_frame.pack(pady=10)

src_label = tk.Label(lang_frame, text="Source Language:", font=("Helvetica", 10))
src_label.grid(row=0, column=0, padx=5)

src_lang = ttk.Combobox(lang_frame, values=list(languages.keys()))
src_lang.current(0)
src_lang.grid(row=0, column=1, padx=5)

dest_label = tk.Label(lang_frame, text="Target Language:", font=("Helvetica", 10))
dest_label.grid(row=0, column=2, padx=5)

dest_lang = ttk.Combobox(lang_frame, values=list(languages.keys()))
dest_lang.current(1)
dest_lang.grid(row=0, column=3, padx=5)

# Output Text
output_label = tk.Label(root, text="Translated text:", font=("Helvetica", 12))
output_label.pack(pady=5)

output_text = tk.Text(root, height=5, width=60)
output_text.pack(pady=5)

# Translate Function
def translate_text():
    src = src_lang.get()
    dest = dest_lang.get()
    text = input_text.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text to translate.")
        return
    
    try:
        translator = Translator(to_lang=languages[dest], from_lang=languages[src])
        translation = translator.translate(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translation)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# Translate Button
translate_btn = tk.Button(root, text="Translate", command=translate_text)
translate_btn.pack(pady=10)

root.mainloop()