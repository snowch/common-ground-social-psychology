# Common Ground

An original, illustrated social psychology course in ten stories, with recorded narration, decisions, recall practice, and open reading.

**Private repository.** This project and its releases are intended for the repository owner for now. No public hosting, sharing, or open-source license is enabled by this import.

## Read or download

- [Download the latest offline course ZIP](https://github.com/snowch/common-ground-social-psychology/releases/latest).
- [Open the private web course](https://common-ground-social-psychology.intactmars4.chatgpt.site).
- [Download smaller chapter packages](https://common-ground-social-psychology.intactmars4.chatgpt.site/downloads.html).

The release ZIP includes a self-contained narrated HTML course, ten separate chapter decks, PDFs, chapter audio, scripts, and review records. Extract it and open `common-ground/index.html` in a modern browser, then press **Play narration**. The recorded voice is embedded; no speech service or installed device voice is required. The M4A chapter tracks can be played directly on a phone. Release assets inherit this repository's private access.

## Course

| Chapter | Story | Topic |
| --- | --- | --- |
| 1 | The person and the room | Situations and attribution |
| 2 | The poster that “worked” | Evidence and experiments |
| 3 | The story that comes to mind | Social cognition |
| 4 | The plan we cannot let go | Self and self-justification |
| 5 | The quiet vote | Conformity and authority |
| 6 | The invitation | Attitudes and persuasion |
| 7 | When “we” takes over | Groups and belonging |
| 8 | The invisible doorway | Prejudice and discrimination |
| 9 | A place beside someone | Attraction and relationships |
| 10 | Who will do something? | Aggression, helping, and cooperation |

There are 80 slides, 20 application decisions with feedback for every choice, 20 recall questions, and ten field exercises. The continuous chapter tracks total approximately 48 minutes, including thinking pauses and suggested answers. Allow additional time for the exercises and reading. An optional 20–30-minute written case in a different setting includes six tasks and a self-assessment rubric. It has no recorded narration. The study companion combines the ten evidence notes, case, suggested reasoning, and rubric in HTML and an 11-page PDF.

The [whole-course review](docs/course-review-v0.2.0.md) records the chapter-by-chapter findings, fixes, evidence sources, and remaining limits. This is a short introduction; the multiple-choice decisions are formative practice and do not establish mastery.

## Build from source

Python 3.10 or newer is sufficient. Fonts and final narration files are already included.

```sh
python3 build.py
python3 -m http.server 8877 --directory dist
```

Open <http://localhost:8877>. This build loads each audio file when needed. It does not publish anything.

For self-contained HTML decks with embedded audio:

```sh
python3 build.py --portable --output out/portable
```

Open `out/portable/index.html` or an individual file in `out/portable/chapters/`. Build output is ignored by Git; large portable bundles belong in releases.

The manually dispatched **Package private course release** workflow builds the portable ZIP, verifies its integrity, computes a SHA-256 checksum, and attaches both to a release. It uses the repository’s own short-lived Actions token with contents-write permission. It does not change repository visibility.

## Content and production source

- `course.json`: complete chapter content, quizzes, feedback, recall answers, outcomes, and references.
- `course-evidence.json`, `learning-check.json`: chapter evidence notes and the written transfer case.
- `study-guide.pdf`: printable evidence and assessment companion; `scripts/build_study_guide.py` generates its HTML.
- `content.py`: original content authoring source; regenerates the canonical course JSON and teaching script.
- `template.html`, `build.py`: interactive player and portable/static builds.
- `assets/fonts/`, `FONT-LICENSE.txt`: bundled fonts and their license information.
- `audio/clips/`: 150 final AAC recordings, including feedback and recall answers.
- `audio/chapters/`: ten continuous listening tracks.
- `audio/manifest.json`: encoded durations and SHA-256 hashes.
- `chapters/*.pdf`, `common-ground-slides.pdf`: static slide decks.
- `narration-script.txt`, `narration-recording-script.txt`: teaching and exact recording scripts.
- `production/`: generation scenes, provenance, and audio processing scripts.
- `qa/`: speech screening, browser verification, source checks, and review limits.

Raw working WAV files, downloaded speech models, local environments, and generated HTML are excluded from Git. Final audio is retained, so using or rebuilding the course does not require speech synthesis.

## Narration

Kokoro-82M v1.0, **`af_heart`**, original synthesis speed **1.0**, Linux ONNX CPU. These are the settings documented for the newer `metadata-book` Chapter 1. The model and voice hashes are retained in `production/af-heart-production.json`.

The [narration style guide](docs/narration-style.md) explains explicit references, short paragraphs, and deliberate pauses. The approved opening introduced that approach in v0.1.1. The [v0.1.2 narration review](docs/narration-review-v0.1.2.md) applies it to the remaining 149 clips.

The voice workflow uses [snowch/claude-skills](https://github.com/snowch/claude-skills/tree/c9a7c521568632aa216932f4c965df386498602a/plugins/demo-video/skills/record-demo). [Production notes](production/README.md) explain regeneration. Phoneme overrides preserve the visible text while clarifying speech, including Maya's name and numbers.

## Verification

The recorded-audio browser check decoded all 150 recordings and exercised playback, pause/resume, stopping, rate changes, feedback and recall queues, navigation, mobile width, and a separate chapter deck. The 20 decisions' 60 feedback variants were checked.

Independent Whisper `small.en` screening covered all 150 clips. The retained report includes 9 flags: eight pacing flags and one number-formatting word-match flag; [the review](qa/af-heart-review.txt) records their interpretation. ASR and phoneme inspection are not a human listening review. No external subject-matter review or learner pilot has been performed.

For optional browser checks, install Playwright and Chromium, serve `dist` on port 8877, then run:

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
python3 qa/check_deck.py
python3 qa/check_recorded_audio.py
# Optional broader accessibility and regression audit:
curl -fsSL https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js -o /tmp/common-ground-axe.min.js
python3 qa/check_course_review.py
# Regenerate the PDFs from a running course preview:
python3 scripts/export_pdfs.py
```

The scripts default to `/usr/bin/chromium`; adjust that executable for another development machine. `COURSE_BASE_URL` can select another preview origin. Normal reading and builds require no browser automation dependencies.

## Sources and rights

This is an independently organized introductory course. It does not reproduce *The Social Animal*, follow its chapter structure, or claim equivalent depth or full textbook coverage. Characters and café events are fictional. Teaching text, illustrations, and exercises are original. OpenStax, Noba, and research readings are linked within each chapter rather than reproduced.

Learning and visual design drew on the [Instructional Design skill](https://github.com/joelrkohlman/instructional-design/blob/main/SKILL.md) and [Frontend Design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). Third-party fonts retain their own license. No general redistribution license for the original course is granted by this private repository.
