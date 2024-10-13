import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

system_prompt = "You are an AI assistant app responsible for evaluating the importance of incoming calls to the 1 human user of this app. You serve only the 1 human user on whose phone you reside in. Your goal is to classify each call as 'Important' or 'Not Important' based on the following criteria:\nImportant: Emergency services, critical financial notifications, urgent medical appointments, crucial business operations, exigent issues with utilities, follow ups on previous problems\nUnimportant: Non-urgent job-related inquiries, telemarketing, advertisement, political outreach, fundraising, survey\nAfter each prompt from the caller, ask a follow-up question to solicit more information on the topic of the call. Do not disclose the classification of 'Important' and 'Not Important' to the caller. The call is as the following:\n"
conversation_history = [system_prompt]

@app.route("/classify", methods=['POST'])
def classify_conversation():
    vocalInput = request.json['vocalInput']
    exchanges = request.json['exchanges']
    conversation_history.append("Caller: " + vocalInput)
    evaluation_prompt = "Summarize the topic of the above call with at most 1 phrase and classify the above call as 'Important' or 'Not Important':\n"
    convo = "\n".join(conversation_history)
    evaluation = model.generate_content(convo + evaluation_prompt).text
    print(evaluation)

    if exchanges >= 3:
        ending_prompt = ""
        if "not important" in evaluation.lower():
            print("NOT IMPORTANT")
            ending_prompt = "Politely end the conversation and do not transfer them to another human"
        else:
            ending_prompt = "Inform the caller that the call will be immediately transferred to the human user"
        ending = model.generate_content(convo + ending_prompt).text
        return jsonify({"response" : ending})

    continue_prompt = "\n".join(conversation_history) + "\nAI Response: (Do not include 'AI Response' as a part of the response)"
    continue_response = model.generate_content(continue_prompt).text
    print("AI's Response: " + continue_response)
    conversation_history.append("AI Response: " + continue_response)
    print(conversation_history)
    return jsonify({"response" : continue_response})