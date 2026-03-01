import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")

def load_config():
    # Load base config
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    # ===============================
    # Inject sensitive data from .env
    # ===============================
    config["email"]["address"] = os.getenv("EMAIL_ADDRESS")
    config["email"]["app_password"] = os.getenv("EMAIL_APP_PASSWORD")

    # Optional: Override LLM config from .env if provided
    config["llm_url"] = os.getenv("LLM_URL", config.get("llm_url"))
    config["model_name"] = os.getenv("MODEL_NAME", config.get("model_name"))

    return config