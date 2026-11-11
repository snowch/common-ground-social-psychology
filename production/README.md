# Narration production

The final recordings are already committed in `audio/`. Do not regenerate unchanged speech for visual edits.

Voice: Kokoro v1.0, `af_heart`, speed `1.0`, ONNX CPU. The originating skill commit is `c9a7c521568632aa216932f4c965df386498602a` in `snowch/claude-skills`. It verifies downloaded model and voice files against pinned hashes.

For regeneration, clone that skill repository separately, install `uv` and FFmpeg, and run its original scripts against this repository's `production/af-heart` directory:

```sh
uv run /path/to/claude-skills/plugins/demo-video/skills/record-demo/scripts/tts.py "$PWD/production/af-heart" af_heart 1.0
uv run /path/to/claude-skills/plugins/demo-video/skills/record-demo/scripts/phonemes.py "$PWD/production/af-heart" --all
uv run /path/to/claude-skills/plugins/demo-video/skills/record-demo/scripts/asr.py "$PWD/production/af-heart" small.en
```

Run from the course repository root. The narration skill's dependencies are declared in its scripts. Retain raw `audio/*.wav` as ignored working files. Selective regeneration is available through the skill's `SCENES` environment variable.

`asr_batch.py` retains independent Whisper small.en screening with audio-only batches and explicit clip boundaries. It can resume previously screened clips; invalidate corresponding entries in its working `asr-progress.json` after changing speech. Original sequential and batched checks share the same word, pacing, peak, level, and internal-gap criteria. ASR screening is not listening approval.

After reviewing speech, install `numpy` and `soundfile` for the encoding helper, and run:

```sh
python3 production/encode_audio.py
python3 build.py
```

The encoder uses FFmpeg, targets -16 LUFS and -1.5 dBTP, and writes 48 kHz mono AAC at 160 kbps. It preserves unchanged clips and chapter tracks. `production/af-heart-production.json` describes the imported recording run; `audio/manifest.json` gives the final encoded hashes. Update provenance after a new production run rather than claiming its checks match the original.

Canonical on-screen text and speech-specific pronunciation forms are recorded separately in `af-heart/scenes.json` and `narration-recording-script.txt`. No voice belonging to a real person was supplied for cloning.
