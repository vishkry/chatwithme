# Import necessary libraries
from flask import Flask, render_template, request, redirect
import openai
import os
import time

from openai import OpenAI
# Set the OpenAI API key
client = OpenAI(api_key = "sk-proj-EZULP3RIvVLvpJHjusXdT3BlbkFJoBj5JB2mioLoikisaa1T")

# Define the name of the bot
name = 'Renu'

# Define the role of the bot
role = 'personal bot'

# Define the impersonated role with instructions
impersonated_role = f"""
    From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. You never give unknown information.
    Renu is a Indian girl, your role is to act as Renu and reply based on that.
    Renu age is 27.
    Your role is to reply on behalf of renu
    Be pprofessional and reply as an freind
    YOU ARE NOT AN AI MODEL!
"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)

# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )


    return output.choices[0].message.content

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
