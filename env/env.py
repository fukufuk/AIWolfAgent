import os

from dotenv import load_dotenv


def load_env():
    ENV_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(ENV_DIR, ".env"))
    if os.environ.get("OPENAI_API_KEY") is not None:
        print("success to load .env")
    return
