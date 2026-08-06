"""Rewrite the molecular visualization notebook around RDKit and nglview."""

import json
from pathlib import Path
from textwrap import dedent


PATH = Path("docs/datahandtering_visualisering/molekylvisualisering.ipynb")


def source(text):
    return dedent(text).strip("\n").splitlines(keepends=True)


def set_cell(cells, cell_id, text):
    for cell in cells:
        if cell.get("id") == cell_id:
            cell["source"] = source(text)
            if cell.get("cell_type") == "code":
                cell["execution_count"] = None
                cell["outputs"] = []
            return
    raise KeyError("Fant ikke celle: " + cell_id)


notebook = json.loads(PATH.read_text(encoding="utf-8"))
cells = notebook["cells"]

set_cell(cells, "856a5047", r"""
# Molekylvisualisering

```{admonition} Læringsutbytte
Etter å ha arbeidet med dette temaet, skal du kunne:

1. tegne ett eller flere små molekyler som strukturformler med `RDKit`
2. framheve bestemte atomer eller strukturmønstre i en molekyltegning
3. generere en mulig tredimensjonal konformasjon fra en SMILES-kode og forklare begrensningene ved modellen
4. tegne proteiner med `nglview` og velge ut bestemte deler av strukturen
5. legge på molekylflater og forklare hva overflaten representerer
6. visualisere en molekyldynamikksimulering som en animasjon
7. velge en representasjon som passer til det kjemiske spørsmålet
```

Så langt har vi i stor grad representert molekyler med tekst og tall, for eksempel SMILES-koder, molekylformler og beregnede egenskaper. Visualisering gir oss en annen type informasjon. Vi kan undersøke hvilke atomer som er bundet sammen, molekylform, funksjonelle grupper, aktive seter i enzymer og hvordan et biomolekyl beveger seg.

En visualisering er en modell som fremhever noen egenskaper og skjuler andre. En todimensjonal strukturformel viser bindinger og funksjonelle grupper tydelig, men sier lite om den romlige formen. En tredimensjonal modell viser formen, men kan gjøre bindingsorden og enkelte strukturdetaljer vanskeligere å se.

I dette kapitlet bruker vi to biblioteker med en tydelig arbeidsdeling:

- `RDKit` brukes til små molekyler: SMILES, strukturformler, strukturmønstre og generering av 3D-konformasjoner.
- `nglview` brukes til interaktiv tredimensjonal visning av molekyler, proteiner og simuleringer.
""")

set_cell(cells, "365428eb", """
## Installasjon

Kjør kodecellen nedenfor én gang for å installere bibliotekene.

`nglview` er en **widget**. Det betyr at den interaktive figuren er koblet til en kjørende Python-kjerne, i stedet for å være et vanlig statisk bilde. I VS Code vises widgeten direkte i output-feltet under kodecellen.

Eldre veiledninger kan inneholde ekstra kommandoer for å aktivere `nglview` som en notebook-utvidelse. I nyere Jupyter-miljøer er dette vanligvis ikke nødvendig.
""")

set_cell(cells, "73179d69", """
!pip install nglview rdkit mdtraj
""")

set_cell(cells, "0ffd4095", r"""
## Hvor kommer strukturene fra?

Små og store molekyler representeres ofte på forskjellige måter:

- **Små molekyler** kan skrives som SMILES. En SMILES-kode beskriver hvilke atomer som finnes og hvordan de er bundet sammen. Koden kan blant annet hentes fra PubChem, men i dette kapitlet bruker vi SMILES-kodene direkte.
- **Proteiner og nukleinsyrer** hentes ofte fra [Protein Data Bank](https://www.rcsb.org/). Hver struktur har en firetegns PDB-ID, for eksempel `1PSN` eller `4HHB`.

Det er viktig å skille mellom de ulike modellene vi lager:

- En **2D-tegning** fra RDKit er en ryddig strukturformel laget ut fra bindingene i molekylet.
- En **3D-konformasjon** generert fra SMILES er en beregnet modell. RDKit lager koordinater og kan justere geometrien med et klassisk kraftfelt.
- En **PDB-struktur** bygger vanligvis på røntgendiffraksjon, kryoelektronmikroskopi eller NMR og har en tilhørende eksperimentell usikkerhet.

Alle tre representasjonene kan være nyttige, men de svarer på forskjellige spørsmål.
""")

