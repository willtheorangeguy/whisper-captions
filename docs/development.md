# whisper-captions — Development

## Setup

```bash
git clone https://github.com/willtheorangeguy/whisper-captions.git
cd whisper-captions
pip install -e ".[dev]"
pytest
```

Needs ffmpeg on the `PATH` to run the tool, though not to run the tests.

## Layout

```text
src/whisper_captions/
├── __init__.py    version
├── cli.py         argument parsing and the pipeline
└── utils.py       pure functions
tests/test_utils.py
```

A `src/` layout, so the installed package is what gets tested rather than the working directory.

## Tests

`tests/test_utils.py` covers everything in `utils.py`: `str2bool`, `format_timestamp`,
`write_srt`, `filename`, and `expand_video_paths`.

`cli.py` is untested. That is a defensible line — it is orchestration of ffmpeg and Whisper,
where a meaningful test needs both installed, a real video, and minutes of runtime — but it does
mean the pipeline's own logic (output paths, the `srt_only` branch, flag handling) has no
coverage at all, and that is where this project's defects are.

If you add anything to `cli.py`, consider whether the decision could live in `utils.py` instead,
where it can be tested.

## Conventions

- **Pure logic in `utils.py`, side effects in `cli.py`.** It is what makes the suite possible.
- **Booleans through `str2bool`**, so `--flag false` behaves.
- **Absolute paths for ffmpeg filter arguments.** Relative paths resolve against ffmpeg's own
  working directory.
- Extra `argparse` arguments are forwarded to `model.transcribe` as `**args`, so adding a
  Whisper option usually means only adding the parser entry.

## Manual testing

The tests cannot cover the pipeline, so exercise it by hand after touching `cli.py`:

```bash
whisper-captions clip.mp4 --model tiny
whisper-captions ./folder --model tiny -o ./out
whisper-captions clip.mp4 --model tiny --srt_only false -o ./out
whisper-captions clip.mp4 --model tiny --task translate
```

`tiny` keeps each of those to seconds.

## Releasing

Create a GitHub release; `.github/workflows/publish.yml` publishes to PyPI. Bump the version in
`pyproject.toml` and `__init__.py` first, together.

## CI

`.github/workflows/test.yml` runs the suite on push and pull request.

## Recording defects

Bugs found while working here go in [`internal/known-issues.md`](./internal/known-issues.md)
rather than being fixed in passing, unless fixing them is the job you are on.
