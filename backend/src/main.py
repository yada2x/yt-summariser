from transcript import TranscriptFetcher
from model import ChatBot

transcriptObj = TranscriptFetcher()
chatObj = ChatBot()

while True:
    print("Enter cmd: ")
    cmd = str(input())
    res = transcriptObj.get_transcript(cmd)    
    summary = chatObj.summarise(res)
    print(summary)
