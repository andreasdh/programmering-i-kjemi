"""Normalize exercise boxes and add missing solution proposals."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

BASE = Path("docs/grunnleggende_programmering")

SOLUTIONS = {
    "Oppgave 5.4": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
def stoffmengde(masse, molmasse):
    return masse / molmasse


def masse(stoffmengde, molmasse):
    return stoffmengde * molmasse


def konsentrasjon(stoffmengde, volum):
    return stoffmengde / volum


def nodvendig_masse(konsentrasjon, volum, molmasse):
    stoffmengde = konsentrasjon * volum
    return stoffmengde * molmasse

print(stoffmengde(5.844, 58.44))
print(masse(0.100, 58.44))
print(konsentrasjon(0.100, 0.250))
print(nodvendig_masse(0.100, 0.250, 58.44))
```
````""",
    "Oppgave 5.7": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
def stoffmengde(masse, molmasse):
    return masse / molmasse

stoff = input("Oppgi navn på stoffet: ")
masse = float(input("Oppgi massen i gram: "))
molmasse = float(input("Oppgi molmassen i g/mol: "))

n = stoffmengde(masse, molmasse)
print(f"Stoffmengden av {stoff} er {n:.4f} mol.")
```
````""",
    "Oppgave 5.8": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

def pH(oksoniumkonsentrasjon):
    return -np.log10(oksoniumkonsentrasjon)

print(pH(1.0E-2))
print(pH(1.0E-5))
print(pH(1.0E-7))
```
````""",
    "Oppgave 5.9": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
def absorbans(epsilon, lysvei, konsentrasjon):
    return epsilon * lysvei * konsentrasjon


def konsentrasjon(absorbansverdi, epsilon, lysvei):
    return absorbansverdi / (epsilon * lysvei)

c_start = 2.5E-5
A = absorbans(4700, 1.00, c_start)
c_beregnet = konsentrasjon(A, 4700, 1.00)

print(f"Absorbans: {A:.4f}")
print(f"Beregnet konsentrasjon: {c_beregnet:.2e} mol/L")
```
````""",
    "Oppgave 5.11": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
def omsetning(startstoffmengde, sluttstoffmengde):
    omsatt = startstoffmengde - sluttstoffmengde
    omsetningsgrad = omsatt / startstoffmengde * 100
    return omsatt, omsetningsgrad

omsatt, grad = omsetning(0.250, 0.040)
print(f"Omsatt stoffmengde: {omsatt:.3f} mol")
print(f"Omsetningsgrad: {grad:.1f} %")
```
````""",
    "Oppgave 5.13": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
R = 8.314

def trykk(stoffmengde, temperatur, volum):
    return stoffmengde * R * temperatur / volum


def temperatur(trykkverdi, volum, stoffmengde):
    return trykkverdi * volum / (stoffmengde * R)

P = trykk(1.00, 298.15, 0.0245)
T = temperatur(P, 0.0245, 1.00)

print(f"Trykk: {P/1000:.1f} kPa")
print(f"Temperatur: {T:.2f} K")
```
````""",
    "Oppgave 5.15": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

def klassifiser_losning(oksonium, toleranse=0.1):
    pH = -np.log10(oksonium)
    if pH < 7 - toleranse:
        tekst = "sur"
    elif pH > 7 + toleranse:
        tekst = "basisk"
    else:
        tekst = "nøytral"
    return pH, tekst

for konsentrasjon in [1.0E-5, 1.1E-7, 1.0E-9]:
    pH, type_losning = klassifiser_losning(konsentrasjon)
    print(f"pH = {pH:.2f}: {type_losning}")
```
````""",
    "Oppgave 5.17": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
def varmeopptak(masse, varmekapasitet, starttemperatur, sluttemperatur):
    delta_T = sluttemperatur - starttemperatur
    q = masse * varmekapasitet * delta_T
    return q, delta_T

q, delta_T = varmeopptak(100.0, 4.18, 20.0, 27.5)
print(f"Temperaturendring: {delta_T:.1f} °C")
print(f"Varmeopptak: {q:.0f} J")
```
````""",
    "Oppgave 5.18": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

def gyldig_konsentrasjon(konsentrasjon):
    return konsentrasjon > 0


def pH(oksonium):
    if not gyldig_konsentrasjon(oksonium):
        return None
    return -np.log10(oksonium)

print(pH(1.0E-5))
print(pH(0))
```

