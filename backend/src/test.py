from archive.transcript import TranscriptFetcher
from supadata_transcript_fetcher import TranscriptFetcherSupadata
from archive.model import ChatBot
from openrouter_model import OpenRouterChatBot
from dotenv import dotenv_values
config = dotenv_values(".env")

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

def test_supadata():
    # url = "https://www.youtube.com/watch?v=2crhrbqCLzU"
    # tFetch = TranscriptFetcherSupadata()
    # res = tFetch.fetch_transcript(url)

    bot = OpenRouterChatBot()
    summary = bot.summarise(config["HANK_SCRIPT"])
    print(summary)

if __name__ == '__main__':
    test_supadata()
