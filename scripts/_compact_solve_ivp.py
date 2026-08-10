from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

paths = [
    Path("docs/nullpunkter_likninger/likninger.ipynb"),
    Path("docs/derivasjon_integrasjon/derivasjon.ipynb"),
    Path("docs/derivasjon_integrasjon/integrasjon.ipynb"),
    Path("docs/modellering/diskret_modellering.ipynb"),
    Path("docs/modellering/differensiallikninger.ipynb"),
]

ode_path = paths[-1]
nb = nbf.read(ode_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type != "code":
        continue

    if "losning = solve_ivp(" in cell.source:
        old = '''losning = solve_ivp(
    forste_orden,
    [0, 30],
    [1.0],
    t_eval=t_eval,
    rtol=1e-8,
    atol=1e-10
)'''
        new = 'losning = solve_ivp(forste_orden, [0, 30], [1.0], t_eval=t_eval, rtol=1e-8, atol=1e-10)'
        cell.source = cell.source.replace(old, new)

    if "stiv = solve_ivp(" in cell.source:
        old = '''stiv = solve_ivp(
    konsekutive_reaksjoner,
    [0, 200],
    [1.0, 0.0, 0.0],
    t_eval=t_eval,
    method="BDF"
)'''
        new = 'stiv = solve_ivp(konsekutive_reaksjoner, [0, 200], [1.0, 0.0, 0.0], t_eval=t_eval, method="BDF")'
        cell.source = cell.source.replace(old, new)

nbf.write(nb, ode_path)

# Execute all five notebooks again so the final files consistently contain output.
for path in paths:
    nb = nbf.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
            cell.metadata.pop("execution", None)

    NotebookClient(
        nb,
        timeout=240,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    ).execute()

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.metadata.pop("execution", None)
            assert cell.execution_count is not None
            if "plt.show()" in cell.source:
                assert any(
                    out.get("output_type") in {"display_data", "execute_result"}
                    and "image/png" in out.get("data", {})
                    for out in cell.outputs
                ), f"Mangler figur i {path}, celle {cell.get('id')}"

    nbf.validate(nb)
    nbf.write(nb, path)

# Final formatting check.
nb = nbf.read(ode_path, as_version=4)
text = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "code")
assert 'losning = solve_ivp(forste_orden, [0, 30], [1.0], t_eval=t_eval, rtol=1e-8, atol=1e-10)' in text
assert 'stiv = solve_ivp(konsekutive_reaksjoner, [0, 200], [1.0, 0.0, 0.0], t_eval=t_eval, method="BDF")' in text

print("solve_ivp-kall er komprimert, og alle notebooks er kjørt med inline-output.")
