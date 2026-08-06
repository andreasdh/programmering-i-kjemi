"""Simplify the chemical libraries notebook for beginners."""

import json
from pathlib import Path

PATH = Path("docs/datahandtering_visualisering/kjemiske_biblioteker.ipynb")


def lines(text):
    return text.strip("\n").splitlines(keepends=True)


def set_cell(cells, cell_id, text):
    for cell in cells:
        if cell.get("id") == cell_id:
            cell["source"] = lines(text)
            cell["execution_count"] = None if cell.get("cell_type") == "code" else cell.get("execution_count")
            if cell.get("cell_type") == "code":
                cell["outputs"] = []
            return
    raise KeyError(cell_id)


notebook = json.loads(PATH.read_text(encoding="utf-8"))
cells = notebook["cells"]

set_cell(cells, "18f5f82a", """
#### Flere grunnstoffer med lister

Vi trenger ikke hente hele periodesystemet som en tabell for å undersøke en enkel trend. I stedet kan vi lage ei liste med grunnstoffsymboler og hente ett grunnstoff om gangen.

Dette bygger på lister og løkker, som vi allerede kjenner. Det gjør også koden lettere å lese: Vi ser tydelig hvilke grunnstoffer som er med, og hvilke egenskaper vi henter.
""")

set_cell(cells, "bc7f0e00", """
# Grunnstoffene i andre periode
symboler = ["Li", "Be", "B", "C", "N", "O", "F", "Ne"]

for symbol in symboler:
    grunnstoff = element(symbol)
    print(symbol, grunnstoff.atomic_number, grunnstoff.atomic_weight)
""")

set_cell(cells, "329797b8", """
#### Manglende verdier

Et bibliotek har ikke nødvendigvis en verdi for alle egenskaper til alle grunnstoffer. Dersom en verdi mangler, får vi ofte `None`.

Vi bør derfor kontrollere verdien før vi bruker den i en beregning eller et plott.
""")

set_cell(cells, "de89a56e", """
symboler_uten_verdi = []

for atomnummer in range(1, 119):
    grunnstoff = element(atomnummer)
    elektronegativitet = grunnstoff.electronegativity("pauling")

    if elektronegativitet is None:
        symboler_uten_verdi.append(grunnstoff.symbol)

print("Grunnstoff uten Pauling-elektronegativitet:")
print(symboler_uten_verdi)
""")

set_cell(cells, "02d6f1c5", """
```{admonition} Underveisoppgave: Hvilke verdier mangler?
:class: tip

Studer lista ovenfor.

1. Én gruppe i periodesystemet er tydelig representert. Hvilken gruppe er dette, og hva kan være den kjemiske forklaringen?
2. Flere av de tyngste grunnstoffene mangler også verdier. Hvorfor er det vanskelig å bestemme kjemiske egenskaper for disse?
3. Lag to lister: én med atomnummer og én med Pauling-elektronegativitet. Legg bare til grunnstoffer som faktisk har en verdi, og lag deretter et spredningsplott.
```

````{admonition} Løsningsforslag
:class: tip, dropdown

1. **Edelgassene** er tydelig representert. Paulings skala bygger på bindingsenergier, og edelgassene danner få vanlige bindinger.
2. Mange av de tyngste grunnstoffene er framstilt i svært små mengder og har korte halveringstider. Det gjør målinger vanskelige.
3. Vi kan kontrollere verdien med en `if`-test før vi legger den til i listene:

```{code-block} python
import matplotlib.pyplot as plt

atomnumre = []
elektronegativiteter = []

for atomnummer in range(1, 119):
    grunnstoff = element(atomnummer)
    verdi = grunnstoff.electronegativity("pauling")

    if verdi is not None:
        atomnumre.append(atomnummer)
        elektronegativiteter.append(verdi)

plt.scatter(atomnumre, elektronegativiteter)
plt.xlabel("Atomnummer")
plt.ylabel("Elektronegativitet (Pauling)")
plt.show()
```
````
""")

set_cell(cells, "519d823c", """
#### Trender innenfor en periode

For andre periode kan vi bruke symbolene direkte på x-aksen. Da slipper vi både tabellbehandling og ekstra kode for å skrive symbolene ved hvert punkt.
""")

set_cell(cells, "a925f8ff", """
import matplotlib.pyplot as plt

symboler = ["Li", "Be", "B", "C", "N", "O", "F"]
elektronegativiteter = []

for symbol in symboler:
    grunnstoff = element(symbol)
    verdi = grunnstoff.electronegativity("pauling")
    elektronegativiteter.append(verdi)

plt.plot(symboler, elektronegativiteter, marker="o")
plt.xlabel("Grunnstoff")
plt.ylabel("Elektronegativitet (Pauling)")
plt.title("Elektronegativitet i andre periode")
plt.show()
""")

