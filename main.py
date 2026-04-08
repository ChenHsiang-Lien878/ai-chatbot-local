import speech_recognition as sr
import requests

MODEL_NAME = "llama3"

recognizer = sr.Recognizer()
mic = sr.Microphone()

conversation_history = []


def build_prompt():
    prompt = "You are a helpful AI assistant.\n\n"
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
    return response.json()["response"].strip()


def record_audio():
    print("\nPress ENTER to start recording...")
    input()

    print("🎤 Recording... Press ENTER to stop.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=None)

    input()  # wait for stop
    print("Processing...")

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Speech recognition error:", e)
        return None


print("Voice Chatbot (Press ENTER to record, Ctrl+C to exit)\n")

while True:
    user_input = record_audio()

    if not user_input:
        continue

    if user_input.lower() in ["quit", "exit", "stop"]:
        print("Ending chat.")
        break

    conversation_history.append(("User", user_input))

    try:
        bot_reply = chat_with_ai()
        print("Bot:", bot_reply, "\n")

        conversation_history.append(("Bot", bot_reply))

    except Exception as e:
        print("Error:", e)