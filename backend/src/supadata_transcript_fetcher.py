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
                text=True,
                mode="native" # save credits by fetching existing transcript
            )
            
            if not hasattr(transcript_result, "job_id"):
                return transcript_result.content

            print("Processing job ", transcript_result.job_id)
            result = self.supadata.transcript.get_job_status(transcript_result.job_id)
            while (result.status != "completed"):
                if (result.status == "failed"):
                    return "FAILED"
                time.sleep(5)
                result = self.supadata.transcript.get_job_status(transcript_result.job_id)
            print("Processed job!")
            return result.content

        except Exception as e:
            print(e)

