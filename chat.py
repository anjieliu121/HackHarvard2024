import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
system_prompt = "You are an AI assistant responsible for evaluating the importance of incoming calls. Your goal is to classify each call as 'Important' or 'Not Important' based on the following criteria:\nImportant: Emergency services, critical financial notifications, urgent medical appointments, crucial business operations, exigent issues with utilities, follow ups on previous problems\nUnimportant: Non-urgent job-related inquiries, telemarketing, advertisement, political outreach, fundraising, survey\nAfter each prompt from the caller, ask a follow-up question to solicit more information on the topic of the call. Do not disclose the classification of 'Important' and 'Not Important' to the caller. The call is as the following:\n"
conversation_history = [system_prompt]

def handle_message(message):
    conversation_history.append("Caller: " + message)
    prompt = "\n".join(conversation_history) + "\nAI Response:"

    response = model.generate_content(prompt).text
    conversation_history.append("AI Response: " + response)
    print(conversation_history)
    return response

def classify_conversation():
    prompt = "Summarize the topic of the above call with at most 1 phrase and classify the above call as 'Important' or 'Not Important':\n"
    convo = "\n".join(conversation_history)
    response = model.generate_content(convo + prompt).text
    return response

# Example usage
user_message = "Hello, this is Sarah from XYZ Telecom. Am I speaking with Antai?"
response = handle_message(user_message)
print(user_message)
print(response)
print(conversation_history)
print(classify_conversation())
user_message2 = "I’m calling to follow up on the billing discrepancy you reported last week. I’d like to ensure everything has been resolved to your satisfaction."
response2 = handle_message(user_message2)
print(user_message2)
print(response2)
print(conversation_history)
print(classify_conversation())