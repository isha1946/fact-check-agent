from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_claim(claim):

    response = client.search(
        query=claim,
        search_depth="advanced",
        max_results=3
    )

    results = []

    for item in response["results"]:
        results.append({
            "title": item["title"],
            "content": item["content"],
            "url": item["url"]
        })

    return results