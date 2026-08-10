from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

NOTEBOOKS = [
    Path("docs/nullpunkter_likninger/likninger.ipynb"),
    Path("docs/derivasjon_integrasjon/derivasjon.ipynb"),
    Path("docs/derivasjon_integrasjon/integrasjon.ipynb"),
    Path("docs/modellering/diskret_modellering.ipynb"),
    Path("docs/modellering/differensiallikninger.ipynb"),
]

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

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.metadata.pop("execution", None)
            assert cell.execution_count is not None, f"Ikke kjørt kodecelle i {path}: {cell.get('id')}"
            if "plt.show()" in cell.source:
                has_image = any(
                    output.get("output_type") in {"display_data", "execute_result"}
                    and "image/png" in output.get("data", {})
                    for output in cell.outputs
                )
                assert has_image, f"Figuroutput mangler i {path}, celle {cell.get('id')}"

    nbf.validate(nb)
    nbf.write(nb, path)

print("Alle numeriske notebooks er kjørt med lagret inline figur-output.")
