import os
from typing import Iterator, TextIO

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".avi", ".mov"}


def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    for i, segment in enumerate(transcript, start=1):
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
            f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )


def filename(path):
    return os.path.splitext(os.path.basename(path))[0]


def expand_video_paths(paths):
    """Expand any directories in paths to the video files they contain."""
    expanded = []
    for path in paths:
        if os.path.isdir(path):
            videos = sorted(
                os.path.join(path, name)
                for name in os.listdir(path)
                if os.path.isfile(os.path.join(path, name))
                and os.path.splitext(name)[1].lower() in VIDEO_EXTENSIONS
            )
            if not videos:
                raise FileNotFoundError(f"no video files found in directory: {path}")
            expanded.extend(videos)
        elif os.path.isfile(path):
            expanded.append(path)
        else:
            raise FileNotFoundError(f"no such file or directory: {path}")
    return expanded
