# Course-wide review of teaching pages

The review now covers all ten chapters, including the stories, explanations, alternative figures, application decisions, retrieval prompts, and field exercises. Chapter 1's earlier changes remain in place. This revision applies the same learning-design question to Chapters 2–10: what action is this page teaching, and what explanation and example does the learner need before attempting it?

The [Instructional Design skill](https://github.com/joelrkohlman/instructional-design/blob/main/SKILL.md) informs the sequence: establish the distinction, explain it through the café story, show its limits, then apply and retrieve it. The [Frontend Design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) informs the readable field-guide treatment and restrained visual hierarchy.

## Page decisions

All fifteen remaining alternative figures introduce a distinct explanation, worked example, or procedure. They now appear as primary illustrations on sequential teaching pages with their own narration and Previous/Next controls. These are steps within the existing chapters; creating more chapters would fragment the story and separate the practice from its prerequisite explanations.

| Chapter | Teaching action and decision | Steps |
| --- | --- | --- |
| 1. Situations and attribution | Retain the six primary teaching pages from the preceding review: person and situation, a worked example, observation and attribution, attribution error, actor–observer comparison, and testing an explanation. | 11 |
| 2. Research methods | Separate correlation and causation, the confounding example, sampling versus assignment, estimated size and uncertainty, and significance versus practical importance. Retain the evidence page on replication, preregistration, design, and inspection. Each page answers a different question about a claim or study. | 11 |
| 3. Social cognition | Retain availability, base rate, and denominator together because they support one frequency-estimation task. Separate confirmation bias from motivated reasoning, explicitly stating their overlap and the difference between an existing belief and a preferred conclusion. Retain evidence limits. | 9 |
| 4. Self and self-justification | Retain the existing focused sequence: dissonance and ways to reduce it; sunk costs and future consequences; evidence limits. Its three figures were already primary and the explanations lead into the existing application and retrieval tasks. No additional page is warranted. | 8 |
| 5. Social influence | Keep normative versus informational influence as a meaningful comparison. Keep compliance versus obedience together to distinguish a request from an authority's instruction. Give the procedure for questioning an unsafe instruction its own page before transfer practice. | 9 |
| 6. Attitudes and persuasion | Teach evaluation versus action before message processing. Give elaboration and processing their own step. Keep descriptive versus injunctive norms together, then separately apply that distinction to an honest invitation. | 10 |
| 7. Groups | Distinguish identity and favoritism from the practical work of arranging a shared goal. Separate group polarization from social loafing and coordination loss; the latter comparison teaches different explanations of an unsuccessful team effort. Retain the evidence qualifications. | 10 |
| 8. Prejudice and discrimination | Keep stereotype, prejudice, and discrimination together so thought, feeling, and treatment can be compared. Give structural access barriers a concrete page. Separate intergroup contact from procedural changes, with an explicit account of why a friendly encounter does not change an exclusionary rule. | 10 |
| 9. Relationships | Keep proximity and similarity together as opportunities to meet. Give mere exposure its own qualified explanation, including unwanted contact and boundaries. Keep disclosure, responsiveness, and reciprocity together as an interaction; give attachment patterns a separate step that avoids diagnosing the characters. | 10 |
| 10. Helping and harm | Keep the bystander-process comparison together, then teach a safe helping plan separately. Keep anger, aggression, and de-escalation together as distinctions supporting the response to conflict. Give cooperation and explicit responsibility their own page. | 10 |

The review does not impose one term per page. Comparisons that help the learner discriminate closely related concepts remain together. A procedure or a new causal question receives its own step. Chapter 4 demonstrates the decision to retain an already focused sequence.

## Clarity and pacing

The fifteen added pages and fourteen revised pages have concise slide points and independently recorded scripts. References name whose observation, belief, preference, or action is being discussed. Worked examples identify the café situation before asking the learner to transfer the distinction. Scientific qualifications remain adjacent to the claim: a bias label does not settle a judgment, random assignment does not make a sample representative, a nonsignificant result does not prove zero effect, contact does not guarantee improved access, and familiarity creates no obligation to interact.

The initial story, application decisions, feedback, retrieval prompts, evidence notes, and field exercises retain their stable identities. They already support the chapter outcomes; the new teaching steps make their prerequisites explicit. Existing paragraph breaks, glossary controls, deliberate narration pauses, and controls between text and illustration in stacked layouts remain. Chapter 1 retains the separate definition paragraph and the pause before its course-wide reminder.

## Visual treatment and source structure

All 48 teaching pages have one primary figure. Essential explanation is no longer hidden in a “More visual explanations” disclosure. Sequential procedures use numbered steps with a connecting line and left-aligned action/detail text. Parallel categories use separate bands without sequence numbering. Comparison cards put their headings inside compact panels and size the panel to its content. Teal and plum distinguish the compared categories; amber rules and serif headings retain the course's field-guide identity. Diagrams remain SVG with descriptive text, and the glossary remains keyboard operable.

`teaching-pages.json` is the canonical source for each teaching page's stable ID, purpose, points, script, and primary figure. `content.py` combines those pages with each chapter's story, decisions, retrieval, and practice. The figure catalog is independent of page placement. This prevents future text/figure placement drift and keeps the visual companion consistent with the player.

The course now has 98 steps, including 48 illustrated teaching pages, and 168 recordings. Continuous chapter tracks total 3,997.9 seconds (approximately 67 minutes), including the existing thinking pauses and suggested answers. The complete slide PDF has 98 pages. Chapter PDFs follow each chapter's actual length, while the visual companion remains 49 pages: a cover and all 48 figures.

New suffix IDs preserve original bookmark identities. The additional `c` suffix in Chapter 2 is supported by routing, saved visits, and resume. Legacy numeric resume positions still resolve to their original slide identities. Counts, audio mappings, PDF ranges, and package checks derive from source data.

## Validation

Validation covers all 98 pages at 320, 390, 768, 1024, and 1440 pixels; all 48 teaching pages in sequence; independent playback of all eighteen suffix pages (including Chapter 1); chapter boundaries; existing bookmarks, saved choices, and resume; glossary interaction; all 168 encoded recordings; selected feedback and retrieval-answer playback; standalone chapter decks; printable vocabulary and overflow; SVG text bounds; automated accessibility checks; hosted assets and offline packages.

Twenty-nine changed or added scripts were synthesized with the same pinned Kokoro ONNX model, `af_heart` voice, and speed 1.0. Whisper `small.en` screening found no new flags. Four phrases were refined after inspecting the transcripts, then synthesized and screened again. The 139 unchanged recordings retain their existing screens, including seven historical flags. The current screening and phoneme records are `qa/course-teaching-asr.json` and `qa/course-teaching-phonemes.txt`.

Automated layout, speech, PDF, and accessibility checks do not establish learning effectiveness or human listening approval. There has been no external subject-matter review or learner pilot. The application decisions remain formative practice rather than evidence of mastery.
