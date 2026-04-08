import requests
from datetime import datetime

MODEL_NAME = "llama3"
CHAT_FILE = "chat_history.txt"

conversation_history = []


def save_message(role, message):
    """Save one message to the chat history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CHAT_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {role}: {message}\n")


def build_prompt():
    """Build the full prompt from conversation history."""
    prompt = "You are a helpful and friendly AI chatbot.\n\n"

    for role, message in conversation_history:
        if role == "User":
            prompt += f"User: {message}\n"
        elif role == "Bot":
            prompt += f"Bot: {message}\n"

    prompt += "Bot:"
    return prompt


def chat_with_ai():
    """Send the full conversation history to Ollama and return the reply."""
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


print("Local AI Chatbot with memory started.")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Chat ended.")
        break

    conversation_history.append(("User", user_input))
    save_message("User", user_input)

    try:
        bot_reply = chat_with_ai()
        print("Bot:", bot_reply, "\n")

        conversation_history.append(("Bot", bot_reply))
        save_message("Bot", bot_reply)

    except requests.exceptions.RequestException as error:
        print("Error connecting to Ollama:", error)