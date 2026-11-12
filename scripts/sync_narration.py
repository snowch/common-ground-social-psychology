"""Synchronize recording scripts after content edits; retain unchanged speech forms.

This prepares scripts only. Changed clips still need synthesis and screening.
"""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def speech_form(text):
    text = re.sub(r"\bMaya[’']s\b", '[Maya’s](/mˈaɪəz/)', text)
    text = re.sub(r"(?<!\[)\bMaya\b(?![’'])", '[Maya](/mˈaɪə/)', text)
    return (text.replace('£100', 'one hundred pounds')
            .replace('£300', 'three hundred pounds').replace('2024', 'twenty twenty-four')
            .replace('The linked Vaidis and colleagues study provides the details.',
                     'The linked study provides the details.'))


def compile_scenes(course, previous):
    old = {s['id']: s for s in previous}
    scenes = []

    def add(key, title, text, say, part, slide=None):
        # Keep approved pacing and pronunciation when the spoken content is unchanged.
        if key in old and old[key]['text'] == text:
            scene = dict(old[key], step=title, part=part)
        else:
            scene = dict(id=key, step=title, text=text, part=part, say=speech_form(say))
        if slide is not None:
            scene['slide'] = slide
        scenes.append(scene)

    for chapter in course:
        part = f"chapter-{chapter['number']:02d}"
        for index, slide in enumerate(chapter['slides']):
            text = slide['text']
            if 'quiz' in slide:
                options = [f"Option {chr(65+i)}. {v}" for i, v in enumerate(slide['quiz']['options'])]
                say = text.replace('\n\n', ' [pause 0.6] ') + ' [pause 0.6] '
                say += ' [pause 0.6] '.join(options) + ' [pause 0.7] Pause here and make your choice. [pause 2.0]'
                text += '\n\n' + '\n'.join(options) + '\n\nPause here and make your choice.'
            elif slide['kind'] == 'recall':
                parts = text.split('\n\n')
                assert len(parts) == 4, slide['id']
                say = parts[0] + ' [pause 0.7] ' + parts[1] + ' [pause 2.0] '
                say += parts[2] + ' [pause 2.0] ' + parts[3] + ' [pause 3.0]'
            else:
                say = text.replace('\n\n', ' [pause 0.9] ')
                if text.endswith('?'):
                    say += ' [pause 1.5]'
            add(slide['id'], slide['title'], text, say, part, sum(len(c['slides']) for c in course if c['number'] < chapter['number'])+index+1)
            if 'quiz' in slide:
                for index, feedback in enumerate(slide['quiz']['feedback']):
                    prefix = 'Good application.' if index == slide['quiz']['correct'] else 'Consider the consequence.'
                    add(f"{slide['id']}-feedback-{index}", 'Decision feedback', prefix+' '+feedback,
                        prefix+' [pause 0.35] '+feedback, part)
            if 'answers' in slide:
                text = 'Suggested answers.\n\nFirst. '+slide['answers'][0]+'\n\nSecond. '+slide['answers'][1]
                add(slide['id']+'-answers', 'Suggested recall answers', text,
                    text.replace('\n\n', ' [pause 0.8] '), part)
    assert len(scenes) == len({s['id'] for s in scenes})
    assert len(scenes) == sum(1+len(s.get('quiz',{}).get('options',[]))+('answers' in s) for c in course for s in c['slides'])
    return scenes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if recording scripts need synchronization.')
    args = parser.parse_args()
    path = ROOT/'production/af-heart/scenes.json'
    previous = json.loads(path.read_text())
    scenes = compile_scenes(json.loads((ROOT/'course.json').read_text()), previous)
    old_by_id = {s['id']: s for s in previous}
    changed = [s['id'] for s in scenes if s != old_by_id.get(s['id'])]
    script = ['COMMON GROUND — RECORDED AF_HEART SCRIPT',
              'Current recording script; see production/af-heart-production.json for revision provenance.',
              'Kokoro v1.0, ONNX CPU, af_heart, speed 1.0. Pause markers indicate inserted silence and are not spoken.', '']
    for scene in scenes:
        script.extend([scene['id']+' | '+scene['step'], scene['text']])
        if scene.get('say', scene['text']) != scene['text']:
            script.append('Speech-specific rendering: '+scene['say'])
        script.append('')
    recording_script = '\n'.join(script)
    if args.check:
        assert not changed, 'Scenes need synchronization: '+', '.join(changed)
        assert (ROOT/'narration-recording-script.txt').read_text() == recording_script, 'Recording transcript is stale.'
    else:
        path.write_text(json.dumps(scenes, ensure_ascii=False, indent=2))
        (ROOT/'narration-recording-script.txt').write_text(recording_script)
    print(json.dumps({'scene_count': len(scenes), 'changed': changed}))


if __name__ == '__main__':
    main()
