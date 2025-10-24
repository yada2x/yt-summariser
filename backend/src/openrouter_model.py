import time
import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

class OpenRouterChatBot:
   def __init__(self, model = "google/gemini-2.0-flash-exp:free"):
      self.model = model # default
      self.system_prompt = "You are a helpful AI assistant who will receive a text transcript from a video. \
         Your job is to summarise it, detailing the main points and key takeaways. You will also be asked to answer questions about the content of the transcript \
         Your primary goal is to deliver clear and concise summaries and responses."
      self.messages = [
         {
            "role": "system", "content": self.system_prompt,
         }
      ]

   def chat(self, text):
      self.messages.append({"role": "user", "content": text})
      data = {
      "model": self.model,
      "messages": self.messages,
      }

      while True:
         response = requests.post(
            url=BASE_URL,
            headers = {
               "Authorization": "Bearer " + config['OPENROUTER_API_KEY'],
               "Content-Type": "application/json"
            },
            json=data
         )

         result = response.json()
         try:
            message = result["choices"][0]["message"]["content"]
            self.messages.append(message)
            return message
         except:
            print(f"ERROR: Status {result['error']['code']} {result['error']['message']}")
            print(result)
         
         time.sleep(5)         

   def summarise(self, transcript, length = 500):
      return self.chat(f"Summarise the following transcript in {length} words.\n" + transcript)
   
   def setModel(self, model):
      self.model = model
