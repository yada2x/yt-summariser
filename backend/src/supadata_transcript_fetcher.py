import time
import json
from logger_util import setup_logger
from supadata import Supadata
from dotenv import dotenv_values
config = dotenv_values("../.env")


class TranscriptFetcherSupadata:
    def __init__(self):
        self.supadata = Supadata(config["SUPADATA_API_KEY"])
        self.logger = setup_logger(__name__, "../logs/app.log")

        with open("cache.json", "r") as cache:
            self.cache = json.load(cache)
    
    def _save_cache(self):
        with open("cache.json", "w") as file:
            json.dump(self.cache, file, indent=4)
            self.logger.info("Cache saved successfully!")

    def fetch_transcript(self, url: str) -> str:
        self.logger.info(f"Fetching transcript for [{url}]")
        if (self.cache.get(url)): # Try receiving from cache
            self.logger.info("Cache Hit!")
            return self.cache[url]
        
        try:
            transcript_result = self.supadata.transcript(
                url=url,
                text=True,
                mode="native" # save credits by fetching existing transcript
            )
            
            if hasattr(transcript_result, "job_id"):
                self.logger.info("Job Batch ID received")
                transcript_result = self.supadata.transcript.get_job_status(transcript_result.job_id)
                i = 1
                while (transcript_result.status != "completed"):
                    self.logger.info(f"Job fetch attempt {i}")
                    time.sleep(5)
                    i += 1
                    if (transcript_result.status == "failed"):
                        return None
                    transcript_result = self.supadata.transcript.get_job_status(transcript_result.job_id)
            else:
                self.logger.info("Transcript fetched!")
                self.cache[url] = transcript_result.content

            self.cache[url] = transcript_result.content
            self.logger.info("Cache Write!")  
            return transcript_result.content

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
