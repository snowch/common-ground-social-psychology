# Common Ground visual refinement

Design guidance: Frontend Design, https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md (read 11 November 2026). The existing course, fictional cast, learning interactions, and audited OFL fonts provide the brief.

## Plan

Subject: a community repair café as a place to notice how people think and act. The course should feel like entering that workshop and opening a carefully made field guide.

Color tokens: cool canvas #EDF3F8, white paper #FFFFFF, navy ink #19394D, teal #236A67, brass #D8AC5C, and plum #806196. Chapter accents remain attached to their existing chapters.

Type: Libre Baskerville carries narrative headlines and chapter titles; Arimo carries reading, navigation, and controls. Both remain locally embedded with their complete OFL notices. Headlines have less compression; reading width stays controlled.

Layout:

```
brand                                      chapters / downloads / print
+--------------------------------------------------------------------+
| short introduction                 illustrated workshop             |
| People make more                   window, people, shared table     |
| sense in context.                  repair tools and everyday objects|
| start / resume                     Maya, Sam, Leo                   |
+--------------------------------------------------------------------+
chapter introduction                     how to use this course
01 chapter / topic / explicit status     02 chapter / topic / status
03 chapter / topic / explicit status     04 chapter / topic / status
...
written transfer case / study companion
learning guidance / source and usage information
```

Player: chapter context, accessible narration/navigation toolbar, reading stage, transcript and optional research details. The toolbar should be available before the large slide illustration on phones. Buttons and current/selected states must remain explicit.

## Review against the brief

A generic dashboard, stock photography, and a new font library would add little to this course. One prominent illustrated cover gives the page identity; chapter links remain a quiet sequence rather than a collection of dashboard cards. The new workshop SVG is drawn in the course source using the established fictional people. No external illustration, image, or icon pack is introduced.

The existing blue palette alone was not providing enough hierarchy. A navy cover and white reading surfaces separate entry, navigation, and learning without applying decorative gradients or repeated shadows. Brass is reserved for workshop objects and small structural details. Native disclosure controls keep reference material available with less visual noise.

## Implementation constraints

Keep recording files, timing, questions, feedback, recall answers, evidence text, and progress storage intact. Preserve the visible “Not started” label. Maintain keyboard focus, reduced-motion support, contrast, print layouts, complete embedded asset notices, self-contained downloads, and relative URLs under the GitHub Pages repository path.

The public GitHub Pages site and offline chapter downloads receive the same design. The separately hosted ChatGPT Site is a previous publication with independent access and deployment.

## Visual critique

Reviewed full-page desktop and mobile screenshots against the plan. The navy cover gives the workshop illustration a clear home, and the chapter list keeps titles and progress easy to scan. The first illustration pass lost the cast labels against the cover; a pale caption plate now keeps their names readable in both cover and slide contexts. Automatic heading focus no longer draws a large browser-default outline; keyboard focus remains visible on interactive controls.

The player toolbar precedes the slide. Evidence remains available in native disclosure controls, open on evidence slides, while the recording transcript remains open for reading. Downloads now explain extraction before listing packages, and the companion reads as a single paper document. New SVG drawing code was authored within this project; no external artwork or font was added.
