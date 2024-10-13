import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
conversation_history = []
available_models = genai.list_models()
for model in available_models:
    print(model.name)
def handle_message(message):
    conversation_history.append("User: " + message)
    prompt = "\n".join(conversation_history) + "\nAI Response:"

    response = model.generate_content(prompt).text
    conversation_history.append("AI Response: " + response)
    print(conversation_history)
    return response

def classify_conversation():
    sentiment_model = genai.get_model("models/text-sentiment-003")
    cur_convo = "\n".join(conversation_history)
    sentiment_response = sentiment_model.predict(text=cur_convo)
    sentiment_score = sentiment_response.sentiment
    print("Sentiment: " + sentiment_score)
    if sentiment_score >= 0.8:  # Adjust threshold as needed
        return "important"
    elif sentiment_score <= -0.8:
        return "important"
    elif -0.2 < sentiment_score < 0.2: # Adjust threshold as needed
        return "unclear"
    else:
        return "not important"

# Example usage
user_message = "Hello, how are you?"
response = handle_message(user_message)
print(user_message)
print(response)
print(conversation_history)
print(classify_conversation())
user_message2 = "What did I just ask?"
response2 = handle_message(user_message2)
print(user_message2)
print(response2)
print(conversation_history)
print(classify_conversation())