`None` er en naturlig returverdi når beregningen ikke kan utføres. I et større program kan funksjonen i stedet gi en tydelig feilmelding med `raise ValueError(...)`.
````""",
    "Oppgave 6.1": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

oddetall = np.arange(1, 102, 2)
partall = np.arange(0, 101, 2)
sum_array = oddetall + partall
print(sum_array)
```
````""",
    "Oppgave 6.2": """````{admonition} Løsningsforslag
:class: tip, dropdown

Når `a` og `b` er vanlige lister, betyr `a + b` at listene settes etter hverandre. Når de er NumPy-arrayer med samme form, utføres addisjonen element for element. Et tall kan adderes til hvert element i en array, men ikke direkte til en vanlig liste.
````""",
    "Oppgave 6.3": """````{admonition} Løsningsforslag
:class: tip, dropdown

For NumPy-arrayer utføres `a * b` elementvis. En vanlig liste kan multipliseres med et heltall, men da gjentas lista; tallene i lista multipliseres ikke. To vanlige lister kan ikke multipliseres direkte med hverandre.
````""",
    "Oppgave 6.4": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

tall_i_nigangen = np.arange(9, 1001, 9)
print(tall_i_nigangen)
```
````""",
    "Oppgave 6.5": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

oksonium = np.array([1.0E-2, 1.0E-4, 1.0E-7, 1.0E-10])
pH = -np.log10(oksonium)
print(pH)
```

NumPy-funksjonen virker på hele arrayen, slik at vi ikke trenger en løkke.
````""",
    "Oppgave 6.6": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

v = np.array([2, 2])
w = np.array([1, -3])

skalarprodukt = np.dot(v, w)
print(skalarprodukt)
```

For hånd får vi $2\cdot1 + 2\cdot(-3)=-4$. Vektorene er derfor ikke ortogonale.
````""",
    "Oppgave 6.7": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
import numpy as np

partall = np.arange(0, 11, 2)
tusen_tall = np.linspace(0, 10, 1000)
nedtelling = np.arange(100, 0, -1)

print(partall)
print(tusen_tall)
print(nedtelling)
```
````""",
    "Oppgave 6.8": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
rod = (255, 0, 0)
gronn = (0, 180, 0)
bla = (0, 0, 255)
lilla = (150, 0, 180)

farger = [rod, gronn, bla, lilla]
```

Tuplene kan deretter brukes i samme rekkefølge som sirklene. Dersom grafikkbiblioteket forventer verdier mellom 0 og 1, kan hver komponent deles på 255.
````""",
    "Oppgave 6.9": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
farger = {
    "rød": (255, 0, 0),
    "grønn": (0, 180, 0),
    "blå": (0, 0, 255),
    "gul": (255, 255, 0),
    "lilla": (150, 0, 180),
}

for navn, rgb in farger.items():
    print(f"RGB-koden for {navn} er: {rgb}")
```
````""",
    "Oppgave 6.10": """````{admonition} Løsningsforslag
:class: tip, dropdown

Informasjonen kan samles i en dictionary med elevnavn som nøkler og en ny dictionary med egenskaper som verdi:

```{code-block} Python
elever = {
    "elev_1": {"alder": 16, "fag": "kjemi", "lærer": "Lise"},
    "elev_2": {"alder": 17, "fag": "biologi", "lærer": "Lise"},
    "elev_3": {"alder": 16, "fag": "fysikk", "lærer": "Lise"},
}

print(elever["elev_2"]["fag"])
```

En dictionary samler opplysninger som hører sammen, gir dem meningsfulle nøkler og gjør det enklere å legge til flere elever eller egenskaper.
````""",
    "Oppgave 6.11 (biologi)": """````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} Python
arter = {
    "fjellrev": {
        "klasse": "pattedyr",
        "leveområde": "tundra",
        "føde": "smågnagere",
    },
    "gran": {
        "rike": "planter",
        "leveområde": "barskog",
        "formering": "kongler",
    },
    "torsk": {
        "klasse": "beinfisk",
        "leveområde": "saltvann",
        "føde": "krepsdyr og fisk",
    },
}

print(arter["torsk"]["leveområde"])
```
````""",
}

TITLE_RE = re.compile(r"Oppgave\s+\d+\.\d+(?:\s*\([^\n}]+\))?")
BOLD_RE = re.compile(r"(?m)^\*\*(Oppgave\s+\d+\.\d+(?:\s*[-–][^*]+|\s*\([^*]+\))?)\*\*\s*\n?")
BOUNDARY_RE = re.compile(
    r"(?m)(?=^\*\*Oppgave\s+\d+\.\d+.*\*\*\s*$)"
    r"|(?=^`{3,4}\{admonition\} Løsningsforslag\s*$)"
    r"|(?=^`{3,4}\{admonition\} Oppgave\s+\d+\.\d+.*$)"
)


def markdown_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
        "id": uuid.uuid4().hex[:8],
    }


def fenced_code(cell: dict) -> str:
    code = "".join(cell.get("source", [])).rstrip()
    return f"```{{code-block}} Python\n{code}\n```\n\n"


