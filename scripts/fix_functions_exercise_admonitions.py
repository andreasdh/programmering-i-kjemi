"""One-off repair of exercise admonitions in the functions notebook."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path


NOTEBOOK = Path("docs/grunnleggende_programmering/funksjoner.ipynb")
BOLD_EXERCISE_RE = re.compile(r"(?m)^\*\*(Oppgave 5\.\d+)\*\*\s*\n?")
BOUNDARY_RE = re.compile(
    r"(?m)(?=^\*\*Oppgave 5\.\d+\*\*\s*$)"
    r"|(?=^`{3,4}\{admonition\} Løsningsforslag\s*$)"
    r"|(?=^`{3,4}\{admonition\} Oppgave 5\.\d+\s*$)"
)


def markdown_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
        "id": uuid.uuid4().hex[:8],
    }


def append_markdown(cells: list[dict], text: str) -> None:
    if not text:
        return
    if cells and cells[-1].get("cell_type") == "markdown":
        current = "".join(cells[-1].get("source", []))
        cells[-1]["source"] = (current + text).splitlines(keepends=True)
    else:
        cells.append(markdown_cell(text))


def fenced_code(cell: dict) -> str:
    code = "".join(cell.get("source", [])).rstrip()
    return f"```{{code-block}} Python\n{code}\n```\n"


def close_exercise(output: list[dict], title: str | None, parts: list[str]) -> tuple[None, list[str]]:
    if title is None:
        return None, []
    body = "".join(parts).strip()
    text = f"````{{admonition}} {title}\n:class: tip\n\n{body}\n````\n\n"
    append_markdown(output, text)
    return None, []


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = notebook["cells"]

    start_index = next(
        index
        for index, cell in enumerate(cells)
        if cell.get("cell_type") == "markdown"
        and "## Oppgaver" in "".join(cell.get("source", []))
    )

    before = cells[:start_index]
    exercise_cells = cells[start_index:]
    output: list[dict] = []
    current_title: str | None = None
    current_parts: list[str] = []
    repaired_titles: list[str] = []

    for cell in exercise_cells:
        if cell.get("cell_type") == "code":
            if current_title is not None:
                current_parts.append(fenced_code(cell))
            else:
                output.append(cell)
            continue

        text = "".join(cell.get("source", []))
        fragments = [fragment for fragment in BOUNDARY_RE.split(text) if fragment]

        for fragment in fragments:
            bold_match = BOLD_EXERCISE_RE.match(fragment)
            if bold_match:
                current_title, current_parts = close_exercise(
                    output, current_title, current_parts
                )
                current_title = bold_match.group(1)
                repaired_titles.append(current_title)
                remainder = fragment[bold_match.end():]
                if remainder:
                    current_parts.append(remainder)
                continue

            stripped = fragment.lstrip()
            is_solution = re.match(
                r"^`{3,4}\{admonition\} Løsningsforslag\s*$",
                stripped.splitlines()[0] if stripped else "",
            )
            is_existing_exercise = re.match(
                r"^`{3,4}\{admonition\} Oppgave 5\.\d+\s*$",
                stripped.splitlines()[0] if stripped else "",
            )

            if is_solution or is_existing_exercise:
                current_title, current_parts = close_exercise(
                    output, current_title, current_parts
                )
                append_markdown(output, fragment)
            elif current_title is not None:
                current_parts.append(fragment)
            else:
                append_markdown(output, fragment)

    close_exercise(output, current_title, current_parts)
    notebook["cells"] = before + output

    full_text = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )
    remaining = BOLD_EXERCISE_RE.findall(full_text)
    if remaining:
        raise RuntimeError(
            "Bold exercise headings remain after repair: " + ", ".join(remaining)
        )
    if "Oppgave 5.1" not in repaired_titles:
        raise RuntimeError("Oppgave 5.1 was not repaired")

    NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(
        f"Repaired {len(repaired_titles)} exercise admonitions in {NOTEBOOK}: "
        + ", ".join(repaired_titles)
    )


if __name__ == "__main__":
    main()
