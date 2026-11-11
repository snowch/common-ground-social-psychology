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
