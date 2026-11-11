# Copyright and asset audit — v0.3.0

11 November 2026. Scope: the current Common Ground course, source tree, learner pages, slides, recordings, study companion, standalone chapter packages, and new release packaging. The repository and Site remain private to the owner.

**Finding:** the inspection did not identify a copied passage, imported figure, reproduced assessment, or audiobook excerpt in the teaching material reviewed. It did identify font-notice and production-code licensing gaps, which this release addresses. This is a documented risk assessment, not a guarantee of non-infringement or a jurisdiction-specific legal opinion.

## Inspection and evidence

- Read the ten chapter stories, explanations, examples, 20 decision questions and all 60 feedback variants, 20 recall prompts and answers, ten field exercises, ten evidence notes, six final-case tasks and suggested answers, rubric, player copy, and recording scripts.
- Inspected the player and diagram source, media and font files, build/production code, file inventory, and Git provenance. The course entered this repository as a generated course project; the Git record alone cannot establish independent authorship of every expression.
- Compared 355 distinct content units, including speech-specific wording, with 15 linked public reading pages: eight OpenStax pages and seven Noba modules, totaling 70,252 normalized source tokens. All 15 returned usable page text. No contiguous match of eight or more normalized words was found. `qa/copyright-source-overlap.json` records URLs, retrieval hashes, counts, and results; `scripts/audit_source_overlap.py` reproduces the screening. The eight-word threshold is an investigation setting, **not a legal test or safe harbor**. This does not detect all close paraphrase, nonverbatim copying, protected selection/arrangement, or sources outside the comparison set. Navigation/footer text in retrieved pages was included, so token counts exceed teaching prose alone.
- Reviewed the reading examples and course situations for close adaptation. The café cast, broken lift, poster comparison, repair-return record, booking tool, publicity vote, recruitment invitation, checklist, access process, friendship, and helping incident use a continuing fictional setting and new questions. The final language-club case is a separate fictional application. No identifiable source-specific anecdote or assessment was found in this comparison; independent creation cannot be proven from surface inspection alone.
- Checked the requested reference book's publisher-supplied contents for title/sequence comparison. The course has ten story-titled chapters, none matching those published chapter titles verbatim, and a different sequence and instructional format. Common subject coverage is expected in introductory social psychology. **The complete proprietary book was not obtained or compared**, so the audit does not exclude every possible similarity to it. Only the public publisher record was consulted; no unauthorized book download was used.
- Inspected the conceptual SVG source. Figures use programmatically specified people, tables, boxes, arrows, and explanatory labels; no source textbook figures, cover art, screenshots, photographic stock, or imported icon pack was found among current course assets. This is source/provenance inspection, not an exhaustive reverse-image search or a determination of copyrightability of generated artwork.
- Checked font permissions and distribution paths, model and voice provenance, standalone HTML comments, package notices, PDF font lists, and exact hashes of the 150 recorded clips and ten continuous tracks. No narration regeneration was required. The preview recording is also included in the asset inventory.

The source-page snapshots used for local comparison remain outside the repository and release. No course text was uploaded to a plagiarism service or submitted as a search query. Source URLs were retrieved to perform the comparison locally.

## Findings and corrections

| Area | Finding | Correction / disposition |
| --- | --- | --- |
| Embedded fonts | Nimbus Sans and URW Bookman were distributed with an incomplete Debian-derived notice. Upstream licenses the fonts under AGPL-3.0 with an exception specifically addressing PostScript/PDF documents. That exception does not itself establish HTML/webfont permission on the same terms, and the full AGPL/source requirements had not been documented for this package. | Removed those binaries from the current source tree and rebuilt all current PDFs and HTML with unmodified **Libre Baskerville** and **Arimo**, under **OFL-1.1**. Complete author notices and OFL texts accompany the fonts, are embedded in each HTML file, and are included in chapter and full-course packages. Original font names and binary metadata are preserved. Sources are pinned to a Google Fonts commit and SHA-256 hashes. This resolves the current packaging choice without asserting that every prior font use was infringing. |
| Production helper | `production/asr_batch.py` incorporated helper code from the record-demo checkout. No general license was found at the pinned upstream commit; public availability and a user instruction to use a tool do not establish a general redistribution license for its code. | Replaced the incorporated implementation with a runner that invokes a separately obtained upstream script. The runner preserves cached reports, supports three external workers, and forwards the configured script path. Existing recordings and production-review records remain unchanged. A stub-based interface check verifies worker invocation, ordering, flags, and cache behavior; it is not a new speech-quality review. |
| Course comparisons | Current footer, About copy, README, study companion, starter text, and older source release notes contained defensive comparisons or equivalence claims. | Replaced them with positive descriptions of the course and its learning activities. Source credits and third-party license notices remain. Removing a disclaimer is an editorial change, not evidence of independent creation. |
| Asset notices | Third-party production provenance and the difference between bundled assets and tools were not collected in one place. | Added `THIRD-PARTY-NOTICES.txt`, complete font notices, model/software license references, and an asset manifest. Notices distinguish synthesized recordings from separately installed software, weights, voice tensors, and training datasets. |
| Reading licenses | Linked sources remain copyrighted. Current OpenStax/Noba pages identify CC BY-NC-SA 4.0 terms. A citation is not permission to copy passages or figures, and a license on a linked page does not automatically license this whole course. | Preserve reading links and bibliographic research credits. Do not bundle source-page snapshots or rely on a blanket educational-use claim. Future copied/adapted material must be evaluated against the applicable source/version terms. |

## Chapter-level expression review

