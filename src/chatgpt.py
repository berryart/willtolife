import json
import openai


class OpenAI:
  def __init__(self) -> None:
    with open("credentials.json", "r") as c:
      creds = json.load(c)
      openai.api_key = creds["openai"]["key"]


  def personalize_text(self, text) -> str:
    response = openai.chat.completions.create(
      model="gpt-4", 
      messages=[
            {"role": "user", "content": "Rephrase text in the following message to make it sound from the first person, like speaking from the 'I'."},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content
