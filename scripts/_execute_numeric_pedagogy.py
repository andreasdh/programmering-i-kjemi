import nbformat as nbf
from pathlib import Path
from nbclient import NotebookClient

FILES = [
    Path("docs/nullpunkter_likninger/likninger.ipynb"),
    Path("docs/derivasjon_integrasjon/derivasjon.ipynb"),
    Path("docs/derivasjon_integrasjon/integrasjon.ipynb"),
    Path("docs/modellering/diskret_modellering.ipynb"),
    Path("docs/modellering/differensiallikninger.ipynb"),
]

# Små etterjusteringer som sikrer at bevarte celler fra den nyere versjonen
# har variablene/importene de forventer.
der_path = Path("docs/derivasjon_integrasjon/derivasjon.ipynb")
nb = nbf.read(der_path, as_version=4)
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.source = "import numpy as np\nimport matplotlib.pyplot as plt\n\n" + cell.source
        break
nbf.write(nb, der_path)

int_path = Path("docs/derivasjon_integrasjon/integrasjon.ipynb")
nb = nbf.read(int_path, as_version=4)
for cell in nb.cells:
    if cell.cell_type == "code" and 'print("Venstre:"' in cell.source and "eksakt =" not in cell.source:
        cell.source = cell.source.replace(
            'print("Venstre:", rektangel_venstre(f, 2, 12, 10))',
            'eksakt = (np.sin(12) + 2*12) - (np.sin(2) + 2*2)\n\nprint("Venstre:", rektangel_venstre(f, 2, 12, 10))'
        )
        cell.source = cell.source.replace(
            'print("Midtpunkt:", rektangel_midt(f, 2, 12, 10))',
            'print("Midtpunkt:", rektangel_midt(f, 2, 12, 10))\nprint("Eksakt:", eksakt)'
        )
        break
nbf.write(nb, int_path)

# Kjør og lagre alle kodeceller med inline figurer.
for path in FILES:
    nb = nbf.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=180,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}}
    )
    client.execute()

    # Kontroller at alle kodeceller faktisk ble kjørt og at plt.show-celler
    # har bildeoutput når de lager en figur.
    for cell in nb.cells:
        if cell.cell_type != "code" or not cell.source.strip():
            continue
        if cell.execution_count is None:
            raise RuntimeError(f"Ukjørt kodecelle i {path}")
        if "plt.show()" in cell.source:
            has_png = any(
                out.get("output_type") in {"display_data", "execute_result"}
                and "image/png" in out.get("data", {})
                for out in cell.outputs
            )
            if not has_png:
                raise RuntimeError(f"Figur uten lagret PNG-output i {path}")

    nbf.write(nb, path)

print("Alle fem notebookene er kjørt og kontrollert.")
