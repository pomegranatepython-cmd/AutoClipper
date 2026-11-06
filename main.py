import sys
from pathlib import Path

from scene_detector import detect_scenes
from transcriber import transcribe_video
from highlight_ai import detect_highlights
from clip_generator import generate_clips

def process_video(video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        print("Video not found!")
        return

    print("\n[1/4] Detecting scenes...")
    detect_scenes(video_path)

    print("\n[2/4] Transcribing video...")
    transcribe_video(video_path)

    transcript = Path("transcripts") / f"{video_path.stem}.json"

    print("\n[3/4] Finding highlights...")
    detect_highlights(transcript)

    highlights = Path("clips") / f"{video_path.stem}_highlights.json"

    print("\n[4/4] Generating clips...")
    generate_clips(video_path, highlights)

    print("\nPROCESSING COMPLETE!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py input/video.mp4")
    else:
        process_video(sys.argv[1])