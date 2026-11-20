
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

models = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

for model in models:
    print(f"\nTesting {model}...")
    try:
        response = client.models.generate_content(
            model=model,
            contents=(
                "Reply with: CrisisLink AI Gemini connection successful."
            ),
        )
        print("SUCCESS!")
        print(response.text)
        print(f"\nWorking model: {model}")
        break
    except Exception as e:
        print(f"Failed: {type(e).__name__}: {e}")
else:
    print("\nNeither model worked. Check the error messages above.")
