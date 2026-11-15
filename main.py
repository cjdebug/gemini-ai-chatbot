from google import genai
from google.genai import errors
from history import load_history, save_history

print("==============================")
print("     Gemini AI Chatbot")
print("==============================")

try:
    client = genai.Client()

except ValueError:
    print("Error: Gemini API key not found.")
    print("Please configure GEMINI_API_KEY and try again.")
    exit()

history = load_history()

gemini_history = []

for message in history:
    gemini_history.append({
        "role": "model" if message["role"] == "gemini" else "user",
        "parts": [
            {
                "text": message["message"]
            }
        ]
    })

chat = client.chats.create(
        model="gemini-3.6-flash",
        history = gemini_history
    )

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

        save_history(history)
        
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