from ollama import Client
from typing import List, Dict
import threading
import time

class Options:
   def __init__(self, options: List[Dict]):
      self.body = options
    
    # define a way to interate through options, all should be done with system role

def spinner(done: threading.Event):
    chars = "|/-\\"
    start = time.time()
    i = 0
    while not done.is_set():
        elapsed = time.time() - start
        print(f"\rProcessing... {chars[i % len(chars)]} "
              f"[{elapsed:.1f}s]", end="", flush=True)
        i += 1
        time.sleep(0.1)
    elapsed = time.time() - start
    print(f"\rProcessing... Done! [{elapsed:.1f}s]    ")

class ChatBot:
    def __init__(self, model = "deepseek-r1:1.5b"):
      self.model = model
      self.system_prompt = "You are a helpful AI assistant who will receive a text transcript from a video. \
        Your job is to summarise it, detailing the main points and key takeaways."
      self.client = Client()

    def setModel(self, model: str):
       self.model = model

    def summarise(self, transcript: str) -> str:

      done = threading.Event()
      t = threading.Thread(target=spinner, args = (done,))
      t.start()

      try:
        response = self.client.chat(
          model = self.model,
          messages = [
              {"role": "system", "content": self.system_prompt},
              {"role": "user", "content": transcript}
            ],
          stream = False
        )
      finally:
         done.set()
         t.join()
      clean_response = response.message.content.split("</think>")[-1].rstrip()
      return clean_response

