# whisper-captions — API

Primarily a CLI, but `whisper_captions.utils` is importable and useful on its own.

## `write_srt(transcript, file)`

Writes Whisper segments as SRT.

```python
from whisper_captions.utils import write_srt
import whisper

model = whisper.load_model("turbo")
result = model.transcribe("audio.wav")

with open("output.srt", "w", encoding="utf-8") as srt:
    write_srt(result["segments"], file=srt)
```

Each segment needs `start`, `end` (seconds, float) and `text`. Any iterable of dicts with those
keys works — the segments do not have to come from Whisper.

A literal `-->` in the text is rewritten to `->`, because SRT readers would otherwise parse it as
a timing line and lose everything after it.

## `format_timestamp(seconds, always_include_hours=False)`

```python
>>> format_timestamp(3661.5, always_include_hours=True)
'01:01:01,500'
>>> format_timestamp(61.5)
'01:01,500'
```

Asserts a non-negative input. Works in integer milliseconds after one `round`, so the parts
cannot disagree.

## `expand_video_paths(paths)`

```python
>>> expand_video_paths(["./videos", "extra.mp4"])
['./videos/a.mkv', './videos/b.mp4', 'extra.mp4']
```

Directories are listed **one level deep** and filtered to `.mp4`, `.mkv`, `.webm`, `.avi`,
`.mov`; results within a directory are sorted. Files named explicitly are passed through
whatever their extension.

Raises `FileNotFoundError` for a missing path or a directory with no videos.

## `filename(path)`

Basename without extension — `"/a/b/video.mp4"` → `"video"`. Used to key temporary audio and
name outputs, which is where the same-basename collision comes from; see
[`internal/known-issues.md`](./internal/known-issues.md).

## `str2bool(string)`

`"true"` / `"false"`, case-insensitive, raising `ValueError` otherwise. Used as an argparse
`type` so `--srt_only false` parses correctly — a bare `bool` type would make any non-empty
string `True`, including `"false"`.

## `VIDEO_EXTENSIONS`

```python
{".mp4", ".mkv", ".webm", ".avi", ".mov"}
```

Only filters directory scans.

## What is not importable

`cli.py`'s `get_audio` and `get_subtitles` are module-level and technically importable, but they
print progress, shell out to ffmpeg, and take a `transcribe` callable — written for `main()`
rather than for reuse.

## Version

```python
>>> import whisper_captions; whisper_captions.__version__
```
