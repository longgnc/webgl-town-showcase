"""Static inventory, not proof of runtime network behavior or visual quality."""
from pathlib import Path
import argparse, hashlib, json, re

def audit(path):
    data = path.read_bytes()
    text = data.decode('utf-8-sig')
    return {
        'file': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
        'inline_script_count': len(re.findall(r'<script(?:\s[^>]*)?>', text)),
        'external_script_sources': re.findall(r'<script[^>]+src=["\']([^"\']+)', text),
        'three_revision_literal': re.findall(r'\bM2="(\d+)"', text),
        'counts': {token: text.count(token) for token in ['fetch(', 'WebSocket', 'XMLHttpRequest', 'AudioContext', 'localStorage', 'requestPointerLock', 'https://', 'http://', 'GLTFLoader', 'FBXLoader']},
        'note': 'Counts include embedded library capabilities. Inspect call sites and actual browser requests before deciding whether a backend exists.'
    }

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args();result=json.dumps(audit(a.file),ensure_ascii=False,indent=2)
    if a.output: a.output.write_text(result,encoding='utf-8')
    print(result)
