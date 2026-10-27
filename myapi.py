import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Find and load the .env file beside myapi.py
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / "env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


class API:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                f"Gemini API key is missing.\n"
                f"Check this file: {ENV_FILE}\n"
                "It must contain GEMINI_API_KEY=your_key"
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.5-flash-lite"

    def ask_gemini(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()

    def sentiment_analysis(self, text):
        prompt = f"""
        Analyze the sentiment of this text.

        Return ONLY a valid JSON object containing:
        compound, pos, neg, neu.

        compound must be between -1 and 1.
        pos, neg and neu must be between 0 and 1.
        The positive, negative and neutral scores should sum
        to approximately 1.

        Do not include Markdown code fences.

        Text: {text}
        """

        result = self.ask_gemini(prompt)
        result = result.replace("```json", "")
        result = result.replace("```", "").strip()

        scores = json.loads(result)

        return {
            "compound": float(scores["compound"]),
            "pos": float(scores["pos"]),
            "neg": float(scores["neg"]),
            "neu": float(scores["neu"])
        }

    def ner(self, text):
        prompt = f"""
        Identify named entities in this text.

        Return ONLY a valid JSON array.
        Each object must contain "text" and "label".
        Use labels such as PERSON, LOCATION, ORGANIZATION,
        DATE, and other suitable entity types.
        Return [] if no entities are found.
        Do not include Markdown code fences.

        Text: {text}
        """

        result = self.ask_gemini(prompt)
        result = result.replace("```json", "")
        result = result.replace("```", "").strip()

        entities = json.loads(result)

        return [
            (item["text"], item["label"])
            for item in entities
        ]

    def emotion_prediction(self, text):
        prompt = f"""
        Identify the main emotion in this text.

        Choose one:
        Happy, Sad, Angry, Fear, Love, Surprise,
        Neutral, or No clear emotion detected.

        Return only the emotion name.

        Text: {text}
        """

        emotion = self.ask_gemini(prompt)
        emotion = emotion.strip().strip('"').strip("'")

        allowed = {
            "Happy",
            "Sad",
            "Angry",
            "Fear",
            "Love",
            "Surprise",
            "Neutral",
            "No clear emotion detected"
        }

        if emotion not in allowed:
            return "No clear emotion detected"

        return emotion