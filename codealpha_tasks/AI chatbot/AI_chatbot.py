import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import requests
import sqlite3
import openai
import datetime

# ==========================
# 🔐 ADD YOUR API KEYS HERE
# ==========================
OPENAI_API_KEY = "YOUR_OPENAI_KEY"
WEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

openai.api_key = OPENAI_API_KEY

# ==========================
# 🎤 VOICE ENGINE
# ==========================
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_area.insert(tk.END, "Listening...\n")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Sorry, I couldn't understand."

# ==========================
# 🗄 DATABASE SETUP
# ==========================
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    bot TEXT,
    time TEXT
)
""")
conn.commit()

def save_chat(user, bot):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chat_history (user, bot, time) VALUES (?, ?, ?)",
                   (user, bot, time_now))
    conn.commit()

# ==========================
# 🌤 WEATHER FUNCTION
# ==========================
def get_weather(city="Delhi"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    else:
        return "Weather not found."

# ==========================
# 📰 NEWS FUNCTION
# ==========================
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()

    articles = response.get("articles", [])[:5]
    news_list = "Top News:\n"
    for article in articles:
        news_list += "- " + article["title"] + "\n"

    return news_list

# ==========================
# 🤖 OPENAI GPT RESPONSE
# ==========================
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "Error connecting to AI."

# ==========================
# 💬 MAIN CHAT LOGIC
# ==========================
def chatbot_response(user_input):

    user_input = user_input.lower()

    if "weather" in user_input:
        return get_weather("Delhi")

    elif "news" in user_input:
        return get_news()

    elif "time" in user_input:
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")

    elif "voice" in user_input:
        voice_text = listen()
        return f"You said: {voice_text}"

    else:
        return ask_openai(user_input)

# ==========================
# 🖥 GUI
# ==========================
def send_message():
    user_input = entry.get()
    entry.delete(0, tk.END)

    if user_input.strip() == "":
        return

    chat_area.insert(tk.END, "You: " + user_input + "\n")

    response = chatbot_response(user_input)

    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    speak(response)
    save_chat(user_input, response)

    chat_area.yview(tk.END)

window = tk.Tk()
window.title("Ultimate AI Assistant 🤖")
window.geometry("600x700")
window.configure(bg="#121212")

chat_area = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=70,
    height=30,
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 11)
)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(window, width=50, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(
    window,
    text="Send",
    command=send_message,
    bg="#00ffcc",
    fg="black",
    font=("Arial", 10, "bold")
)
send_button.pack(side=tk.LEFT)

window.mainloop()
