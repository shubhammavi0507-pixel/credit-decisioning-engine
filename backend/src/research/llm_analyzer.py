import openai
from config import OPENAI_API_KEY

class LLMAnalyzer:

    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def summarize(self, text):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You are a financial analyst."},
                {"role":"user","content":f"Summarize risk insights:\n{text}"}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content
