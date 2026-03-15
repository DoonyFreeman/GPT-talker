from google import genai
from config import config_obj
client = genai.Client(api_key=config_obj.gemini_api_key)



def main():
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Сколько людей живет в Усурийске?",
    )
    print(response.text)


if __name__ == "__main__":
    main()