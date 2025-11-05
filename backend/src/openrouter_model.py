import time
import requests
from logger_util import setup_logger
from dotenv import dotenv_values

config = dotenv_values("../.env")

CHAT_COMPLETION_URL = "https://openrouter.ai/api/v1/chat/completions"
COMPLETION_URL = "https://openrouter.ai/api/v1/completions"
MAX_RETRIES = 5

class OpenRouterChatBot:
   def __init__(self, model = "meta-llama/llama-3.3-8b-instruct:free"):
      self.logger = setup_logger(__name__, "logs/app.log")
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
         "prompt": self.system_prompt + "\n" + text,
         # "messages": self.messages,
      }
      for attempt in range(MAX_RETRIES):
         try:
            response = requests.post(
               url=COMPLETION_URL,
               headers = {
                  "Authorization": "Bearer " + config['OPENROUTER_API_KEY'],
                  "Content-Type": "application/json"
               },
               json=data,
               timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            message = result["choices"][0]["text"]
            self.messages.append({"role": "assistant", "content": message})
            return message
    
         except Exception as e:
            self.logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            time.sleep(2**attempt) # exponential backoff         

   def summarise(self, transcript, length = 500):
      return self.chat(f"Summarise the following transcript in {length} words.\n" + transcript)
   
   def setModel(self, model):
      self.model = model
