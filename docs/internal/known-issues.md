# Known Issues — whisper-captions

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.


**5 open:** 1 high, 3 medium, 1 low.

## 1. Burning subtitles in with the default output directory overwrites the source video

**Severity:** High  
**Where:** `src/whisper_captions/cli.py` -> `main`, `out_path`

**What:** `out_path = os.path.join(output_dir, f"{filename(path)}.mp4")` and `--output_dir` defaults to `"."`. For the natural invocation `whisper-captions video.mp4 --srt_only false` run in the directory holding `video.mp4`, `out_path` **is** the input path. The ffmpeg call uses `overwrite_output=True`, and nothing compares the output path to the input.

**Why it matters:** The source video is destroyed. ffmpeg truncates the output file as it opens it, so the original is not merely replaced by the subtitled version -- it is gone before the encode finishes, and a failed or interrupted encode leaves nothing at all. There is no confirmation prompt, no warning, and no backup. The default value of `--output_dir` is what makes this reachable by accident rather than by carelessness: every other mode of the tool is non-destructive, so there is no reason to expect this one is not.

**Suggested fix:** Refuse to run when `os.path.abspath(out_path) == os.path.abspath(path)` and exit with an explanatory error. Better: suffix burned output (`{name}.subtitled.mp4`) so the collision cannot arise, and preserve the input's container rather than forcing `.mp4`.

## 2. --output_srt is accepted, documented, and ignored

**Severity:** Medium  
**Where:** `src/whisper_captions/cli.py` -> `get_subtitles`

**What:** `get_subtitles(audio_paths, output_srt, output_dir, transcribe)` declares `output_srt` and never references it. The body always writes `srt_path = os.path.join(output_dir, f"{filename(path)}.srt")`. `main` passes `output_srt or srt_only`, so the argument is computed and discarded.

**Why it matters:** The flag exists specifically to control whether the intermediate `.srt` is kept when producing a subtitled video, and it does nothing -- the `.srt` always lands in the output directory. A user who set `--output_srt false` to get a clean output folder finds it littered anyway, and has no reason to suspect the option rather than their own command. The unused parameter in the signature makes the function read as though the behaviour is there.

**Suggested fix:** Write the `.srt` to a temporary directory when `output_srt` is false and `srt_only` is false, deleting it after the burn-in pass -- which is what the parameter's presence implies was intended. Removing the parameter and the documented flag would also be honest, if less useful.

## 3. Extracted WAV files accumulate in the temp directory and are never deleted

**Severity:** Medium  
**Where:** `src/whisper_captions/cli.py` -> `get_audio`

**What:** Each video is decoded to `{tempdir}/{basename}.wav` at 16 kHz mono `pcm_s16le`. The paths are returned and used, and nothing removes them -- no `try/finally`, no `TemporaryDirectory`, no cleanup at exit.

**Why it matters:** 16 kHz mono 16-bit is about 115 MB per hour of source video. Subtitling a season of television leaves several gigabytes behind, and the natural use of this tool is batch runs over folders. Temp directories are cleared on reboot on some systems and never on others, so on a server this simply grows. Nothing reports it, and the files are named after the videos, so anyone who does find them has to work out what wrote them.

**Suggested fix:** Use `tempfile.TemporaryDirectory()` as a context manager around the whole pipeline, or delete each WAV after its transcription completes. The latter also caps peak usage at one file rather than the whole batch.

## 4. Outputs are keyed by basename, so same-named videos in different folders collide

**Severity:** Medium  
**Where:** `src/whisper_captions/cli.py` -> `get_audio`, `get_subtitles`; `src/whisper_captions/utils.py` -> `filename`

**What:** `filename(path)` returns the basename without extension, and it names the temporary WAV, the `.srt`, and the burned `.mp4`. Passing `a/ep1.mp4 b/ep1.mp4` in one run gives both the same temporary audio path and the same output paths.

**Why it matters:** The second video's audio overwrites the first's before the first is transcribed in some orderings, and its `.srt` overwrites the first's regardless -- so one input silently produces no output, or worse, an output containing the other video's transcript. `ep1.mp4` per season directory is exactly how television and course recordings are organised, and the tool advertises batch processing, so this is a normal input rather than a contrived one. Nothing warns, and the run reports success.

**Suggested fix:** Derive output names from a path that disambiguates -- the parent directory plus the basename, or a hash of the absolute path for the temporary audio. At minimum, detect duplicate basenames in the expanded list and refuse to proceed.

## 5. The pipeline in cli.py has no tests, and it is where every defect is

**Severity:** Low  
**Where:** `src/whisper_captions/cli.py`, `tests/test_utils.py`

**What:** `tests/test_utils.py` covers `str2bool`, `format_timestamp`, `write_srt`, `filename`, and `expand_video_paths` -- all of `utils.py`. `cli.py` has no test file. `test.yml` runs the suite and passes.

**Why it matters:** Every issue above lives in `cli.py`: the output path collision, the ignored flag, the uncleaned temporary files, the basename keying. Each is a decision about paths and flags -- the kind of thing a test can check without ffmpeg, Whisper, or a video, if the decisions were extracted from the orchestration. The current split puts the untestable work and the testable decisions in the same functions, so the suite passes while the tool overwrites your input.

**Suggested fix:** Move the path decisions into `utils.py` as pure functions -- `output_path_for(input, output_dir)`, `audio_path_for(input)` -- and test them there. The ffmpeg and Whisper calls stay untested, which is fine; they are not where the bugs are.


---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.
