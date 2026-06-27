import random
import re
import json
from datetime import datetime
import os

# ---------------------------------------------------------
# 1. RULES: keyword patterns (regex) -> responses
# ---------------------------------------------------------
rules = {
    r"\b(hello|hi|hey)\b": ["Hi there!", "Hello!", "Hey! How can I help you?"],
    r"\bhow are you\b": ["I'm just a program, but I'm doing great!", "I'm functioning as expected!"],
    r"\b(your name|who are you)\b": ["I'm a rule-based chatbot built in Python.", "You can call me ChatBot."],
    r"\b(your age|how old)\b": ["I don't have an age, I'm just code!", "Age doesn't apply to me."],
    r"\bweather\b": ["I can't check live weather, but I hope it's nice where you are!"],
    r"\b(help|what can you do)\b": ["I can chat about basic topics. Try asking about my name, age, or say hello!"],
    r"\b(joke|funny)\b": [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Python programmers wear glasses? Because they can't C."
    ],
    r"\b(thanks|thank you)\b": ["You're welcome!", "No problem!", "Anytime!"],
    r"\btime\b": ["__TIME__"],
    r"\b(date|today)\b": ["__DATE__"],
    r"\b(bye|goodbye|exit|quit)\b": ["Goodbye!", "See you later!", "Bye! Take care."]
}

default_responses = [
    "I'm not sure I understand. Can you rephrase that?",
    "Could you elaborate on that?",
    "I don't have an answer for that yet.",
    "Hmm, I'm not trained to answer that."
]

LOG_FILE = "chat_log.json"


def get_response(user_input):
    user_input = user_input.lower().strip()
    best_match = None
    best_score = 0

    for pattern, possible_responses in rules.items():
        matches = re.findall(pattern, user_input)
        score = len(matches)
        if score > best_score:
            best_score = score
            best_match = possible_responses

    if best_match:
        reply = random.choice(best_match)
        if reply == "__TIME__":
            reply = f"It's {datetime.now().strftime('%H:%M:%S')} right now."
        elif reply == "__DATE__":
            reply = f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
        return reply

    return random.choice(default_responses)


def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def log_exchange(log, user_msg, bot_msg):
    log.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user": user_msg,
        "bot": bot_msg
    })
    save_log(log)


def chat_console():
    print("ChatBot: Hello! Type 'quit' or 'exit' to end the chat.\n")
    log = load_log()

    while True:
        user_input = input("You: ")

        if user_input.strip() == "":
            print("ChatBot: Please type something!")
            continue

        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()):
            response = random.choice(["Goodbye!", "See you later!", "Bye! Take care."])
            print("ChatBot:", response)
            log_exchange(log, user_input, response)
            break

        response = get_response(user_input)
        print("ChatBot:", response)
        log_exchange(log, user_input, response)


if __name__ == "__main__":
    chat_console()
