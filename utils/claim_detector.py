import cohere
import os
import time
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(st.secrets["COHERE_API_KEY"])

def extract_claims(text):

    prompt = f"""
    Extract factual claims from the following text.

    Focus on:
    - statistics
    - numbers
    - dates
    - financial data
    - technical claims

    Return only bullet points.

    Text:
    {text[:2500]}
    """

    for attempt in range(3):

        try:

            response = co.chat(
                model="command-a-03-2025",
                message=prompt,
                temperature=0
            )

            claims = response.text

            return claims.split("\n")

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")

            time.sleep(3)

    return ["Could not extract claims"]
