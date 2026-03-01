# SMS-AI-Assistant
A python based way to integrate an AI language model into your SMS messages.

## How It Works

1. The app starts a local Flask server and exposes it publicly via ngrok
2. An initial SMS is sent to the configured phone number via Textbelt to open the webhook to the service
3. When the user replies, Textbelt forwards the message to the Flask webhook
4. The message is sent to a locally hosted Ollama model (llama3.2 in this case) for a response
5. The AI response is split into sentences and sent back as individual SMS messages

## Features

- Powered by a local LLM (Ollama) for no cloud costs
- Two-way SMS via Textbelt API
- Automatic public URL generation with ngrok
- Smart message splitting. Long responses are broken into per-sentence texts

## Requirements

- Python 3.x
- [ngrok](https://ngrok.com/) installed and on your PATH
- [Ollama](https://ollama.com/) running locally with the model of your choice pulled
- A [Textbelt](https://textbelt.com/) API key

## Installation

```bash
pip install flask requests
```

## Configuration

Edit the variables at the top of `assistant.py`:

```python
key = "YOUR_TEXTBELT_API_KEY"
phone = "YOUR_PHONE_NUMBER"  # e.g. '4435551234' for US messages, use E.164 format for global messages
ai_server = "http://x.x.x.x:11434/api/generate"  # Ollama server address
ai_model = "YOUR_AI_MODEL"
```

## Dependencies

| Package | Purpose |
|--------|---------|
| `flask` | Webhook server to receive SMS replies |
| `requests` | HTTP calls to Textbelt and Ollama APIs |
| `subprocess` | Launches ngrok |
| `re` | Sentence splitting for outbound messages |

## Usage

Double click on the python file or navigate to your working directory and use:
```bash
python assistant.py
```

The app will:
1. Start ngrok on port 5000
2. Print the public URL - Warning! Because of the way ngrok and flask take over the terminal, it will NOT look pretty.
3. Send an opening SMS: *"What can I help you with?"*
4. Listen for replies at `/webhook`
