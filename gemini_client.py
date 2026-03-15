from functools import lru_cache

from google import genai
from google.genai import errors as genai_errors

from config import config_obj


MODEL_NAME = "gemini-3-flash-preview"


class GeminiClientError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not config_obj.gemini_api_key:
        raise GeminiClientError(
            "GEMINI_API_KEY is not configured. Export a new Gemini API key before starting FastAPI.",
            status_code=503,
        )

    return genai.Client(api_key=config_obj.gemini_api_key)


def map_genai_error(error: Exception) -> GeminiClientError:
    status_code = getattr(error, "status_code", None) or getattr(error, "code", None) or 502
    message = str(error).strip() or "Gemini API request failed."

    if "reported as leaked" in message.lower():
        return GeminiClientError(
            "Gemini rejected the API key because it is marked as leaked. Create a new key and set GEMINI_API_KEY.",
            status_code=503,
        )

    if isinstance(status_code, str):
        try:
            status_code = int(status_code)
        except ValueError:
            status_code = 502

    return GeminiClientError(message, status_code=int(status_code))


def get_answer_from_gemini(prompt: str) -> str:
    normalized_prompt = prompt.strip()
    if not normalized_prompt:
        raise GeminiClientError("Prompt must not be empty.", status_code=400)

    try:
        response = get_client().models.generate_content(
            model=MODEL_NAME,
            contents=normalized_prompt,
        )
    except GeminiClientError:
        raise
    except genai_errors.ClientError as error:
        raise map_genai_error(error) from error
    except Exception as error:
        raise GeminiClientError(f"Gemini request failed: {error}", status_code=502) from error

    answer = getattr(response, "text", None)
    if not answer:
        raise GeminiClientError("Gemini returned an empty response.", status_code=502)

    return answer
