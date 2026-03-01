import requests
import json
from config.config_loader import load_config

# ============================================================
# LOAD CONFIG
# ============================================================

config = load_config()

LLM_URL = config["llm_url"]
MODEL_NAME = config["model_name"]

# ============================================================
# SYSTEM PROMPT (UPDATED WITH NEW OS TOOLS)
# ============================================================

SYSTEM_PROMPT = """
You are an AI OS controller.

You MUST reply in STRICT valid JSON only.

----------------------------------------
AVAILABLE TOOLS
----------------------------------------

1) Open application
{
  "tool": "open_app",
  "arguments": {
    "app_name": "appname"
  }
}

2) Read recent emails
{
  "tool": "read_recent_emails",
  "arguments": {
    "limit": number,
    "summarize": true_or_false
  }
}

3) Send email
{
  "tool": "send_email",
  "arguments": {
    "to": "email",
    "subject": "text",
    "body": "text"
  }
}

4) Set reminder
{
  "tool": "set_reminder",
  "arguments": {
    "task": "text",
    "time": "time"
  }
}

5) Show reminders
{
  "tool": "show_reminders",
  "arguments": {}
}

6) Web search
{
  "tool": "web_search",
  "arguments": {
    "query": "search text"
  }
}

7) Create file
{
  "tool": "create_file",
  "arguments": {
    "path": "filename",
    "content": "optional text"
  }
}

8) Read file
{
  "tool": "read_file",
  "arguments": {
    "path": "filename"
  }
}

9) Write file
{
  "tool": "write_file",
  "arguments": {
    "path": "filename",
    "content": "text"
  }
}

10) Delete file
{
  "tool": "delete_file",
  "arguments": {
    "path": "filename"
  }
}

11) Create folder
{
  "tool": "create_folder",
  "arguments": {
    "path": "foldername"
  }
}

12) Summarize file
{
  "tool": "summarize_file",
  "arguments": {
    "path": "filename"
  }
}

----------------------------------------
SYSTEM CONTROL TOOLS
----------------------------------------

13) Increase volume
{
  "tool": "volume_up",
  "arguments": {}
}

14) Decrease volume
{
  "tool": "volume_down",
  "arguments": {}
}

15) Mute system
{
  "tool": "mute",
  "arguments": {}
}

16) Unmute system
{
  "tool": "unmute",
  "arguments": {}
}

17) Increase brightness
{
  "tool": "brightness_up",
  "arguments": {}
}

18) Decrease brightness
{
  "tool": "brightness_down",
  "arguments": {}
}

19) Take screenshot
{
  "tool": "screenshot",
  "arguments": {}
}

20) Shutdown computer
{
  "tool": "shutdown_pc",
  "arguments": {}
}

21) Restart computer
{
  "tool": "restart_pc",
  "arguments": {}
}

22) Lock screen
{
  "tool": "lock_screen",
  "arguments": {}
}

----------------------------------------
NORMAL CHAT
----------------------------------------

If NO tool is required, you MUST return:

{
  "response": "STRING ONLY"
}

CRITICAL RULES FOR 'response':
- The value of "response" MUST be a STRING.
- NEVER return an object inside "response".
- NEVER return nested JSON inside "response".
- NEVER create keys inside "response".
- The entire content must be plain text formatted using Markdown.
- Markdown is allowed INSIDE the string only.
- Tool calls are the ONLY place JSON structure is allowed.

----------------------------------------
STRICT OUTPUT RULES
----------------------------------------
- Output must be a single valid JSON object.
- Do not wrap JSON in markdown.
- Do not include backticks.
- Do not include explanations outside JSON.
- Do not return empty JSON.
- If unsure, return:
  {"response": "I am not sure how to handle that."}
"""

# ============================================================
# NON-STREAMING REQUEST
# ============================================================


def ask_llm(messages):

    payload = {"model": MODEL_NAME, "messages": messages, "temperature": 0.1}

    try:
        res = requests.post(LLM_URL, json=payload, timeout=60)
        res.raise_for_status()

        data = res.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)
        return json.dumps({"response": "LLM connection failed."})


# ============================================================
# STREAMING REQUEST (ROBUST)
# ============================================================


def ask_llm_stream(messages):

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.1,
        "stream": True,
    }

    try:
        with requests.post(LLM_URL, json=payload, stream=True, timeout=60) as res:

            res.raise_for_status()

            for line in res.iter_lines():

                if not line:
                    continue

                decoded = line.decode("utf-8").strip()

                if decoded.startswith("data: "):
                    decoded = decoded[6:].strip()

                if decoded == "[DONE]":
                    break

                if not decoded.startswith("{"):
                    continue

                try:
                    chunk_json = json.loads(decoded)
                    delta = chunk_json["choices"][0].get("delta", {})

                    if "content" in delta:
                        yield delta["content"]

                except Exception:
                    continue

    except Exception as e:
        print("STREAM ERROR:", e)
        yield ""


# ============================================================
# SUMMARIZATION
# ============================================================


def summarize_text(text):

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "Summarize clearly and concisely. Plain text only.",
            },
            {"role": "user", "content": text},
        ],
        "temperature": 0.2,
    }

    try:
        res = requests.post(LLM_URL, json=payload, timeout=60)
        res.raise_for_status()

        data = res.json()
        return data["choices"][0]["message"]["content"]

    except Exception:
        return "Summary failed."
