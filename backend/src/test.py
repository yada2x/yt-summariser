import atexit
import time

from archive.transcript import TranscriptFetcher
from supadata_transcript_fetcher import TranscriptFetcherSupadata
from archive.model import ChatBot
from openrouter_model import OpenRouterChatBot
from dotenv import dotenv_values
config = dotenv_values("../.env")

urls = ["https://www.youtube.com/watch?v=O1e4zNfyowA", "https://www.youtube.com/watch?v=2crhrbqCLzU", 
        "https://www.youtube.com/watch?v=gU2AhTTmLCU", "https://www.youtube.com/watch?v=8anNWhbFCmA", 
        "https://www.youtube.com/watch?v=Xxr4l00hkwA", "https://www.youtube.com/watch?v=Lqaq4lVwuVQ"]

def test_original():
    transcriptObj = TranscriptFetcher()
    chatObj = ChatBot()

    while True:
        print("Enter cmd: ")
        cmd = str(input())
        res = transcriptObj.get_transcript(cmd)    
        summary = chatObj.summarise(res)
        print(summary)

def test_bot():
    bot = ChatBot()
    summary = bot.summarise(config["HANK_SCRIPT"])
    print(summary)

def test_openrouter():
    url = "https://www.youtube.com/watch?v=2crhrbqCLzU"
    tFetch = TranscriptFetcherSupadata()

    for url in urls:
        res = tFetch.fetch_transcript(url)
        bot = OpenRouterChatBot()
        summary = bot.summarise(res)
        print(f"--TRANSCRIPT START--\n{summary}\n-- TRANSCRIPT END --\n")

def test_supadata():
    tFetch = TranscriptFetcherSupadata()
    atexit.register(tFetch._save_cache)
    
    for url in urls:
        tFetch.fetch_transcript(url)

if __name__ == '__main__':
    test_openrouter()
