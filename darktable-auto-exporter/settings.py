import dotenv
import os

dotenv.load_dotenv()
RAW_DIRECTORY = os.getenv("RAW_DIRECTORY")
OUT_DIRECTORY = os.getenv("OUT_DIRECTORY")
OUT_FORMAT = os.getenv("OUT_FORMAT", "jpg")
