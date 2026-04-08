import requests

def chat_with_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

print("Local AI Chatbot (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    reply = chat_with_ai(user_input)
    print("Bot:", reply, "\n")