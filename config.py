import os
from pathlib import Path


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[7:].strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')

        if key:
            os.environ.setdefault(key, value)


PROJECT_DIR = Path(__file__).resolve().parent
load_env_file(PROJECT_DIR / ".env")


class Config:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()


config_obj = Config()
