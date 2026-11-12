# Examples and explanation review

This pass reviewed all ten chapters: the 80 slides, 20 decisions and their 60 feedback variants, recall answers, field exercises, evidence notes, and final written case. It addresses places where a beginner would have to infer the meaning of a term or its connection to the example.

| Chapter | Changes |
| --- | --- |
| 1 — Situations and attribution | Explains disposition through “sweet disposition” and a usually patient volunteer under pressure. Distinguishes dispositions from other personal qualities. Defines attribution and actor–observer differences through lateness examples. |
| 2 — Evidence and experiments | Separates random assignment from sampling through household invitations. Explains percentage points, uncertainty, and statistical significance without equating significance with practical value. |
| 3 — Social cognition | Connects availability to Leo’s repair impression. Defines a denominator with an explicitly invented repair count. Contrasts confirmation bias and motivated reasoning through Leo and Maya. |
| 4 — Self-justification | Explains cognitions, inconsistency, and justifications through the booking-system decision. Separates unrecoverable effort from future consequences and explains the procedure behind the cited replication finding. |
| 5 — Conformity and authority | Gives distinct internal questions for informational and normative influence. Illustrates compliance and obedience, and briefly describes the tasks in the classic studies. |
| 6 — Persuasion | Defines attitude with an everyday evaluation. Contrasts central and peripheral processing through practical commitment details and a celebrity cue; preserves the qualification that processing varies by degree. |
| 7 — Groups | Illustrates in-group favoritism, polarization, social loafing, and coordination loss. Explains anchoring in feedback and replaces “dependency” in the field exercise with the action it describes. |
| 8 — Prejudice and discrimination | Gives parallel examples of belief, attitude, and unequal treatment. Makes equal participation and procedural barriers concrete. Explains explicit attitudes and implicit associations before discussing measurement limits. |
| 9 — Relationships | Ties opportunity and familiarity to the shared shift. Illustrates disclosure and responsiveness. Explains self-report limitations and makes the listening exercise easier to apply. |
| 10 — Helping and aggression | Contrasts “someone else will act” with “perhaps no help is needed.” Distinguishes anger from aggression, explains de-escalation, and gives an example of a laboratory aggression measure. |

The study companion also explains invitation sharing between experimental groups, degrees of message processing, and limits on applying findings to other settings. The written case and rubric use plainer language for allocation, discriminating evidence, and generalization.

Examples added in this pass are original illustrations. “Sweet disposition” is an everyday expression, not a dictionary quotation. Existing research qualifications, reading links, chapter outcomes, and quiz answer keys are retained. Explanations and examples illustrate possible processes; they do not establish the causes of a particular person’s behavior.

Recording scripts are synchronized using `scripts/sync_narration.py`; its `--check` mode detects stale scripts. Only changed recordings are regenerated, using the existing Kokoro ONNX `af_heart` voice at speed 1.0, with pauses at paragraph and exercise boundaries. Unchanged clips retain their approved speech forms. Current generation and automated screening details are recorded in `production/af-heart-production.json` and `qa/clarity-review.json`; earlier versioned reviews remain historical records.

This is an editorial and automated verification pass. It is not an external subject-matter review, a learner pilot, or human listening approval.

## Visible terminology follow-up

Fifteen concept slides now name important vocabulary directly in their summaries. The additions include fundamental attribution error, random sampling, statistical significance, confirmation bias, motivated reasoning, cognitive dissonance, sunk cost effect, the elaboration likelihood model, intergroup contact, mere exposure effect, reciprocity, and the three helping concepts. Existing abbreviated labels such as “informational” and “descriptive” now use the full terms “informational influence” and “descriptive norm.”

Concept labels before a colon are emphasized in bold, alongside short explanations or examples. The same summaries appear in the online course, portable decks, and PDFs. The approved recording scripts and all audio files are unchanged.

`qa/essential-terms.json` lists the vocabulary that must appear on each teaching slide. `qa/check_visible_terminology.py` checks the actual slide text at mobile and desktop widths, excluding the recording transcript, and checks the corresponding pages in the complete PDF and individual chapter PDFs. It also covers terms already visible in the evidence slides, including replication, preregistration, groupthink, and implicit associations. Run it against a preview after exporting the PDFs. `qa/visible-terminology-results.json` records the result.

The check passed for 61 required term appearances across 25 teaching slides at widths of 320 and 1440 pixels, and on the matching pages in both PDF formats. The 80-slide layout check found no clipping; the course regression check reported no automated accessibility violations across 83 screens. These are automated checks, with the same usability and review limits stated above.

## Attribution-error diagram

Chapter 1’s first concept retains the diagram showing personal and situational influences together. The second concept shows Leo thinking: his thought bubble contains a larger Person box, a smaller Situation box, and the thought “Maya doesn’t care.” A trail of small bubbles connects the thought to Leo. Labels state “Too much weight” and “Too little weight.” The geometry illustrates relative emphasis in his explanation. The figure also states that the tendency’s strength varies with culture and context.

