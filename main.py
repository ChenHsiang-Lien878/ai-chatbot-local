import requests
import speech_recognition as sr
import pyttsx3
from datetime import datetime

MODEL_NAME = "llama3"
CHAT_FILE = "chat_history.txt"

conversation_history = []

recognizer = sr.Recognizer()
tts = pyttsx3.init()


def save_message(role, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {role}: {message}\n")


def build_prompt():
    prompt = "You are a helpful and friendly AI chatbot.\n\n"
    for role, message in conversation_history:
        prompt += f"{role}: {message}\n"
    prompt += "Bot:"
    return prompt


def chat_with_ai():
    prompt = build_prompt()
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def listen_to_user():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand you.")
        return None
    except sr.RequestError as error:
        print("Speech recognition error:", error)
        return None


def speak_text(text):
    tts.say(text)
    tts.runAndWait()


print("Voice AI Chatbot started.")
print("Say something, or press Ctrl+C to stop.\n")

try:
    while True:
        user_input = listen_to_user()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "stop"]:
            print("Chat ended.")
            break

        conversation_history.append(("User", user_input))
        save_message("User", user_input)

        try:
            bot_reply = chat_with_ai()
            print("Bot:", bot_reply, "\n")

            conversation_history.append(("Bot", bot_reply))
            save_message("Bot", bot_reply)

            speak_text(bot_reply)

        except requests.exceptions.RequestException as error:
            print("Error connecting to Ollama:", error)

except KeyboardInterrupt:
    print("\nChat ended by user.")