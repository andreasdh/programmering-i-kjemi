from pathlib import Path
import os

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

# Store matplotlib figures as notebook display output instead of only rendering to a GUI backend.
os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"

for path in NOTEBOOKS:
    print(f"Executing {path.relative_to(ROOT)}")
    nb = nbformat.read(path, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []

    NotebookClient(
        nb,
        timeout=180,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    ).execute()

    missing = [cell.get("id", "unknown") for cell in nb.cells if cell.cell_type == "code" and cell.execution_count is None]
    if missing:
        raise RuntimeError(f"Kodeceller uten execution_count i {path}: {missing}")

    nbformat.validate(nb)
    nbformat.write(nb, path)

print("Alle fem notebookene er kjørt med lagret inline-output.")
