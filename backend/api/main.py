from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.openrouter_model import OpenRouterChatBot
from src.supadata_transcript_fetcher import TranscriptFetcherSupadata

app = FastAPI()
bot = OpenRouterChatBot()
fetcher = TranscriptFetcherSupadata()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")

    if not message:
        return JSONResponse({"error": "Missing `message` parameter"}, status_code=400)

    try:
        reply = bot.chat(message)
        return JSONResponse({
            "user_message": message,
            "bot_message": reply
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/transcript")
async def transcript(request: Request):
    print("TRANSCRIPT HIT")
    data = await request.json()
    url = data.get("url")

    if not url:
        return JSONResponse({"error": "Missing `url` parameter"}, status_code=400)
    
    try:
        transcript_result = fetcher.fetch_transcript(url)
        if not transcript_result:
            return JSONResponse({"error": "Could not fetch transcript"}, status_code=500)
    
        summary_result = bot.summarise(transcript_result)
        return JSONResponse({
            "url": url,
            "message": summary_result
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
def main():
    return {"message": "API is running!"}
