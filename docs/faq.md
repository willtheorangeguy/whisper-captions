# whisper-captions — FAQ

## Does anything get uploaded?

No. Whisper runs locally through PyTorch. There is no API key, no account, and no network call
after the one-time model download.

That is the reason to use this over a hosted service — for recordings you would not hand to a
third party, local is the only option.

## Why is it so slow?

Transcription is compute-bound, and the default `turbo` model assumes a GPU. On a CPU it can take
longer than the video's own runtime.

```bash
whisper-captions video.mp4 --model base
```

is dramatically faster. See [Configuration](./configuration.md).

## Why did it stall halfway through the first run?

It is downloading the model — about 1.5 GB for `turbo`. That happens **after** audio extraction,
so the pause lands at an odd-looking point. Cached afterwards.

## Do I need a GPU?

No, but it is roughly an order of magnitude faster with one. CPU-only works fine with a smaller
model.

## Do I need ffmpeg separately?

Yes. `ffmpeg-python` is a wrapper around the `ffmpeg` binary, not a bundled copy. See
[Installation](./installation.md).

## Can it translate into a language other than English?

No. Whisper's `translate` task only targets English. `--language` sets the **source**, not the
destination.

## Why is the transcript in the wrong language?

Detection samples the opening audio, so a video that starts with music, silence, or another
language can be detected wrongly and stay wrong throughout. Set `--language` explicitly.

## Does it search subdirectories?

No. A directory argument is scanned one level deep. Pass subdirectories explicitly, or use your
shell's globbing.

## Two videos with the same name produced one output

They collide: temporary audio and output files are keyed by basename, so `a/ep1.mp4` and
`b/ep1.mp4` overwrite each other. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## `--output_srt false` still left an `.srt` behind

Known — the option currently has no effect. See
[`internal/known-issues.md`](./internal/known-issues.md).

## My source video was overwritten

Burn-in writes `{output_dir}/{basename}.mp4`, and `--output_dir` defaults to `.`. Always pass a
separate `-o` with `--srt_only false`. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## The subtitles are inaccurate

Try a larger model, set `--language` explicitly, and check the audio itself — Whisper struggles
with heavy background noise, overlapping speakers, and very quiet recordings. Nothing here can
improve on what Whisper produces.

## Can I edit the subtitles afterwards?

Yes — `.srt` is plain text. Generate the `.srt`, correct it, then burn it in with ffmpeg
directly if you want it in the video.

## What video formats work?

`.mp4`, `.mkv`, `.webm`, `.avi`, `.mov` when scanning a directory. Named explicitly, anything
ffmpeg can read. Burn-in always outputs `.mp4`.

## Is my disk filling up?

Possibly. Extracted WAVs go to the system temp directory and are not deleted — a 16 kHz mono WAV
is roughly 115 MB per hour of video. See
[`internal/known-issues.md`](./internal/known-issues.md).
