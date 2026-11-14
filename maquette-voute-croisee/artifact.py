"""Version « page d'artefact » de montage.html : sans <html>/<head>/<body> (le site les ajoute).
Lancer build.py avant, puis : python3 artifact.py  ->  montage-artefact.html"""
import os, re
ICI = os.path.dirname(os.path.abspath(__file__))
h = open(os.path.join(ICI, "montage.html"), encoding="utf-8").read()
h = re.sub(r"<!doctype html>\s*", "", h, flags=re.I)
h = re.sub(r"</?html[^>]*>\s*", "", h)
h = re.sub(r"</?head>\s*", "", h)
h = re.sub(r"</?body>\s*", "", h)
h = re.sub(r'<meta charset="utf-8">\s*', "", h)
h = re.sub(r'<meta name="viewport"[^>]*>\s*', "", h)
assert "<title>" in h[:8192] and 'claude:viewport-fit-sides' in h[:8192]
open(os.path.join(ICI, "montage-artefact.html"), "w", encoding="utf-8").write(h)
print("montage-artefact.html", len(h) // 1024, "Ko")
