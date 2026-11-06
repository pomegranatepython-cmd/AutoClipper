import json
import sys
from pathlib import Path

from config import (
    CLIPS_DIR,
    TRANSCRIPTS_DIR,
    MIN_CLIP_SECONDS,
    MAX_CLIP_SECONDS
)

KEYWORDS = {
    "surprise": 3,
    "secret": 3,
    "never": 2,
    "truth": 3,
    "impossible": 3,
    "remember": 2,
    "betray": 3,
    "danger": 3,
    "finally": 2,
    "wait": 1,
    "sorry": 1,
    "love": 1,
    "why": 1,
    "what": 1
}


def score_text(text):
    text = text.lower()
    score = 0

    for word, weight in KEYWORDS.items():
        if word in text:
            score += weight

    if "!" in text:
        score += 2

    if "?" in text:
        score += 1

    return score


def detect_highlights(transcript_path):
    transcript_path = Path(transcript_path)

    segments = json.loads(
        transcript_path.read_text(encoding="utf-8")
    )

    if not segments:
        print("No transcript segments found.")
        return

    candidates = []
    video_end = max(s["end"] for s in segments)

    window = MAX_CLIP_SECONDS
    step = 10

    start = 0

    while start < video_end:
        end = min(start + window, video_end)

        if end - start < MIN_CLIP_SECONDS:
            break

        text_parts = [
            s["text"]
            for s in segments
            if s["start"] < end and s["end"] > start
        ]

        combined_text = " ".join(text_parts)
        score = score_text(combined_text)

        if score > 0:
            candidates.append({
                "start": start,
                "end": end,
                "duration": end - start,
                "score": score,
                "text": combined_text
            })

        start += step

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    selected = []

    for candidate in candidates:
        overlap = any(
            candidate["start"] < item["end"]
            and candidate["end"] > item["start"]
            for item in selected
        )

        if not overlap:
            selected.append(candidate)

    output = CLIPS_DIR / (
        f"{transcript_path.stem}_highlights.json"
    )

    output.write_text(
        json.dumps(selected, indent=2),
        encoding="utf-8"
    )

    print(f"Found {len(selected)} candidate highlights")
    print(f"Saved: {output}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python highlight_ai.py transcript.json")
    else:
        detect_highlights(sys.argv[1])