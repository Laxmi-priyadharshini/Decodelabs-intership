# Rule-Based AI Chatbot

A simple, dependency-free chatbot built in Python using **regular expressions**, **dictionaries**, and **loops** — no machine learning required. It runs either in the console or in a Tkinter GUI window, and logs every conversation to a JSON file.

---

## Features

- **Pattern-based matching** — uses `re` with `\b` word-boundary regex so keywords like "hi" don't false-match inside words like "this".
- **Best-match scoring** — counts how many times each rule's pattern matches the input and picks the highest-scoring rule, instead of stopping at the first match.
- **Dynamic replies** — live `time` and `date` responses generated with `datetime`.
- **Persistent logging** — every exchange (user message, bot reply, timestamp) is saved to `chat_log.json`.
- **Two interfaces** — a console (terminal) mode and a graphical Tkinter window, both powered by the same matching engine.

## Requirements

- Python 3.6+
- No external packages — only standard library (`re`, `json`, `os`, `random`, `datetime`, `tkinter`)
- `tkinter` ships with most Python installs. On Ubuntu/Debian, if missing: `sudo apt install python3-tk`

## How to Run

```bash
python3 chatbot.py
```

You'll be prompted to choose a mode:

```
Choose mode - (1) Console  (2) GUI:
```

- **1** → runs in the terminal
- **2** → opens the Tkinter chat window

Type `bye`, `quit`, or `exit` at any time to end the conversation.

## Example

```
You: hello
ChatBot: Hey! How can I help you?
You: tell me a joke
ChatBot: Why don't programmers like nature? It has too many bugs.
You: what's the time
ChatBot: It's 14:32:07 right now.
You: bye
ChatBot: Goodbye!
```

## How It Works

1. `rules` — a dictionary mapping a regex pattern to a list of possible replies.
2. `get_response()` — loops through every rule, scores it against the cleaned user input with `re.findall()`, and returns a random reply from the best-scoring rule (or a fallback if nothing matches).
3. `log_exchange()` / `save_log()` / `load_log()` — append each exchange to `chat_log.json` with an ISO timestamp, preserving history across runs.
4. `chat_console()` / `chat_gui()` — two thin interface layers that both call `get_response()` and `log_exchange()`.

## Project Files

| File | Description |
|---|---|
| `chatbot.py` | Main chatbot script (console + GUI modes) |
| `chat_log.json` | Auto-generated conversation history (created on first run) |
| `Rule_Based_Chatbot_Report.pdf` / `.docx` | Full project report with flowcharts, architecture diagram, and source walkthrough |

## Extending It

- Add new intents by adding a new `pattern: [responses]` entry to the `rules` dictionary — no other code changes needed.
- Swap the in-memory `rules` dict for a JSON/YAML config file to let non-programmers edit responses.
- Add a confidence threshold so very weak matches fall back to the default response instead of a low-scoring rule.

## License

This project was built as a submission for the DecodeLabs Industrial Training Kit (AI track). Free to reuse and extend for learning purposes.