set_cell(cells, "527effd0", """
```{admonition} Underveisoppgave: Forklar to trender
:class: tip

1. Beskriv trenden fra litium til fluor og forklar den ut fra kjerneladning og skjerming.
2. Lag et tilsvarende plott for halogenene med lista `["F", "Cl", "Br", "I"]`.
3. Går trenden samme vei nedover i ei gruppe som bortover i en periode? Forklar forskjellen.
```

````{admonition} Løsningsforslag
:class: tip, dropdown

Elektronegativiteten øker fra litium til fluor. Kjerneladningen øker, mens elektronene legges i det samme hovedskallet. Effektiv kjerneladning øker derfor, og valenselektronene holdes sterkere.

Nedover i ei gruppe minker elektronegativiteten. Valenselektronene befinner seg lenger fra kjernen og skjermes av flere indre elektronskall.

```{code-block} python
halogener = ["F", "Cl", "Br", "I"]
verdier = []

for symbol in halogener:
    grunnstoff = element(symbol)
    verdier.append(grunnstoff.electronegativity("pauling"))

plt.plot(halogener, verdier, marker="o")
plt.xlabel("Grunnstoff")
plt.ylabel("Elektronegativitet (Pauling)")
plt.show()
```
````
""")

set_cell(cells, "a43a7e2d", """
```{admonition} Underveisoppgave: Det store spranget
:class: tip

Hent ut de fem første ioniseringsenergiene til magnesium og plott dem mot ioniseringsgrad.

Hvor kommer det store spranget, og hvorfor akkurat der? Hva forteller dette om elektronstrukturen til magnesium?
```

````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} python
magnesium = element("Mg")

grader = [1, 2, 3, 4, 5]
energier = []

for grad in grader:
    energier.append(magnesium.ionenergies[grad])

plt.plot(grader, energier, marker="o")
plt.xlabel("Ioniseringsgrad")
plt.ylabel("Ioniseringsenergi (eV)")
plt.show()
```

Spranget kommer mellom den andre og den tredje ioniseringen. De to første elektronene tas fra 3s-orbitalen. Det tredje må tas fra et fylt indre skall og krever derfor mye mer energi.
````
""")

set_cell(cells, "0412cc20", """
navn_liste = ["koffein", "aspirin", "ibuprofen", "askorbinsyre"]

for navn in navn_liste:
    forbindelse = pcp.get_compounds(navn, "name")[0]
    print(navn)
    print("  CID:", forbindelse.cid)
    print("  Formel:", forbindelse.molecular_formula)
    print("  Molar masse:", forbindelse.molecular_weight, "g/mol")
""")

set_cell(cells, "b8e8f948", """
```{admonition} Underveisoppgave: Hent flere forbindelser
:class: tip

Lag ei liste med fem legemidler eller naturstoffer. Bruk en løkke til å hente molekylformel, molar masse og CID for hvert stoff, og skriv verdiene ut på en ryddig måte.

Ta vare på CID-ene. Du får bruk for dem når vi skal visualisere molekylene.
```

````{admonition} Løsningsforslag
:class: tip, dropdown

```{code-block} python
navn_liste = ["koffein", "nikotin", "morfin", "penicillin G", "kolesterol"]

for navn in navn_liste:
    forbindelse = pcp.get_compounds(navn, "name")[0]
    print(navn, forbindelse.cid, forbindelse.molecular_formula,
          forbindelse.molecular_weight)
```
````
""")

set_cell(cells, "d66c1de7", """
smiles = {
    "koffein": "CN1C=NC2=C1C(=O)N(C)C(=O)N2C",
    "paracetamol": "CC(=O)Nc1ccc(O)cc1",
    "acetylsalisylsyre": "CC(=O)Oc1ccccc1C(=O)O",
    "ibuprofen": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
}

molekyler = []
navn = []

for stoffnavn in smiles:
    molekyl = Chem.MolFromSmiles(smiles[stoffnavn])
    molekyler.append(molekyl)
    navn.append(stoffnavn)

Draw.MolsToGridImage(molekyler, legends=navn, molsPerRow=4)
""")

