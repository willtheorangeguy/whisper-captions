# whisper-captions — Troubleshooting

## `ffmpeg` not found

```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

ffmpeg is a separate program, not a Python package. Install it and confirm with
`ffmpeg -version` — see [Installation](./installation.md). Reopen your terminal afterwards so a
changed `PATH` takes effect.

## It seems to hang after "Extracting audio..."

It is downloading the model — up to 1.5 GB, once. Model loading happens after extraction, which
is why the pause lands there. Watch `~/.cache/whisper` grow.

## Transcription takes forever

Expected on a CPU with the default `turbo`. Use `--model base` or `--model small`. Check whether
PyTorch can see your GPU:

```python
import torch; print(torch.cuda.is_available())
```

`False` on a machine with a CUDA card usually means the CPU-only PyTorch build was installed.

## `RuntimeError: CUDA out of memory`

The model does not fit in VRAM. Drop to a smaller one, or force CPU with
`CUDA_VISIBLE_DEVICES=""`.

## The `.srt` is empty or nearly so

| Cause | Check |
|---|---|
| No speech | Play the extracted WAV in the temp directory |
| Audio track missing | `ffprobe video.mp4` — a video with no audio stream produces nothing |
| Wrong language detected | Set `--language` explicitly |
| Very quiet audio | Normalise with ffmpeg first |

## The transcript is in the wrong language

Detection samples the opening audio. A video starting with music or silence can be misdetected
and stay wrong throughout. `--language fr` (or whichever) fixes it.

## `--task translate` produced the original language

`translate` targets English only. If the source **is** English, translate and transcribe do the
same thing.

## Two videos produced one output

Outputs are keyed by basename, so same-named files in different folders overwrite each other.
Process them separately, or rename. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## `--output_srt false` still wrote an `.srt`

The option has no effect — the `.srt` is always written to `--output_dir`. Delete it afterwards.
Recorded in [`internal/known-issues.md`](./internal/known-issues.md).

## My source video is gone

Burn-in writes `{output_dir}/{basename}.mp4`, and `--output_dir` defaults to `.`. Running
`--srt_only false` without `-o` on a file in the current directory overwrites it, and ffmpeg
truncates the output before reading, so the original is not recoverable.

**Always pass a separate `-o` with `--srt_only false`.** Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## The disk filled up

Extracted WAVs accumulate in the system temp directory — roughly 115 MB per hour of video, never
cleaned up. Clear them:

```bash
rm /tmp/*.wav                       # Linux, macOS — check before running
del %TEMP%\*.wav                    # Windows
```

Recorded in [`internal/known-issues.md`](./internal/known-issues.md).

## Burned subtitles are unreadable or missing

The filter needs an absolute path to the `.srt` — the code does that, but a hand-run ffmpeg
command often does not. On Windows, paths with colons need escaping in filter syntax.

Confirm the `.srt` itself is right first: play the video with it as an external subtitle track.

## The burned video is `.mp4` but my input was `.mkv`

The output container is always MP4. Not configurable.

## `no video files found in directory`

The scan is one level deep and filtered to `.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`. Name files
explicitly to bypass the filter.

## Still stuck

[Open an issue](https://github.com/willtheorangeguy/whisper-captions/issues/new/choose) with the
command, the error, your OS, whether a GPU is in use, and the model.
