# whisper-captions — Roadmap

Direction, not a schedule. Defects are tracked in
[`internal/known-issues.md`](./internal/known-issues.md); this page is about what the tool is
*for*.

## Where it is

It subtitles one video, several, or a folder; translates to English; and burns subtitles in. The
utility functions are tested; the pipeline is not.

## Considered

**Not overwriting the source video.** The most important change here. Burn-in writes
`{output_dir}/{basename}.mp4` with `output_dir` defaulting to `.`, so a careless invocation
destroys the input. Refusing to write over the input path would be a few lines.

**Cleaning up extracted audio.** WAVs accumulate in the temp directory forever.

**Making `--output_srt` do something.** It is accepted, documented, and ignored.

**Unique output naming.** Same-named videos in different directories overwrite each other.

**Preserving the input container.** Burn-in always produces MP4.

**Recursive directory scanning**, or a `--recursive` flag.

**Testing the pipeline.** Everything above lives in `cli.py`, which has no tests — the two facts
are related.

**A progress indicator.** Whisper reports progress with `--verbose`; a per-file summary would
help on long batches.

## Non-goals

**A hosted or API mode.** Local transcription is the reason this exists. Sending audio to a
service would make it a thin wrapper around something that already exists.

**Subtitle editing.** `.srt` is plain text and there are good editors for it. Generate, edit
elsewhere, burn in.

**Improving on Whisper's accuracy.** Post-processing transcripts to "fix" them means guessing at
what was said, and a confidently wrong subtitle is worse than an obviously garbled one. Pick a
bigger model instead.

**Translating to languages other than English.** Whisper does not offer it. Wrapping a separate
translator would be a different tool.

**Speaker diarisation.** Whisper does not identify speakers, and bolting on a second model would
double the dependency footprint of something that is already a large install.

## Contributing

Issues and pull requests welcome — see the
[Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md).
Refusing to overwrite the input file is the smallest change with the largest consequence.
