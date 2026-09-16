from google import genai

print("==============================")
print("     Gemini AI Chatbot")
print("==============================")

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.6-flash"
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

    response = chat.send_message(
        message = user_message
    )

    print("\nGemini: ", response.text)