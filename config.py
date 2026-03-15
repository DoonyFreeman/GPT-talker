import os


class Config:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()


config_obj = Config()
