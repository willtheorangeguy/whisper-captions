# whisper-captions — Architecture

Two modules. `cli.py` runs the pipeline; `utils.py` holds the pure functions.

```text
video files / directories
   └── expand_video_paths()        one level deep, by extension
          └── get_audio()          ffmpeg → 16 kHz mono WAV in the temp dir
                 └── model.transcribe()   Whisper, locally
                        └── write_srt()   segments → .srt
                               └── (optional) ffmpeg subtitles filter → .mp4
```

## `expand_video_paths`

Takes the positional arguments and returns a flat list of files. A directory is listed with
`os.listdir` — **one level, no recursion** — and filtered by `VIDEO_EXTENSIONS`. A directory
containing no videos, or a path that does not exist, raises `FileNotFoundError`, which `main`
turns into a clean `parser.error` rather than a traceback.

## `get_audio`

One ffmpeg call per video:

```text
acodec=pcm_s16le, ac=1, ar=16k
```

Whisper resamples to 16 kHz mono internally, so extracting in that form directly avoids a second
conversion. Output goes to the system temp directory, keyed by the input's **basename**.

Two consequences: files with the same basename in different directories overwrite each other,
and nothing deletes the WAVs afterwards. Both are in
[`internal/known-issues.md`](./internal/known-issues.md).

## Transcription

`whisper.load_model(model_name)` then `model.transcribe(audio_path, **args)`. Everything left in
`args` after the explicit pops — `task`, `verbose`, and `language` when set — is forwarded
straight through, which is why any Whisper argument the parser accepts reaches the model without
plumbing.

Model loading happens **after** audio extraction, so the first run pauses at what looks like a
random point while it downloads.

`warnings.filterwarnings("ignore")` wraps the call to silence PyTorch's FP16-on-CPU notice, then
resets to `"default"` — which restores the default filter set rather than whatever was there
before.

## `write_srt`

Numbers segments from 1 and formats `HH:MM:SS,mmm --> HH:MM:SS,mmm`, taking `start`, `end`, and
`text` from each Whisper segment.

One detail worth keeping: `text.replace('-->', '->')`. A literal `-->` inside subtitle text would
be parsed as a timing line by SRT readers, corrupting everything after it. Rewriting it is the
standard defence.

`format_timestamp` works entirely in integer milliseconds after a single `round`, so the
components cannot disagree through floating-point drift.

## Burn-in

When `--srt_only false`:

```python
ffmpeg.concat(
    video.filter('subtitles', os.path.abspath(srt_path),
                 force_style="OutlineColour=&H40000000,BorderStyle=3"),
    audio, v=1, a=1
).output(out_path).run(quiet=True, overwrite_output=True)
```

The `subtitles` filter rasterises the SRT into the frames, so the result plays anywhere without
subtitle support. `BorderStyle=3` draws a translucent box behind the text, which keeps it
readable over light footage.

The absolute path matters: ffmpeg's filter syntax treats the argument specially, and a relative
path resolves against ffmpeg's own working directory.

**`out_path` is always `{output_dir}/{basename}.mp4`** — the input container is not preserved,
and with the default `output_dir` of `.` it can be the input path itself. See
[`internal/known-issues.md`](./internal/known-issues.md).

## Why ffmpeg twice

Once to extract audio for Whisper, once to burn subtitles in. They are separate because most runs
only need the first — the default is `.srt` output, and the second pass is the expensive one.

## Tests

`tests/test_utils.py` covers `str2bool`, `format_timestamp`, `write_srt`, `filename`, and
`expand_video_paths` — everything in `utils.py`, which is everything that does not need ffmpeg,
a model, or a video file.

`cli.py` is untested, being almost entirely orchestration of two external programs.
