def respond(intent):
    responses = {
        "greeting": "Hello. How may I assist you?",
        "exit": "Shutting down. Goodbye."
    }
    return responses.get(intent, "I'm here.")
