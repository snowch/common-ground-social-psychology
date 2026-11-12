# Reading and visual layout review

The course serves introductory learners choosing a standalone web course. Its performance goal is to help learners generate plausible explanations, distinguish observation from inference, and test ideas using evidence. Stories, application decisions, explanatory feedback, retrieval questions, and field practice already support this goal. The immediate barrier was presentation: paragraph boundaries were collapsed and optional diagrams shared a horizontal flex row with the main figure.

Applied the Instructional Design skill (https://github.com/joelrkohlman/instructional-design/blob/main/SKILL.md) and Frontend Design skill (https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), both already credited in README. Retain the field-guide identity: paper #EDF3F8, ink #19394D, ocean #216B88, muted #4B6172, line #CDD9E2; Libre Baskerville headings and Arimo body text. Left-aligned prose, deliberate paragraph spacing, and diagrams below text on smaller screens support reading. Replacing the palette or adding decorative cards would not address the learner's problem.

All ten evidence screens now preserve authored paragraphs. Recording transcripts use semantic paragraphs at the existing recorded pause boundaries. The attribution evidence recording already has 0.9-second pauses between its three paragraphs; audio has not been regenerated. All ten evidence recordings contain explicit pause markers.

All chapter players share the corrected vertical figure layout, including portable decks. Additional figures stay below the main figure and caption. At 900px and below, the lesson stacks in reading order. Print retains its existing two-column layout and plain term text.

Chapter glossaries cover the essential vocabulary registry, including attribution research. Definitions draw from existing teaching points, with additional definitions for terms introduced in evidence passages. Dotted underlines and ocean-colored text distinguish definition buttons. Native popovers work by touch and keyboard and dismiss with Escape or outside activation; the full chapter glossary is available below the lesson. Glossary use supports application and is not a new memorization requirement.

Validation: qa/check_reading_layout.py checks all 80 slides at 320, 390, 768, 1024, and 1440px, expanded figures, paragraph count, keyboard definition opening/dismissal, focus restoration, and JavaScript errors. This is a presentation review, not a learner pilot or independent academic review.