def normalize_bold_exercises(notebook: dict) -> None:
    cells = notebook["cells"]
    start = next(
        i for i, cell in enumerate(cells)
        if cell.get("cell_type") == "markdown"
        and "## Oppgaver" in "".join(cell.get("source", []))
    )
    before = cells[:start]
    source_cells = cells[start:]
    output: list[dict] = []
    current_title: str | None = None
    current_parts: list[str] = []

    def append_text(text: str) -> None:
        if not text:
            return
        if output and output[-1].get("cell_type") == "markdown":
            old = "".join(output[-1].get("source", []))
            output[-1]["source"] = (old + text).splitlines(keepends=True)
        else:
            output.append(markdown_cell(text))

    def close_current() -> None:
        nonlocal current_title, current_parts
        if current_title is None:
            return
        body = "".join(current_parts).strip()
        append_text(
            f"````{{admonition}} {current_title}\n:class: tip\n\n{body}\n````\n\n"
        )
        current_title = None
        current_parts = []

    for cell in source_cells:
        if cell.get("cell_type") == "code":
            if current_title is not None:
                current_parts.append(fenced_code(cell))
            else:
                output.append(cell)
            continue

        text = "".join(cell.get("source", []))
        for fragment in [x for x in BOUNDARY_RE.split(text) if x]:
            bold = BOLD_RE.match(fragment)
            if bold:
                close_current()
                current_title = bold.group(1)
                remainder = fragment[bold.end():]
                if remainder:
                    current_parts.append(remainder)
                continue

            stripped = fragment.lstrip()
            first = stripped.splitlines()[0] if stripped else ""
            if re.match(r"^`{3,4}\{admonition\} (?:Løsningsforslag|Oppgave )", first):
                close_current()
                append_text(fragment)
            elif current_title is not None:
                current_parts.append(fragment)
            else:
                append_text(fragment)

    close_current()
    notebook["cells"] = before + output


def flatten_exercise_section(notebook: dict) -> tuple[list[dict], str]:
    cells = notebook["cells"]
    start = next(
        i for i, cell in enumerate(cells)
        if cell.get("cell_type") == "markdown"
        and "## Oppgaver" in "".join(cell.get("source", []))
    )
    before = cells[:start]
    parts: list[str] = []
    for cell in cells[start:]:
        if cell.get("cell_type") == "markdown":
            parts.append("".join(cell.get("source", [])))
        elif cell.get("cell_type") == "code":
            parts.append(fenced_code(cell))
    return before, "".join(parts)


def add_solutions(notebook: dict, titles: list[str]) -> None:
    before, text = flatten_exercise_section(notebook)

    markers = []
    for match in re.finditer(r"(?m)^(?:`{3,4}\{admonition\}\s+|\*\*)(Oppgave\s+\d+\.\d+(?:\s*\([^\n}*]+\))?)[^\n]*", text):
        markers.append((match.start(), match.group(1).strip()))

    for index in range(len(markers) - 1, -1, -1):
        start, found_title = markers[index]
        end = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        canonical = next((title for title in titles if found_title.startswith(title)), None)
        if canonical is None:
            continue
        segment = text[start:end]
        if "{admonition} Løsningsforslag" in segment:
            continue
        solution = SOLUTIONS[canonical]
        text = text[:end] + "\n\n" + solution + "\n\n" + text[end:]

    notebook["cells"] = before + [markdown_cell(text)]


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    lister_path = BASE / "lister.ipynb"
    funksjoner_path = BASE / "funksjoner.ipynb"
    datasamlinger_path = BASE / "datasamlinger.ipynb"

    lister = json.loads(lister_path.read_text(encoding="utf-8"))
    funksjoner = json.loads(funksjoner_path.read_text(encoding="utf-8"))
    datasamlinger = json.loads(datasamlinger_path.read_text(encoding="utf-8"))

    normalize_bold_exercises(lister)
    normalize_bold_exercises(datasamlinger)

    add_solutions(
        funksjoner,
        ["Oppgave 5.4", "Oppgave 5.7", "Oppgave 5.8", "Oppgave 5.9", "Oppgave 5.11", "Oppgave 5.13", "Oppgave 5.15", "Oppgave 5.17", "Oppgave 5.18"],
    )
    add_solutions(datasamlinger, [f"Oppgave 6.{i}" for i in range(1, 11)] + ["Oppgave 6.11 (biologi)"])

    save(lister_path, lister)
    save(funksjoner_path, funksjoner)
    save(datasamlinger_path, datasamlinger)

    for path in (lister_path, funksjoner_path, datasamlinger_path):
        json.loads(path.read_text(encoding="utf-8"))

    print("Repaired list exercise boxes and added missing solution proposals.")


if __name__ == "__main__":
    main()
