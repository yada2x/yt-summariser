import time
import threading
from functools import lru_cache
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

class TranscriptFetcher:
    def __init__(self, min_interval_seconds: float = 1.0):
        self.transcript_api = YouTubeTranscriptApi()
        self.min_interval = min_interval_seconds
        self._lock = threading.Lock()
        self._last_request_ts = time.time()

    def _throttle(self):
        with self._lock:
            now = time.time()
            elapsed = now - self._last_request_ts
            wait = self.min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            self._last_request_ts = time.time()
    
    def get_video_id(self, url: str) -> str:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return url

    @lru_cache(maxsize=4096)
    def get_transcript(self, url: str) -> str:
        backoff = 1.0
        for attempt in range(4):
            try:
                self._throttle()
                id = self.get_video_id(url)
                fetched_transcript = self.transcript_api.fetch(id)
                return " ".join(snip.text for snip in fetched_transcript)
            except (TranscriptsDisabled, NoTranscriptFound):
                raise
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(backoff)
                backoff *= 2.0