set_cell(cells, "650f0ec2", """
## Små molekyler med RDKit

### Tegne en strukturformel

`Chem.MolFromSmiles` leser en SMILES-kode og lager et molekylobjekt. Molekylobjektet inneholder informasjon om atomene, bindingene og bindingsordenen.

`Draw.MolToImage` bruker denne informasjonen til å lage en todimensjonal strukturformel. RDKit beregner selv hvor atomene skal plasseres på arket, slik at tegningen blir oversiktlig.
""")

set_cell(cells, "7dd52530", """
from rdkit import Chem
from rdkit.Chem import Draw

paracetamol = Chem.MolFromSmiles("CC(=O)NC1=CC=C(C=C1)O")

Draw.MolToImage(paracetamol, size=(500, 300))
""")

set_cell(cells, "cfdfd5c8", r"""
Tegningen viser atomtyper, bindinger og bindingsorden. Karbon- og hydrogenatomer følger de vanlige konvensjonene for strukturformler:

- Karbonatomer i kjeden og ringen er vanligvis ikke skrevet med bokstaven C.
- Hydrogenatomer bundet til karbon er vanligvis utelatt.
- Heteroatomer som O og N skrives eksplisitt.
- Enkelt-, dobbelt- og aromatiske bindinger vises forskjellig.

Dette er en **2D-representasjon**. Plasseringen av atomene på skjermen er valgt for å gjøre strukturen lett å lese. Tegningen er ikke en projeksjon av én bestemt tredimensjonal konformasjon.

### Flere molekyler i samme figur

Når vi skal sammenlikne flere molekyler, kan vi samle dem i ei liste og bruke `Draw.MolsToGridImage`. Funksjonen plasserer molekylene i et rutenett og kan skrive en merkelapp under hvert molekyl.
""")

set_cell(cells, "2d8061da", """
smiles = ["CCO", "CC(=O)O", "c1ccccc1"]
navn = ["etanol", "eddiksyre", "benzen"]

molekyler = []

for tekst in smiles:
    molekyl = Chem.MolFromSmiles(tekst)
    molekyler.append(molekyl)

Draw.MolsToGridImage(molekyler, legends=navn, molsPerRow=3)
""")

set_cell(cells, "99157f7a", r"""
```{admonition} Underveisoppgave: Les strukturformlene
:class: tip

Studer de tre strukturene ovenfor.

1. Hvilke bindinger og atomtyper er enklest å se i 2D-tegningene?
2. Hvor mange hydrogenatomer er utelatt i hver struktur?
3. Hvorfor tegnes benzen som en flat seksring, selv om SMILES-koden ikke inneholder koordinater?
4. Bytt ut én av SMILES-kodene med et molekyl du har arbeidet med tidligere, og forklar hvilke strukturelle trekk som blir tydelige i tegningen.

En 2D-tegning er særlig god når vi vil undersøke bindingsmønster, funksjonelle grupper og stereokjemi. Den er mindre egnet når spørsmålet handler om molekylets romlige form.
```
""")

set_cell(cells, "18189ddc", r"""
### Framheve et strukturmønster

RDKit kan framheve bestemte atomer i en strukturformel. Dette er nyttig når vi vil vise hvor en funksjonell gruppe eller et annet SMARTS-mønster finnes i molekylet.

Arbeidsflyten er:

1. lag molekylet fra SMILES
2. lag et søkemønster med `Chem.MolFromSmarts`
3. finn atomene som passer med `GetSubstructMatch`
4. send atomnumrene til `Draw.MolToImage`

`GetSubstructMatch` returnerer en **tuple med atomindekser**. Indeksene forteller hvilke atomer i molekylobjektet som traff mønsteret.
""")

set_cell(cells, "a57e4c79", """
ibuprofen = Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
karboksylsyre = Chem.MolFromSmarts("C(=O)O")

treff = ibuprofen.GetSubstructMatch(karboksylsyre)

Draw.MolToImage(ibuprofen, highlightAtoms=treff, size=(500, 300))
""")

