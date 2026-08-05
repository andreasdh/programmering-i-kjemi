"""One-off repair of exercise admonitions in the functions notebook."""

from __future__ import annotations

import json
import re
from pathlib import Path


NOTEBOOK = Path("docs/grunnleggende_programmering/funksjoner.ipynb")
EXERCISE_RE = re.compile(r"^\*\*(Oppgave 5\.\d+)\*\*\s*\n+", re.MULTILINE)


def as_source(text: str) -> list[str]:
    """Convert text to the line-list representation used by notebooks."""
    return text.splitlines(keepends=True)


def make_admonition(title: str, body: str, code: str | None) -> str:
    body = body.strip()
    lines = [f"````{{admonition}} {title}", ":class: tip", ""]
    if body:
        lines.extend([body, ""])
    if code is not None:
        lines.extend([
            "```{code-block} Python",
            code.rstrip(),
            "```",
        ])
    lines.append("````")
    return "\n".join(lines) + "\n"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = notebook["cells"]

    exercise_start = next(
        index
        for index, cell in enumerate(cells)
        if cell.get("cell_type") == "markdown"
        and "## Oppgaver" in "".join(cell.get("source", []))
    )

    repaired = 0
    index = exercise_start + 1
    while index < len(cells):
        cell = cells[index]
        if cell.get("cell_type") != "markdown":
            index += 1
            continue

        text = "".join(cell.get("source", []))
        stripped = text.lstrip()
        match = EXERCISE_RE.match(stripped)
        if match is None:
            index += 1
            continue

        title = match.group(1)
        body = stripped[match.end():]
        code = None

        if index + 1 < len(cells) and cells[index + 1].get("cell_type") == "code":
            code = "".join(cells[index + 1].get("source", []))
            del cells[index + 1]

        cell["source"] = as_source(make_admonition(title, body, code))
        repaired += 1
        index += 1

    remaining_bold = []
    for cell in cells[exercise_start + 1:]:
        if cell.get("cell_type") == "markdown":
            text = "".join(cell.get("source", []))
            remaining_bold.extend(EXERCISE_RE.findall(text.lstrip()))

    if remaining_bold:
        raise RuntimeError(
            "Bold exercise headings remain after repair: " + ", ".join(remaining_bold)
        )
    if repaired < 1:
        raise RuntimeError("No exercise admonitions were repaired")

    NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"Repaired {repaired} exercise admonitions in {NOTEBOOK}")


if __name__ == "__main__":
    main()
