from pathlib import Path

BASE_DIR = Path(__file__).parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CLIPS_DIR = BASE_DIR / "clips"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"

WHISPER_MODEL = "base"
DEVICE = "cpu"

OUTPUT_WIDTH = 1440
OUTPUT_HEIGHT = 1080
OUTPUT_FPS = 60

MIN_CLIP_SECONDS = 60
MAX_CLIP_SECONDS = 60

for folder in [
    INPUT_DIR,
    OUTPUT_DIR,
    CLIPS_DIR,
    TRANSCRIPTS_DIR,
]:
    folder.mkdir(exist_ok=True)