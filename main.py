import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import base64

# ---------------- Setup Gemini API ----------------
encoded_api = "QUl6YVN5Qmpuc25jSDNoandvUDRlZVlwRm5YWnd3NUpBb0NPbTlV"  
API_KEY = base64.b64decode(encoded_api).decode("utf-8")
MODEL = "gemini-1.5-flash"
# Use requests Session (better DNS handling)
session = requests.Session()

def call_gemini(prompt, max_tokens=120):
    """Send request to Gemini API and return response text."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.3
            }
        }
        headers = {"Content-Type": "application/json"}

        response = session.post(url, headers=headers, json=payload, timeout=15, verify=True)

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response.")
    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("🏥 Health Care AI Assistant")
root.geometry("700x600")
root.config(bg="#f0f9ff")

# Title
title_label = tk.Label(root, text="🏥 Health Care AI Assistant", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10)
title_label.pack(fill="x")

# Input
input_label = tk.Label(root, text="Enter your symptoms / question / healthcare text:", font=("Arial", 12), bg="#f0f9ff")
input_label.pack(pady=5)

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=8, font=("Arial", 11))
input_text.pack(padx=10, pady=5)

# Output
output_label = tk.Label(root, text="AI Response:", font=("Arial", 12), bg="#f0f9ff")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 11), bg="white")
output_text.pack(padx=10, pady=5)

# Functions
def analyze_symptoms():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter your symptoms.")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Analyzing symptoms...\n")
    prompt = f"You are a healthcare assistant. The patient has symptoms: {user_input}. Provide possible conditions (not diagnosis), in simple terms."
    response = call_gemini(prompt, 100)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

def medical_guidance():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter a question.")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Providing guidance...\n")
    prompt = f"Provide general medical guidance for this question: {user_input}. Keep it clear, short, and easy to understand."
    response = call_gemini(prompt, 120)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

def healthcare_insights():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter some healthcare-related text.")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Generating insights...\n")
    prompt = f"Analyze this healthcare-related text and give insights in 4-5 sentences:\n\n{user_input}"
    response = call_gemini(prompt, 150)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f9ff")
btn_frame.pack(pady=10)

btn1 = tk.Button(btn_frame, text="🩺 Symptom Analysis", font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5, command=analyze_symptoms)
btn1.grid(row=0, column=0, padx=10)

btn2 = tk.Button(btn_frame, text="💊 Medical Guidance", font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5, command=medical_guidance)
btn2.grid(row=0, column=1, padx=10)

btn3 = tk.Button(btn_frame, text="📊 Healthcare Insights", font=("Arial", 12), bg="#FF9800", fg="white", padx=10, pady=5, command=healthcare_insights)
btn3.grid(row=0, column=2, padx=10)

# Run
root.mainloop()