set_cell(cells, "44ac7ef9", r"""
De framhevede atomene utgjør karboksylsyregruppen. Bindingene mellom de markerte atomene blir også framhevet automatisk.

```{admonition} Underveisoppgave: Framhev en funksjonell gruppe
:class: tip

1. Tegn paracetamol og framhev amidgruppen med SMARTS-mønsteret `C(=O)N`.
2. Framhev hydroksylgruppen med mønsteret `[OX2H]`.
3. Kontroller tegningen med kjemikunnskapen din. Treffer mønsteret akkurat de atomene du forventet?
4. Forklar hvorfor en framhevet strukturformel ofte er mer informativ enn bare å skrive antall treff.
```
""")

set_cell(cells, "c00e3307", r"""
### Fra SMILES til en 3D-modell

En SMILES-kode beskriver bindingene, men inneholder vanligvis ikke tredimensjonale koordinater. RDKit kan generere en mulig 3D-konformasjon i tre trinn:

| Kode | Hva som skjer |
|---|---|
| `Chem.AddHs(...)` | legger til hydrogenatomene som er utelatt i SMILES |
| `AllChem.EmbedMolecule(...)` | lager tredimensjonale koordinater |
| `AllChem.MMFFOptimizeMolecule(...)` | justerer geometrien med et klassisk kraftfelt |

RDKit lager selve molekylmodellen. For å rotere og undersøke den interaktivt bruker vi `nglview`, som kan vise et RDKit-molekyl direkte med `nv.show_rdkit`.

`randomSeed=42` gjør at vi får samme startgeometri hver gang koden kjøres. Tallet har ingen kjemisk betydning; det gjør bare eksemplet reproduserbart.
""")

set_cell(cells, "f2cb48d9", """
from rdkit.Chem import AllChem
import nglview as nv

ibuprofen_3d = Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
ibuprofen_3d = Chem.AddHs(ibuprofen_3d)

AllChem.EmbedMolecule(ibuprofen_3d, randomSeed=42)
AllChem.MMFFOptimizeMolecule(ibuprofen_3d)

visning = nv.show_rdkit(ibuprofen_3d)
visning.layout.width = "600px"
visning.layout.height = "400px"
visning
""")

set_cell(cells, "9211e54e", r"""
```{admonition} Underveisoppgave: 2D og 3D viser forskjellige ting
:class: tip

1. Sammenlikn 2D-tegningen og 3D-modellen av ibuprofen. Hvilke strukturtrekk er tydeligst i hver representasjon?
2. Kjør `EmbedMolecule` med tre forskjellige verdier for `randomSeed`. Blir konformasjonene helt like?
3. Prøv det samme med et fleksibelt molekyl med en lengre karbonkjede. Hvorfor blir forskjellene større?
4. Formuler i én setning hva `EmbedMolecule` gir deg, og hva metoden ikke kan garantere.
```

````{admonition} Løsningsforslag
:class: tip, dropdown

1. Strukturformelen viser bindingsorden, ringstruktur og funksjonelle grupper tydeligst. 3D-modellen viser molekylform, vinkler og rotasjon rundt enkeltbindinger tydeligst.

2. Konformasjonene kan bli noe forskjellige fordi metoden starter fra en delvis tilfeldig geometri. Et lite og forholdsvis stivt molekyl gir ofte lignende, men ikke nødvendigvis identiske, resultater.

3. Fleksible molekyler har flere roterbare enkeltbindinger og dermed flere mulige konformasjoner med forholdsvis lav energi.

4. `EmbedMolecule` gir én rimelig tredimensjonal konformasjon. Metoden garanterer ikke at dette er den mest stabile konformasjonen eller den eneste formen molekylet har i løsning.
````
""")

set_cell(cells, "929bad30", """
## Proteiner og simuleringer med nglview

`nglview` gir omfattende kontroll over hvilke deler av en struktur som skal vises. En viktig funksjon er **seleksjonsspråket**, som brukes til å velge bestemte kjeder, aminosyrerester, ligander eller atomgrupper. Dette er særlig nyttig for proteiner.

Biblioteket er også utviklet for **trajektorier**, altså serier av strukturer som viser hvordan et system endrer seg over tid. Det egner seg derfor godt til molekyldynamikksimuleringer.

Vi begynner med pepsin, et enzym i magesekken som bryter proteiner ned til kortere polypeptider.
""")

