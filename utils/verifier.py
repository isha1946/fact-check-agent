import cohere
import os
import time
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(st.secrets["COHERE_API_KEY"])

def verify_claim(claim, web_results):

    combined_text = ""

    for result in web_results:
        combined_text += result["content"] + "\n"

    prompt = f"""
    Claim:
    {claim}

    Web Evidence:
    {combined_text}

    Determine if the claim is:

    - Verified
    - Inaccurate
    - False

    Also provide:
    - corrected fact
    - short explanation

    Return in this format:

    Status:
    Correct Fact:
    Explanation:
    """

    for attempt in range(3):

        try:

            response = co.chat(
                model="command-a-03-2025",
                message=prompt,
                temperature=0
            )

            return response.text

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")

            time.sleep(3)

    return "Verification failed"
