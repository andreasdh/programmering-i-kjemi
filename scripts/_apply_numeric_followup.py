from pathlib import Path
import re

import nbformat as nbf
from nbclient import NotebookClient

NOTEBOOKS = [
    Path("docs/nullpunkter_likninger/likninger.ipynb"),
    Path("docs/derivasjon_integrasjon/derivasjon.ipynb"),
    Path("docs/derivasjon_integrasjon/integrasjon.ipynb"),
    Path("docs/modellering/diskret_modellering.ipynb"),
    Path("docs/modellering/differensiallikninger.ipynb"),
]


def get_cell(nb, cell_id):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            return cell
    raise KeyError(f"Fant ikke celle {cell_id}")


def clean_basthon_wording(text):
    # Keep the technical /basthon/ URL intact, but do not use the product name
    # in text shown to students.
    text = text.replace("### Prøv selv i Basthon", "### Prøv selv")
    text = text.replace("Prøv selv i Basthon", "Prøv selv")
    text = text.replace('title="Basthon:', 'title="Prøv selv:')
    text = text.replace("Basthon-editoren", "editoren")
    text = text.replace("Basthon-editor", "editor")
    text = text.replace("Basthon", "editoren")
    return text


def remove_leibniz_learning_goal(text):
    lines = text.splitlines()
    out = []
    in_learning = False
    number = 1

    for line in lines:
        if line.startswith("```{admonition} Læringsutbytte"):
            in_learning = True
            number = 1
            out.append(line)
            continue

        if in_learning and line.strip() == "```":
            in_learning = False
            out.append(line)
            continue

        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if in_learning and match:
            item = match.group(2)
            if "Leibniz" in item or "bruke både notasjonen" in item:
                continue
            out.append(f"{number}. {item}")
            number += 1
        else:
            out.append(line)

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


notebooks = {}
for path in NOTEBOOKS:
    nb = nbf.read(path, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            cell.source = clean_basthon_wording(cell.source)
            cell.source = remove_leibniz_learning_goal(cell.source)

    notebooks[path] = nb

# --- Likninger/nullpunkter ---
nb = notebooks[Path("docs/nullpunkter_likninger/likninger.ipynb")]
intro = get_cell(nb, "0ab7de5c")
if "Å løse likningen" not in intro.source or "nullpunkt" not in intro.source:
    intro.source += (
        "\nEt **nullpunkt** til en funksjon er en $x$-verdi der funksjonsverdien er 0. "
        "Å løse en likning er derfor det samme som å skrive den på formen $f(x)=0$ og "
        "finne nullpunktet til $f$. Dette kaller vi et **nullpunktsproblem**.\n"
    )

root_cell = get_cell(nb, "0007b951")
root_cell.source = '''from scipy.optimize import root_scalar

bisect_resultat = root_scalar(ladningsbalanse, bracket=[1e-7, 1e-2], method="bisect")

def d_ladningsbalanse(h):
    return 1 + C*Ka/(h + Ka)**2 + Kw/h**2

newton_resultat = root_scalar(ladningsbalanse, x0=4e-4, fprime=d_ladningsbalanse, method="newton")

print("Halvering:")
print("  konvergert:", bisect_resultat.converged)
print("  iterasjoner:", bisect_resultat.iterations)
print("  pH:", -np.log10(bisect_resultat.root))

print("\\nNewton:")
print("  konvergert:", newton_resultat.converged)
print("  iterasjoner:", newton_resultat.iterations)
print("  pH:", -np.log10(newton_resultat.root))
'''

# --- Numerisk integrasjon ---
nb = notebooks[Path("docs/derivasjon_integrasjon/integrasjon.ipynb")]
rect = get_cell(nb, "df1b405a")
rect.source = '''def rektangel_venstre(f, a, b, n):
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
'''

trap = get_cell(nb, "83612c6e")
trap.source = '''def trapesmetoden(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a
    for k in range(n):
        areal = areal + (f(x) + f(x + h)) / 2 * h
        x = x + h
    return areal


print("Trapes:", trapesmetoden(f, 0, 5, 100))
print("Eksakt:", 156.25)
'''

simpson = get_cell(nb, "23f748dc")
simpson.source = '''def simpsons_metode(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n må være et partall.")

    h = (b - a) / n
    areal = 0.0
    x = a
    for k in range(n + 1):
        if k == 0 or k == n:
            areal = areal + f(x)
        elif k % 2 == 0:
            areal = areal + 2*f(x)
        else:
            areal = areal + 4*f(x)
        x = x + h
    return areal * h / 3


print("Simpson:", simpsons_metode(f, 0, 5, 100))
'''

# Save text/code changes before executing.
for path, nb in notebooks.items():
    nbf.write(nb, path)

# Execute every code cell once so outputs and figures are stored in the notebooks.
for path in NOTEBOOKS:
    nb = nbf.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
            cell.metadata.pop("execution", None)

    client = NotebookClient(
        nb,
        timeout=240,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    )
    client.execute()

    # Keep outputs and execution counts, but remove timestamp metadata to avoid noise.
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.metadata.pop("execution", None)

    nbf.validate(nb)
    nbf.write(nb, path)

# Final checks.
for path in NOTEBOOKS:
    nb = nbf.read(path, as_version=4)
    visible_markdown = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
    assert "Basthon" not in visible_markdown
    for cell in nb.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is not None, f"Ikke kjørt kodecelle i {path}: {cell.get('id')}"

likninger = nbf.read(NOTEBOOKS[0], as_version=4)
assert "Et **nullpunkt**" in get_cell(likninger, "0ab7de5c").source
assert "bisect_resultat = root_scalar(ladningsbalanse, bracket=[1e-7, 1e-2], method=\"bisect\")" in get_cell(likninger, "0007b951").source

integrasjon = nbf.read(NOTEBOOKS[2], as_version=4)
for cell_id in ["df1b405a", "83612c6e", "23f748dc"]:
    src = get_cell(integrasjon, cell_id).source
    assert "x = x + h" in src
    assert "areal = 0.0" in src

print("Oppfølgingsrevisjonen er gjennomført og alle kodeceller er kjørt uten feil.")
