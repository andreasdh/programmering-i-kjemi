from __future__ import annotations

import json
import os
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "docs/nullpunkter_likninger/likninger.ipynb",
    ROOT / "docs/derivasjon_integrasjon/derivasjon.ipynb",
    ROOT / "docs/derivasjon_integrasjon/integrasjon.ipynb",
    ROOT / "docs/modellering/diskret_modellering.ipynb",
    ROOT / "docs/modellering/differensiallikninger.ipynb",
]


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def polish_visible_editor_text(nb: dict) -> None:
    """Keep Basthon as implementation detail, not student-facing terminology."""
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        text = text.replace("Prøv selv i Basthon", "Prøv selv")
        text = text.replace("prøv selv i Basthon", "prøv selv")
        text = text.replace("i Basthon", "i editoren")
        text = text.replace("Basthon:", "Prøv selv:")
        set_source(cell, text)


def polish_equations(nb: dict) -> None:
    # Explain explicitly why solving an equation can be turned into finding a zero.
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        marker = "Da har likningsproblemet blitt et **nullpunktsproblem**."
        if marker in text:
            replacement = (
                "Et **nullpunkt** til en funksjon er en $x$-verdi der funksjonsverdien er 0. "
                "Å løse likningen $g(x)=h(x)$ er derfor det samme som å finne nullpunktet til "
                "$f(x)=g(x)-h(x)$. Da har vi formulert likningen som et **nullpunktsproblem**."
            )
            text = text.replace(marker, replacement)
            set_source(cell, text)
            break
    else:
        raise RuntimeError("Fant ikke introduksjonen av nullpunktsproblem.")

    # Keep short SciPy calls on one readable line.
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)
        if "bisect_resultat = root_scalar(" in text:
            text = re.sub(
                r'bisect_resultat = root_scalar\(\s*ladningsbalanse,\s*bracket=\[1e-7, 1e-2\],\s*method="bisect"\s*\)',
                'bisect_resultat = root_scalar(ladningsbalanse, bracket=[1e-7, 1e-2], method="bisect")',
                text,
                flags=re.S,
            )
            text = re.sub(
                r'newton_resultat = root_scalar\(\s*ladningsbalanse,\s*x0=4e-4,\s*fprime=d_ladningsbalanse,\s*method="newton"\s*\)',
                'newton_resultat = root_scalar(ladningsbalanse, x0=4e-4, fprime=d_ladningsbalanse, method="newton")',
                text,
                flags=re.S,
            )
            if "bisect_resultat = root_scalar(\n" in text or "newton_resultat = root_scalar(\n" in text:
                raise RuntimeError("Klarte ikke å gjøre root_scalar-kallene énlinjede.")
            set_source(cell, text)
            return
    raise RuntimeError("Fant ikke SciPy-cellen med root_scalar.")


def polish_derivative(nb: dict) -> None:
    # Remove the requested learning outcome, while keeping the notation explanation in the chapter body.
    first = nb["cells"][0]
    text = source_text(first)
    lines = text.splitlines()
    target_fragment = "bruke både notasjonen $f'(x)$"
    lines = [line for line in lines if target_fragment not in line]

    # Renumber numbered learning outcomes consecutively until the admonition closes.
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
    if target_fragment in new_text:
        raise RuntimeError("Læringsmålet om notasjon ble ikke fjernet.")
    set_source(first, new_text)


def polish_integration(nb: dict) -> None:
    rectangles_done = trapezoid_done = simpson_done = False

    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)

        if "def rektangel_venstre" in text and "def rektangel_hoyre" in text and "def rektangel_midt" in text:
            set_source(
                cell,
                '''def rektangel_venstre(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal


def rektangel_hoyre(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a + h

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal


def rektangel_midt(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a + h/2

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal
''',
            )
            rectangles_done = True

        elif "def trapesmetoden" in text:
            set_source(
                cell,
                '''def trapesmetoden(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a

    for k in range(n):
        areal = areal + (f(x) + f(x + h))/2 * h
        x = x + h

    return areal


print("Trapes:", trapesmetoden(f, 0, 5, 100))
print("Eksakt:", 156.25)
''',
            )
            trapezoid_done = True

        elif "def simpsons_metode" in text:
            set_source(
                cell,
                '''def simpsons_metode(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n må være et partall.")

    h = (b - a) / n
    total = f(a) + f(b)
    x = a + h

    for k in range(1, n):
        if k % 2 == 0:
            total = total + 2*f(x)
        else:
            total = total + 4*f(x)
        x = x + h

    return total * h / 3


print("Simpson:", simpsons_metode(f, 0, 5, 100))
''',
            )
            simpson_done = True

    if not (rectangles_done and trapezoid_done and simpson_done):
        raise RuntimeError(
            f"Fant ikke alle integrasjonsmetodene: "
            f"rektangler={rectangles_done}, trapes={trapezoid_done}, Simpson={simpson_done}"
        )


def update_notebooks() -> None:
    for path in NOTEBOOKS:
        nb = json.loads(path.read_text(encoding="utf-8"))
        polish_visible_editor_text(nb)

        if path.name == "likninger.ipynb":
            polish_equations(nb)
        elif path.name == "derivasjon.ipynb":
            polish_derivative(nb)
        elif path.name == "integrasjon.ipynb":
            polish_integration(nb)

        # Make sure Basthon is not named in student-facing prose. Lower-case basthon remains in iframe src URLs.
        for cell in nb["cells"]:
            if cell.get("cell_type") == "markdown" and "Basthon" in source_text(cell):
                raise RuntimeError(f"Synlig Basthon-henvisning står igjen i {path}: {source_text(cell)[:200]}")

        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def execute_notebooks() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")

    for path in NOTEBOOKS:
        print(f"Executing {path.relative_to(ROOT)}")
        nb = nbformat.read(path, as_version=4)
        client = NotebookClient(
            nb,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
            allow_errors=False,
        )
        client.execute()
        nbformat.write(nb, path)

        code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
        missing = [cell.get("id", "unknown") for cell in code_cells if cell.execution_count is None]
        if missing:
            raise RuntimeError(f"Kodeceller uten execution_count i {path}: {missing}")


def validate_final_state() -> None:
    for path in NOTEBOOKS:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)

    equations = nbformat.read(NOTEBOOKS[0], as_version=4)
    eq_text = "\n".join(cell.source for cell in equations.cells)
    assert "Et **nullpunkt** til en funksjon er en $x$-verdi der funksjonsverdien er 0." in eq_text
    assert 'bisect_resultat = root_scalar(ladningsbalanse, bracket=[1e-7, 1e-2], method="bisect")' in eq_text

    derivative = nbformat.read(NOTEBOOKS[1], as_version=4)
    learning = derivative.cells[0].source
    assert "bruke både notasjonen $f'(x)$" not in learning
    assert "\\frac{df}{dx}" in "\n".join(cell.source for cell in derivative.cells)

    integration = nbformat.read(NOTEBOOKS[2], as_version=4)
    integration_text = "\n".join(cell.source for cell in integration.cells)
    for snippet in ["x = a", "x = a + h", "x = a + h/2", "x = x + h"]:
        assert snippet in integration_text


if __name__ == "__main__":
    update_notebooks()
    execute_notebooks()
    validate_final_state()
    print("Numeriske kapitler er oppdatert, kjørt og validert.")
