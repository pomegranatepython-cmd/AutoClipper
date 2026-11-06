
import json
import subprocess
import sys
from pathlib import Path

from config import CLIPS_DIR, OUTPUT_DIR


def generate_clips(video_path, highlights_path):
    video_path = Path(video_path)
    highlights_path = Path(highlights_path)

    if not video_path.exists():
        print("Video not found!")
        return

    if not highlights_path.exists():
        print("Highlights file not found!")
        return

    highlights = json.loads(
        highlights_path.read_text(encoding="utf-8")
    )

    if not highlights:
        print("No highlights found!")
        return

    for index, clip in enumerate(highlights, start=1):
        start = clip["start"]
        duration = clip["end"] - start

        output = OUTPUT_DIR / (
            f"{video_path.stem}_clip_{index}.mp4"
        )

        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", str(video_path),
            "-t", str(duration),
            "-map", "0:v:0",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-fps_mode", "passthrough",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output)
        ]

        print(f"Generating clip {index}/{len(highlights)}...")

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as error:
            print(f"Failed to generate clip {index}: {error}")
            return

    print(f"Generated {len(highlights)} clips successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python clip_generator.py "
            "video.mp4 highlights.json"
        )
    else:
        generate_clips(sys.argv[1], sys.argv[2])