set_cell(cells, "f39b17ea", """
for navn in smiles:
    molekyl = Chem.MolFromSmiles(smiles[navn])

    print(navn)
    print("  Molar masse:", round(Descriptors.MolWt(molekyl), 2))
    print("  logP:", round(Descriptors.MolLogP(molekyl), 2))
    print("  TPSA:", round(Descriptors.TPSA(molekyl), 1))
    print("  H-donorer:", Descriptors.NumHDonors(molekyl))
    print("  H-akseptorer:", Descriptors.NumHAcceptors(molekyl))
""")

set_cell(cells, "1db18d38", """
monstre = {
    "karboksylsyre": "[CX3](=O)[OX2H1]",
    "ester": "[CX3](=O)[OX2][CX4]",
    "amid": "[CX3](=O)[NX3]",
    "alkohol/fenol": "[OX2H]",
    "aromatisk ring": "c1ccccc1",
}

for navn in smiles:
    molekyl = Chem.MolFromSmiles(smiles[navn])
    print(navn)

    for gruppe in monstre:
        mal = Chem.MolFromSmarts(monstre[gruppe])
        antall = len(molekyl.GetSubstructMatches(mal))
        print(" ", gruppe, antall)
""")

set_cell(cells, "8156c806", """
import sympy as sp

#                a   b   c   d
A = sp.Matrix([[6, 0, -1, 0],
               [6, 0, 0, -2],
               [0, 2, -1, -1]])

losning = A.nullspace()[0]
print(losning)

# SymPy gir forholdet mellom koeffisientene.
# Her ganger vi med 2 for å få hele tall.
koeffisienter = losning * 2
print(list(koeffisienter))
""")

set_cell(cells, "b48557a6", """
import numpy as np


def ladningsbalanse(h, Ka, c, Kw=1.0e-14):
    A_minus = Ka * c / (Ka + h)
    OH = Kw / h
    return h - A_minus - OH


def halveringsmetoden(f, a, b, n=100):
    for _ in range(n):
        midtpunkt = (a + b) / 2

        if f(a) * f(midtpunkt) < 0:
            b = midtpunkt
        else:
            a = midtpunkt

    return (a + b) / 2


def funksjon(h):
    return ladningsbalanse(h, 1.75e-5, 0.010)


h = halveringsmetoden(funksjon, 1.0e-14, 1.0)
print("pH med egen kode:", round(-np.log10(h), 3))
print("pH med pHcalc:", round(losning.pH, 3))
""")

set_cell(cells, "ce79dc6c", """
## Sluttoppgaver

Oppgavene nedenfor bruker lister, løkker, funksjoner og enkle plott. Du trenger ikke Pandas.

```{admonition} Oppgave 1: Trender i periodesystemet
:class: tip

1. Velg én periode eller gruppe i periodesystemet.
2. Lag ei liste med grunnstoffsymbolene.
3. Bruk `mendeleev` til å hente én egenskap, for eksempel elektronegativitet eller første ioniseringsenergi.
4. Lag et plott og forklar trenden kjemisk.
```

```{admonition} Oppgave 2: Fra navn til struktur til egenskap
:class: tip

Velg fem legemidler eller naturstoffer.

1. Hent CID, molekylformel og molar masse fra PubChem.
2. Hent eller slå opp SMILES og les strukturene inn i RDKit.
3. Skriv ut molar masse, logP og TPSA for hvert molekyl.
4. Tegn strukturene med `Draw.MolsToGridImage`.
5. Sammenlikn resultatene og beskriv minst én kjemisk sammenheng du ser.
```

```{admonition} Oppgave 3: Titrering med to metoder
:class: tip

Beregn noen utvalgte punkter på en titrerkurve både med din egen nullpunktsmetode og med `pHcalc`. Sammenlikn svarene og forklar når det er nyttig å bruke et bibliotek.
```

```{admonition} Oppgave 4: Balansering og utbytte
:class: tip

Balanser termittreaksjonen med matrisemetoden. Bruk deretter egne funksjoner til å beregne begrensende reaktant og teoretisk utbytte.
```

```{admonition} Oppgave 5: Vurder et kjemibibliotek
:class: tip

Finn et kjemibibliotek som ikke er nevnt i kapitlet. Beskriv kort hva det gjør, test ett enkelt eksempel, og vurder om du ville brukt det i et studentprosjekt.
```
""")

# The notebook should not introduce pandas before the data-handling chapter.
text = json.dumps(notebook, ensure_ascii=False)
for forbidden in ("import pandas", "DataFrame", "iterrows", "fetch_table"):
    if forbidden in text:
        raise RuntimeError("Still contains forbidden beginner-level construct: " + forbidden)

PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("Simplified", PATH)
