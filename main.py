from google import genai
from google.genai import errors
import json

print("==============================")
print("     Gemini AI Chatbot")
print("==============================")

try:
    client = genai.Client()

    chat = client.chats.create(
        model="gemini-3.6-flash"
    )

except ValueError:
    print("Error: Gemini API key not found.")
    print("Please configure GEMINI_API_KEY and try again.")
    exit()

history = []

while True:
    user_message = input("\nYou: ")

    command = user_message.strip().lower()

    if not command:
        print("Please enter a message.")
        continue
    
    if command in ["/help" , "help"]:
        print("\nAvailable commands: ")
        print("/help - Show available commands")
        print("/exit - Exit the Chatbot")
        continue

    if command in ["/exit" , "exit"]:
        print("Gemini: Goodbye!")
        break
    
    history.append({
        "role": "user",
        "message": user_message
    })

    try:
        response = chat.send_message(
            message = user_message
        )

        print("\nGemini: ", response.text)

        history.append({
            "role": "gemini",
            "message": response.text
        })

        with open("chat_history.json", "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

    except errors.APIError as error:
        if error.code == 503:
            print("\nGemini is temporarily unavailable.")
            print("Please try again later.")

        elif error.code == 429:
            print("\nYou have reached an API rate or quota limit.")
            print("Please wait and try again later.")

        elif error.code in [401 , 403]:
            print("\nThere is a problem with your Gemini API key or permissions.")

        else:
            print(f"\nGemini API error ({error.code}): {error.message}")