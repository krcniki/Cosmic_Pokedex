from google import genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_content(
        model='models/gemini-2.0-flash-lite', 
        contents="Say 'System Online'"
    )
    print(f"✅ Success: {response.text}")
except Exception as e:
    print(f"❌ Result: {e}")