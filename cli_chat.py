import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)

chat_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[
        {
            "function_declarations": [
                {
                    "name": "collect_feedback",
                    "description": "Gathers a user review and a rating between 1 and 5.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "review": {
                                "type": "string",
                                "description": "User's short review of their chat experience",
                            },
                            "rating": {
                                "type": "integer",
                                "description": "Experience rating (1-5)"
                            },
                        },
                        "required": ["review", "rating"],
                    },
                }
            ]
        }
    ]
)

conversation_log = []


def write_feedback(feedback):
    with open("feedback.txt", "a") as file:
        file.write(f"Review: {feedback['review']}\n")
        file.write(f"Rating: {feedback['rating']}\n")
        file.write("-" * 40 + "\n")


def write_chat_log(messages):
    with open("chat_history.txt", "a") as file:
        for message in messages:
            file.write(message + "\n")
        file.write("-" * 40 + "\n")


def check_exit_intent(message):
    temp_chat = chat_model.start_chat()
    prompt = (
        f"Decide if the user intend to exit. Reply only 'yes' or 'no'. Message: \"{message}\""
    )

    try:
        response = temp_chat.send_message(prompt)
        decision = response.text.strip().lower()
        return "yes" in decision
    except Exception as error:
        print(f"⚠️ Error checking exit intent: {str(error)}")
        return False


def chat_session():
    print("👋 Welcome to the chatbot!")

    while True:
        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        conversation_log.append(f"You: {user_message}")

        if check_exit_intent(user_message):

            feedback_chat = chat_model.start_chat()
            while True:
                try:
                    feedback_input = input("\nPlease leave a review and rating! ").strip()
                    response = feedback_chat.send_message(feedback_input)
                    if response.candidates[0].content.parts[0].function_call:
                        feedback = response.candidates[0].content.parts[0].function_call.args
                        write_feedback(feedback)
                        write_chat_log(conversation_log)
                        print("\n🙏 Thanks for your feedback! Goodbye!")
                        return
                    print("Please provide a valid review and a rating between 1-5!")
                except Exception as error:
                    print(f"⚠️ Error extracting feedback: {str(error)}")
                    break


        try:
            chat = chat_model.start_chat()
            reply = chat.send_message(user_message)
            bot_response = reply.text.strip()

            print(f"\nBot: {bot_response}")
            conversation_log.append(f"Bot: {bot_response}")

        except Exception as error:
            print(f"Communication error:")


if __name__ == "__main__":
    chat_session()
