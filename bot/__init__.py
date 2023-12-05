import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Start Write-Ahead Logs (For app status and debugging)
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# read messages JSON file
BASE_DIR = os.path.join(Path(__file__).parent.parent)
messages = messages = json.load(
    open(os.path.join(BASE_DIR, "bot", "messages.json"), encoding="utf-8")
)