| Chapter | Material inspected and conclusion within the audit scope |
| --- | --- |
| 1 | Fictional lateness story, person/situation diagram, attribution explanation, shift/travel decisions. No identifiable borrowed narrative or figure found; scientific terms and the general distinction are shared subject matter. |
| 2 | Fictional poster story, household-assignment diagram, invented 12/100 and 15/100 numbers, causal reasoning questions. Numbers are labeled hypothetical; no research table or published dataset is reproduced. |
| 3 | Fictional repair-return story, evidence-filter diagram, denominators and belief-testing exercises. Explanations were screened against the linked cognition readings; no eight-word candidate match found. |
| 4 | Fictional booking-system decision, consistency diagram, future-cost exercise, short account of the multilab result. Research findings are paraphrased and cited; no paper abstract, study instrument, or published illustration is inserted. |
| 5 | Fictional donor vote and safety instruction, influence diagram, independent-view exercise. Mentions of researchers and standard experimental findings are factual descriptions, not reproduced stimuli, participant scripts, or copyrighted photographs. |
| 6 | Fictional invitation, processing diagram, norm distinctions, message-design exercise. No advertising creative, published campaign, or source-specific assessment is imported. |
| 7 | Fictional team split, group diagram, escalating budget and checklist decisions. Theoretical concepts and practical procedures are explained through the course's own setting; no imported case study or research figure found. |
| 8 | Fictional recruitment barriers, doorway diagram, access-review exercise. No real applicant data, proprietary questionnaire, implicit-test stimuli, or published intervention manual is bundled. |
| 9 | Fictional shared shift, responsiveness diagram, invitation/boundary decisions. No copyrighted attachment inventory, compatibility questionnaire, or relationship-study instrument is reproduced. |
| 10 | Fictional incident, helping-process diagram, response-plan exercise. No emergency training manual, incident record, video, or laboratory aggression instrument is imported. |

These conclusions are based on the inspected files and comparison sources. They are not exhaustive source tracing of every sentence or proof that similar expression exists nowhere else.

## Narration and software

The retained stock voice is Kokoro v1.0 `af_heart`, speed 1.0. Upstream model metadata declares Apache-2.0; the kokoro-onnx implementation is MIT licensed. Model/voice binary hashes are retained in `production/af-heart-production.json`. The distributed material is synthesized speech of the course scripts. Upstream executable code, model weights, voice tensors, and training recordings are not included in the course player.

The model card discloses training sources including CC BY material. The project has not independently verified those training-data permissions, voice provenance, or the absence of memorized material in every possible model output. An open model license is not a blanket warranty covering all output or a grant of personality/publicity rights. The project supplied no person's recording for cloning. The inspection found no externally sourced soundtrack, song, or audiobook segment in the delivered assets.

Production tools and externally read skills are credited. They retain their own terms; their use does not automatically impose their software license on teaching content or generated audio. No assertion of exclusive copyright in AI-assisted output is made. Copyrightability and ownership are separate from whether third-party expression is infringed.

## Legal framework used

Jurisdiction was not specified. The audit uses the general distinction between scientific ideas/facts and protected expression, with official US and UK guidance as reference points:

- [US Copyright Office: What Does Copyright Protect?](https://www.copyright.gov/help/faq/faq-protect.html): ideas and facts differ from their expression; unpublished works may also be protected.
- [US Copyright Office: Fair Use Index](https://www.copyright.gov/fair-use/): educational and noncommercial purposes do not automatically establish fair use; the statutory factors and circumstances matter.
- [UK Intellectual Property Office: Exceptions to copyright](https://www.gov.uk/guidance/exceptions-to-copyright): private-study and teaching exceptions are limited and subject to conditions such as fair dealing.
- [SIL Open Font License FAQ](https://openfontlicense.org/ofl-faq/): web distribution and document embedding are permitted under the OFL conditions, and the font license does not relicense the document.
- [URW upstream license](https://github.com/ArtifexSoftware/urw-base35-fonts/blob/master/LICENSE): records the terms that prompted the font replacement.
- [Kokoro model card](https://huggingface.co/hexgrad/Kokoro-82M) and [kokoro-onnx license](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE): production provenance and declared licensing.

Keeping a repository private, avoiding a purchase, giving a credit, changing words, or adding a disclaimer does not itself establish lawful use. The audit's conclusions rely on inspected expression, source comparison, and documented asset permissions, not those factors alone.

## Validation and limits

`qa/copyright-artifact-checks.json` records current HTML/notice checks, font hashes, audio hashes, PDF inspection, and packaging checks. `qa/copyright-pdf-build.json` records the PDF rebuild with the replacement fonts and measured slide bounds. `qa/copyright-inventory.json` inventories current media, font, and license artifacts.

Chromium was used as an offline PDF build engine. Interactive Site browser QA was not rerun because the managed preview route is unavailable; source/build checks and PDF inspection cover this change. Existing broader course/ASR checks retain their own dates and scope. No new ASR or human listening approval is claimed.

Earlier Git commits and previously published release ZIPs retain their historical files and notices; they were not rewritten or retroactively cleared by this audit. The current course and v0.3.0 package are the reviewed artifacts. Historical source release notes have been editorially updated to remove the requested comparison language. Previously downloaded HTML/ZIP files require a new download to receive these changes.

Residual limits: the complete proprietary reference book and the universe of potential source works were not compared; nonverbatim similarity, training-data rights, and jurisdiction-specific application have not been legally adjudicated. This audit reduces identifiable risk and documents corrections. It cannot ensure that no copyright claim could arise. A qualified rights/legal review would be needed for stronger clearance, especially if distribution or use changes.
