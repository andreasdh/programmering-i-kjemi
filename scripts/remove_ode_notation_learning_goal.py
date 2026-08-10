import json
import re
from pathlib import Path

path = Path("docs/modellering/differensiallikninger.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))
cell = nb["cells"][0]
text = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
lines = text.splitlines()

fragment = "bruke både $f'(x)$ og Leibniz-notasjon"
lines = [line for line in lines if fragment not in line]

new_lines = []
in_outcomes = False
number = 1
for line in lines:
    if "```{admonition} Læringsutbytte" in line:
        in_outcomes = True
        new_lines.append(line)
        continue
    if in_outcomes and line.strip() == "```":
        in_outcomes = False
        new_lines.append(line)
        continue
    if in_outcomes and re.match(r"^\d+\.\s", line):
        line = re.sub(r"^\d+\.", f"{number}.", line)
        number += 1
    new_lines.append(line)

new_text = "\n".join(new_lines) + "\n"
if fragment in new_text:
    raise RuntimeError("Læringsmålet ble ikke fjernet.")

cell["source"] = new_text.splitlines(keepends=True)
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("Læringsmålet er fjernet og øvrig forklaring om notasjon er beholdt.")
