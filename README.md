---

# AI-Native Intent Operating Layer

A modular AI-powered operating layer that interprets natural language using a local LLM and executes structured system actions safely.

---

## Overview

AI-Native Intent Operating Layer is a prototype intelligent operating system layer that transforms natural language into executable system actions.

Instead of traditional command-based interaction, users express intent in plain language. The system:

1. Understands intent using a local LLM
2. Converts intent into structured JSON
3. Routes the structured output to modular tools
4. Executes actions with confirmation and logging

This project demonstrates how AI can function as a structured OS control layer rather than a conversational chatbot.

---

## Architecture

```
User Input
    ↓
Controller (Intent Processing + Memory)
    ↓
LLM Client (Structured JSON Output)
    ↓
Tool Router
    ↓
Modular Tool Execution
    ↓
System Action / Response
```

---

## Core Components

| Component        | Purpose                                                      |
| ---------------- | ------------------------------------------------------------ |
| `controller.py`  | Central orchestration layer (memory, confirmations, parsing) |
| `llm_client.py`  | Connects to local LLM endpoint                               |
| `tool_router.py` | Routes structured tool calls                                 |
| `tools/`         | Modular action handlers                                      |
| `voice/`         | Speech-to-text and text-to-speech modules                    |
| `memory/`        | SQLite-based conversation logging                            |
| `security/`      | Permission safeguards                                        |
| `backend/`       | Server integration layer                                     |
| `frontend/`      | UI prototype                                                 |

---

## Features

### Structured AI Control

* Strict JSON-only LLM responses
* Robust JSON parsing with fallback handling
* Conversation memory trimming
* Confirmation system for destructive actions

### Modular Tool System

#### Productivity Tools

* Open applications
* Send and read emails
* Web search
* Set and show reminders
* File creation, reading, writing, and deletion
* Folder creation
* File summarization

#### System Controls

* Volume control (up, down, mute, unmute)
* Brightness control
* Screenshot capture
* Shutdown and restart
* Lock screen

#### Voice Layer

* Speech-to-text integration
* Text-to-speech using ONNX models
* Extensible wake word architecture

---

## Safety and Control

The system enforces:

* Confirmation prompts for destructive actions
* Strict separation between LLM reasoning and OS execution
* Structured tool execution
* Logging of interactions
* JSON-only response enforcement

---

## Tech Stack

* Python 3.10+
* Local LLM API (OpenAI-compatible endpoint)
* SQLite
* ONNX (TTS models)
* Requests library
* Modular architecture design

---

## Project Structure

```
backend/
config/
frontend/
memory/
security/
tools/
utils/
voice/
controller.py
llm_client.py
tool_router.py
main.py
```

The following are excluded from the repository:

* `.env`
* model files
* logs
* database files
* temporary audio files

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/PraveenKumar2049/AI-Native-Intent-Operating-Layer.git
cd AI-Native-Intent-Operating-Layer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file:

```
EMAIL_ADDRESS=your_email
EMAIL_APP_PASSWORD=your_app_password
LLM_URL=http://127.0.0.1:1234/v1/chat/completions
MODEL_NAME=your_model_name
```

### 4. Run Application

```bash
python main.py
```

---

## Example Interaction

**User Input**

Open Chrome

**LLM Output (Structured JSON)**

```json
{
  "tool": "open_app",
  "arguments": {
    "app_name": "chrome"
  }
}
```

The system safely routes and executes the corresponding tool.

---

## Design Philosophy

This project explores the idea that AI should not only generate text but execute structured intent safely.

Key principles:

* Deterministic tool execution
* Strict model output formatting
* Separation of reasoning and execution
* Modular extensibility

---

## Future Improvements

* Cross-platform support
* Multi-user profiles
* Permission sandboxing
* GUI dashboard
* Cloud LLM fallback
* Advanced intent verification
* Autonomous task chains

---

## Use Case

Built as a competition prototype demonstrating:

* AI system orchestration
* Intent-driven computing
* Modular OS-level automation
* Safe LLM integration

---

## Author

Praveen Kumar
GitHub: [https://github.com/PraveenKumar2049](https://github.com/PraveenKumar2049)

---

