import os

class ai_enums:
    S_API_URL = os.getenv("LLM_URL", "http://host.docker.internal:11434/api/chat")
    S_TIMEOUT_SECONDS = 30
    S_DEFAULT_MODEL = "llama2-uncensored:latest"
    S_SUMMARY_MODEL = "tinyllama"
