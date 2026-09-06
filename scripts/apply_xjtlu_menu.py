from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
tag = '<script src="assets/guide-nav.js" defer></script>'
if tag not in text:
    text = text.replace('</body>', tag + '\n</body>')
    p.write_text(text, encoding='utf-8')
    print('Added shared menu loader to index.html')
else:
    print('Shared menu loader already present')
