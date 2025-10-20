import time
import threading
from functools import lru_cache
from supadata import Supadata
from dotenv import dotenv_values

config = dotenv_values(".env")

class TranscriptFetcher:
    def __init__(self):
        self.supadata = Supadata(config["SUPADATA_API_KEY"])

    @lru_cache(maxsize=100)
    def fetch_transcript(self, url: str) -> str:
        try:
            transcript_result = self.supadata.transcript(
                url=url,
                lang="en",
                text=True,
                mode="auto")
            
            if hasattr(transcript_result, "job_id"):
                result = self.supadata.transcript.get_job_status(transcript_result.job_id)
                return result
            else:
                return transcript_result.content

        except Exception as e:
            raise e

