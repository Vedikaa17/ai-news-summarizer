import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def summarize_article(title, description):
    """
    Groq LLM ka use karke article ka short summary aur sentiment nikalta hai.
    Return: dict with 'summary' and 'sentiment'
    """
    prompt = f"""
You are a news summarization assistant. Given the news title and description below, do two things:

1. Write a very short 2-line summary in simple English.
2. Classify the sentiment as exactly one word: Positive, Negative, or Neutral.

Title: {title}
Description: {description}

Respond ONLY in this exact format (no extra text):
Summary: <your 2-line summary>
Sentiment: <Positive/Negative/Neutral>
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )

        output = response.choices[0].message.content.strip()

        # Output ko parse karke summary aur sentiment alag karte hain
        summary = ""
        sentiment = "Neutral"

        for line in output.split("\n"):
            if line.lower().startswith("summary:"):
                summary = line.split(":", 1)[1].strip()
            elif line.lower().startswith("sentiment:"):
                sentiment = line.split(":", 1)[1].strip()

        return {"summary": summary, "sentiment": sentiment}

    except Exception as e:
        print(f"Error summarizing: {e}")
        return {"summary": description[:150] + "...", "sentiment": "Neutral"}
