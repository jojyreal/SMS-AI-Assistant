import subprocess
import requests
from flask import Flask, request
import time
import re

#variables
key = "YOUR_TEXTBELT_API_KEY"
phone = 'YOUR_PHONE_NUMBER'
ai_server = "http://x.x.x.x:11434/api/generate"
ai_model = "YOUR_AI_MODEL"
api_url = "https://textbelt.com/text"


# start ngrok
subprocess.Popen('ngrok http 5000', shell=True)

time.sleep(2)

# get public URL from ngrok
response = requests.get('http://localhost:4040/api/tunnels')
data = response.json()

for tunnel in data['tunnels']:
    if tunnel['proto'] == 'https':
        public_url = tunnel['public_url']
        break

print(f'Public URL: {public_url}')


#send a message
def send_text(message):
    resp = requests.post(api_url, {
  'phone': phone,
  'message': message,
  'key': key,
  'replyWebhookUrl': public_url + '/webhook'
})
    print(resp.json())

#generate AI response
def generate_ai_response(user_message):
    payload = {
        "model": ai_model,
        "prompt": f'You are a helpful text message assistant. Respond to questions concisely and briefly. User message: {user_message}',
        "stream": False
    }
    response = requests.post(ai_server, json=payload)
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return 'Sorry, I had trouble connecting to the AI server.'
    
#split long AI responses into multiple texts
def split_messages(message):
    sentences = re.split(r'(?<=[.!?])\s+', message.strip())
    for sentence in sentences:
        send_text(sentence)


#random flask stuff
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data['text']
    print(f'Received data:', data['text'])
    ai_response = generate_ai_response(user_message)
    split_messages(ai_response)
    return 'OK', 200


#init first text
send_text("What can I help you with?")

#start flask webhook
app.run(port=5000)