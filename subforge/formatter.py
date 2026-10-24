"""
Professional subtitle formatting conforming to standard broadcast guidelines:
- Maximum 42 characters per line.
- Maximum 2 lines per subtitle block.
- Correct WebVTT and SubRip (SRT) timecodes.
"""
from dataclasses import dataclass

@dataclass
class SubtitleSegment:
    start_seconds: float
    end_seconds: float
    text: str

def format_timestamp(seconds: float, srt_format: bool = False) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if srt_format:
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"

def wrap_line_42chars(text: str, max_chars: int = 42) -> str:
    """Wraps text into at most 2 lines of max_chars length."""
    words = text.strip().split()
    lines = []
    current_line = []
    
    for word in words:
        if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_chars:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    # Cap at 2 lines
    return "\n".join(lines[:2])

def format_vtt(segments: list[SubtitleSegment]) -> str:
    out = ["WEBVTT\n"]
    for seg in segments:
        t_start = format_timestamp(seg.start_seconds)
        t_end = format_timestamp(seg.end_seconds)
        text = wrap_line_42chars(seg.text)
        out.append(f"{t_start} --> {t_end}\n{text}\n")
    return "\n".join(out)

def format_srt(segments: list[SubtitleSegment]) -> str:
    out = []
    for i, seg in enumerate(segments, start=1):
        t_start = format_timestamp(seg.start_seconds, srt_format=True)
        t_end = format_timestamp(seg.end_seconds, srt_format=True)
        text = wrap_line_42chars(seg.text)
        out.append(f"{i}\n{t_start} --> {t_end}\n{text}\n")
    return "\n".join(out)
