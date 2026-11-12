"""Bundle the supplied buildless scene into an offline HTML. No dependency installation."""
from pathlib import Path
import argparse
import re

def build(project: Path, output: Path):
    project = project.resolve()
    html = (project / 'index.html').read_text(encoding='utf-8-sig')
    def content(relative):
        target = (project / relative).resolve()
        if not target.is_relative_to(project):
            raise ValueError('Asset escapes the project: ' + relative)
        return target.read_text(encoding='utf-8-sig')
    def script(m):
        text = content(m.group(1)).replace('</script', '<\\/script')
        return '<script>\n' + text + '\n</script>'
    html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', lambda m: '<style>\n' + content(m.group(1)) + '\n</style>', html)
    html = re.sub(r'<script src="([^"]+)"></script>', script, html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding='utf-8')
    print(f'{output.resolve()}\n{output.stat().st_size:,} bytes')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    build(a.project, a.output)