The graphic has an accessible description and appears in the online slide, portable chapter, and PDF. Checks at 320, 390, 768, and 1440 pixels found no horizontal overflow or cropped SVG text; the preceding balanced diagram is preserved. Targeted accessibility and PDF layout checks passed. `qa/attribution-diagram-results.json` records the targeted checks. Existing teaching text and recordings are unchanged.

## Concept-specific visual explanations

Six further teaching slides now illustrate the seven suggested concepts. They use the existing cast, palette, fonts, and original SVG artwork:

| Slide | What the visual explains |
| --- | --- |
| Chapter 2, slide 3 | New poster, better weather, and publicity are possible explanations for increased attendance. Dashed paths show hypotheses to investigate. |
| Chapter 3, slide 4 | Leo and Maya see the same illustrative repair records, but give different cases more attention according to their expectations. Symbols and outlines distinguish the cases as well as color. |
| Chapter 4, slide 4 | An unrecoverable past expense sits behind Today. Both continuing and switching are future options; skills and obligations can still affect their consequences. |
| Chapter 5, slide 3 | Sam says “I agree” under two possible private motives: treating others as information and seeking acceptance. The figure states that both motives can operate together. |
| Chapter 7, slide 4 | Illustrative opinion positions show agreement around a similar average position versus a stronger version of the initial leaning. These are illustrative possible outcomes; agreement and polarization can also coexist. |
| Chapter 10, slide 3 | Privately worried people misread others’ calm in pluralistic ignorance; people assume someone else will act in diffusion of responsibility. Context and available support remain relevant. |

The repair records and opinion positions are illustrations, with no empirical effect sizes or café outcome rates implied. Recorded narration and teaching text are unchanged. Each visual is assigned to its own teaching slide and appears in the portable decks and PDF exports.

`qa/check_concept_visuals.py` checks placement, text bounds, horizontal overflow, and accessibility at mobile and desktop widths. It also verifies that the confirmation-bias illustration uses the same evidence on both sides while highlighting different outcomes. `qa/concept-visuals-results.json` records the results. These checks do not establish learner comprehension or complete accessibility conformance.

## Complete visual coverage

The visual set now covers every concept and evidence slide: 30 teaching slides, with 48 separate views. The original attribution thought bubble and the seven subsequently illustrated concepts remain available. Additional views separate concepts that need their own explanation rather than compressing them into one diagram.

| Chapter | Visual explanations |
| --- | --- |
| 1 | Person and situation, disposition under pressure, attribution error, observation versus attribution, actor–observer differences, and evidence across occasions |
| 2 | Confounding, correlation, random sampling versus assignment, invented effect sizes, significance versus importance, and research reliability |
| 3 | Availability, base rates and denominators, confirmation bias, motivated reasoning, and checking bias claims against evidence |
| 4 | Cognitive dissonance and its possible responses, sunk costs and future consequences, and the scope of a particular replication |
| 5 | Informational and normative influence, compliance versus obedience, an actionable questioning route, and the limits of classic study settings |
| 6 | Message processing, attitudes versus action, descriptive versus injunctive norms, honest invitations, and persuasion outcomes |
| 7 | Social identity and favoritism, shared goals, polarization versus consensus, loafing versus coordination loss, and groupthink processes |
| 8 | Stereotype, prejudice, and discrimination; procedural barriers; contact conditions; access changes; and distinct attitude and behavior measures |
| 9 | Opportunities and similarity, mere exposure and its limits, disclosure and responsiveness, reciprocity, attachment labels and boundaries, and relationship evidence |
| 10 | Bystander processes, a safe helping path, anger versus aggression, de-escalation, cooperation, and limits of research proxies |

Every teaching slide has a primary figure. Native expandable sections provide the additional views. The shared artwork registry generates a separate visual companion in HTML and PDF, containing every view. Each chapter ZIP includes that companion, while the main slide PDFs remain eight pages per chapter. The complete visual PDF has 49 pages: a cover and 48 individual figures.

`qa/visual-coverage.json` records the slide-to-view mapping and required vocabulary. The expanded visual QA checks every view at four widths, the native disclosures, visible terminology, accessible descriptions, and every page of the visual PDF. Figures are original teaching illustrations; invented counts and opinion positions are identified as illustrative. Course text, questions, and recorded narration are unchanged. No learner pilot or external subject-matter review is claimed.

Offline archive verification also exercised an expanded chapter figure, embedded audio playback, all 48 companion views, and the chapter return link with other network requests blocked. The test served HTML directly from a generated ZIP. Managed Chromium blocks direct file navigation, so file-opening behavior itself was not verified; see `qa/offline-visuals-results.json`.
