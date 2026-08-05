"""Repair one malformed MyST fence in datasamlinger.ipynb.

The exercise-repair pass accidentally concatenated the closing four-backtick
fence of a tab-set with the opening three-backtick code-block fence. This
script is intentionally small and idempotent so the book can be rebuilt safely.
"""

import json
from pathlib import Path

NOTEBOOK = Path("docs/grunnleggende_programmering/datasamlinger.ipynb")
BROKEN = "```````{code-block} Python"
FIXED = "````\n\n```{code-block} Python"


def main():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    replacements = 0

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue

        source = "".join(cell.get("source", []))
        if BROKEN not in source:
            continue

        source = source.replace(BROKEN, FIXED)
        cell["source"] = source.splitlines(keepends=True)
        replacements += 1

    if replacements > 1:
        raise RuntimeError(
            "Expected at most one malformed fence, found {}".format(replacements)
        )

    if replacements == 1:
        NOTEBOOK.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        print("Repaired malformed tab-set/code-block fence in datasamlinger.ipynb")
    else:
        print("datasamlinger.ipynb already has the correct fence structure")


if __name__ == "__main__":
    main()