set_cell(cells, "7a8e8199", r"""
## Arbeidsdeling mellom bibliotekene

Vi trenger ikke to forskjellige biblioteker som gjør den samme jobben. I dette kapitlet har bibliotekene tydelige roller:

| Bibliotek | Brukes til |
|---|---|
| `RDKit` | lese SMILES, tegne 2D-strukturer, framheve strukturmønstre og generere 3D-konformasjoner |
| `nglview` | interaktiv 3D-visning av RDKit-molekyler, PDB-strukturer og trajektorier |
| `mdtraj` | lese og behandle filer fra molekyldynamikksimuleringer |

Dette gir en enkel arbeidsflyt:

1. **Representer eller les strukturen** med RDKit, PDB eller mdtraj.
2. **Velg hva du ønsker å vise.** Det kan være bindinger, et strukturmønster, en ligand, en overflate eller bevegelse.
3. **Velg representasjon** ut fra det kjemiske spørsmålet.
4. **Kontroller hva figuren ikke viser.** En strukturfigur viser ikke automatisk energi, ladningsfordeling eller hvilke konformasjoner som dominerer i løsning.
""")

set_cell(cells, "4908ae05", r"""
## Sluttoppgaver

```{admonition} Oppgave 1: Strukturformler med RDKit
:class: tip

Velg tre molekyler som illustrerer ulike bindingsforhold: ett med bare enkeltbindinger, ett med en dobbeltbinding og ett aromatisk molekyl.

1. Tegn alle tre i samme rutenett med `Draw.MolsToGridImage`.
2. Skriv navn under molekylene med argumentet `legends`.
3. Lag et SMARTS-mønster for én funksjonell gruppe og framhev treffet i minst ett av molekylene.
4. Forklar hvilke kjemiske trekk som blir tydelige i 2D-tegningene, og hva tegningene ikke forteller om molekylformen.
```

```{admonition} Oppgave 2: Et enzym og liganden
:class: tip

Velg et enzym fra PDB som er løst sammen med et substrat, en substratanalog eller en hemmer. Lysozym med en sukkerkjede (`1HEW`) er et godt utgangspunkt.

1. Vis proteinet som bånd og liganden som pinnemodell.
2. Bruk seleksjonsspråket i `nglview` til å vise sidekjedene som ligger nær liganden.
3. Legg på en halvgjennomsiktig overflate og vis at liganden ligger i en lomme.
4. Lag et statisk bilde og skriv en figurtekst som forklarer hva figuren viser.
5. Slå opp den katalytiske mekanismen og forklar hvilke av restene du ser som er involvert.
```

```{admonition} Oppgave 3: Fra SMILES til 3D
:class: tip

Velg et lite molekyl med minst tre roterbare enkeltbindinger.

1. Tegn først en 2D-strukturformel med RDKit.
2. Legg til hydrogenatomer og generer en 3D-konformasjon.
3. Vis konformasjonen med `nv.show_rdkit`.
4. Gjenta med tre forskjellige verdier for `randomSeed`.
5. Diskuter hvilke deler av molekylet som endrer form, og hvorfor én enkelt konformasjon ikke beskriver hele molekylets oppførsel i løsning.
```

```{admonition} Oppgave 4: Din egen figur til en rapport
:class: tip

Lag én figur som du kunne brukt i en labrapport eller presentasjon. Figuren skal:

1. vise et molekyl eller protein som er relevant for noe du har arbeidet med
2. bruke en representasjon som er valgt med en tydelig faglig begrunnelse
3. framheve minst én strukturdel som er viktig for tolkningen
4. lagres som et statisk bilde

Lever figuren sammen med en kort tekst der du begrunner valgene og sier tydelig hva figuren ikke viser.
```
""")

remove_ids = {
    "c2588eb1",
    "7582dde3",
    "d111cf20",
    "59d8c688",
    "540bc1d3",
    "034848ac",
    "6f723ba1",
}

notebook["cells"] = [cell for cell in cells if cell.get("id") not in remove_ids]

all_text = "\n".join(
    "".join(cell.get("source", [])) for cell in notebook["cells"]
)

assert "py3Dmol" not in all_text
assert "query=\"cid:" not in all_text
assert "Draw.MolToImage" in all_text
assert "nv.show_rdkit" in all_text
assert "nv.show_pdbid" in all_text
assert "nv.show_mdtraj" in all_text

PATH.write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)

print("Rewrote", PATH)
