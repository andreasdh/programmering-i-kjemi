import nbformat as nbf
from pathlib import Path

FILES = {
    "likninger": Path("docs/nullpunkter_likninger/likninger.ipynb"),
    "derivasjon": Path("docs/derivasjon_integrasjon/derivasjon.ipynb"),
    "integrasjon": Path("docs/derivasjon_integrasjon/integrasjon.ipynb"),
    "diskret": Path("docs/modellering/diskret_modellering.ipynb"),
    "ode": Path("docs/modellering/differensiallikninger.ipynb"),
}


def md(text):
    return nbf.v4.new_markdown_cell(text.strip() + "\n")


def code(text):
    c = nbf.v4.new_code_cell(text.strip() + "\n")
    c.execution_count = None
    c.outputs = []
    return c


def text(cell):
    return cell.source if isinstance(cell.source, str) else "".join(cell.source)


def find_heading(nb, heading, start=0):
    for i in range(start, len(nb.cells)):
        c = nb.cells[i]
        if c.cell_type == "markdown" and text(c).lstrip().startswith(heading):
            return i
    raise ValueError(f"Fant ikke overskriften {heading}")


def save(nb, path):
    nbf.write(nb, path)


# -----------------------------------------------------------------------------
# LIKNINGER OG NULLPUNKTER
# -----------------------------------------------------------------------------
path = FILES["likninger"]
nb = nbf.read(path, as_version=4)
lib_i = find_heading(nb, "## Ferdige metoder")
rest = nb.cells[lib_i:]

intro = [
md(r'''# Likninger og nullpunkter

```{admonition} Læringsutbytte
Etter å ha arbeidet med denne delen av emnet, skal du kunne:

1. forklare hva et nullpunktsproblem er, og formulere likninger som $f(x)=0$
2. forklare den teoretiske bakgrunnen for halveringsmetoden og Newtons metode
3. implementere metodene med enkel Python-kode
4. bruke toleranse til å kontrollere en numerisk beregning
5. drøfte styrker, svakheter og konvergens for metodene
6. bruke ferdige nullpunktsløsere i SciPy på kjemiske problemer
```

## Likninger som nullpunktsproblemer

Å løse en likning og å finne et nullpunkt er egentlig det samme problemet skrevet på to ulike måter. Hvis vi har

$$g(x)=h(x),$$

kan vi flytte alt over på én side:

$$f(x)=g(x)-h(x)=0.$$

Et **nullpunkt** er en verdi av $x$ der funksjonsverdien er 0. Å løse likningen $g(x)=h(x)$ betyr derfor å finne den verdien av $x$ som gjør $f(x)=0$. Det er dette vi mener når vi sier at vi **formulerer likningen som et nullpunktsproblem**.

For andregradslikninger kjenner vi en egen løsningsformel. For mer kompliserte likninger finnes det ikke alltid et praktisk analytisk uttrykk for løsningen. Numeriske metoder er mer generelle: De prøver i stedet å nærme seg løsningen steg for steg.
'''),
md(r'''## Et kjemisk eksempel: pH i en svak syre

Vi bruker en 0,010 M løsning av eddiksyre som eksempel. For en enprotisk svak syre med total konsentrasjon $C$ kan vi kombinere massebalansen og syrekonstanten og skrive

$$[\mathrm{A^-}]=C\frac{K_a}{[\mathrm{H_3O^+}]+K_a}.$$

Ladningsbalansen er

$$[\mathrm{H_3O^+}]=[\mathrm{A^-}]+[\mathrm{OH^-}],$$

og vannets ionprodukt gir

$$[\mathrm{OH^-}]=\frac{K_w}{[\mathrm{H_3O^+}]}.$$

Hvis vi setter $h=[\mathrm{H_3O^+}]$, kan hele problemet samles i én funksjon:

$$f(h)=h-C\frac{K_a}{h+K_a}-\frac{K_w}{h}.$$

pH-en finnes når ladningsbalansen er oppfylt, altså når $f(h)=0$. Vi trenger med andre ord ikke isolere $h$ algebraisk. Det holder at vi kan beregne $f(h)$ og lete etter nullpunktet.
'''),
code(r'''import numpy as np
import matplotlib.pyplot as plt

C = 0.010
Ka = 1.75e-5
Kw = 1.0e-14

def ladningsbalanse(h):
    A_minus = C * Ka / (h + Ka)
    OH = Kw / h
    return h - A_minus - OH

h = np.logspace(-7, -2, 500)
plt.semilogx(h, ladningsbalanse(h))
plt.axhline(0)
plt.xlabel(r"$[\mathrm{H_3O^+}]$ (mol/L)")
plt.ylabel("Ladningsbalanse")
plt.show()'''),
md(r'''## Fra graf til algoritme

Før vi prøver å løse en likning numerisk, er det ofte lurt å **se på problemet**. En graf kan fortelle oss omtrent hvor nullpunktet ligger, om det finnes flere nullpunkter, og hvilke startverdier som kan være fornuftige.

En svært enkel idé er å starte ved en verdi $x$ og flytte oss bortover grafen med en fast steglengde $dx$. For hvert steg sammenlikner vi fortegnet til $f(x)$ og $f(x+dx)$. Hvis fortegnet skifter, må et nullpunkt ligge mellom punktene, så lenge funksjonen er kontinuerlig.

<img src="../bilder/brute_force_likninger.png" width="500"/>

I figuren har $f(x_7)$ og $f(x_8)$ motsatt fortegn. Nullpunktet må derfor ligge et sted mellom $x_7$ og $x_8$. Vi kan bruke midtpunktet som et første estimat.

Dette er intuitivt, men ikke særlig effektivt. Hvis $dx$ er stort, blir svaret grovt. Hvis $dx$ er lite, må vi gå gjennom svært mange punkter. Ideen om **fortegnsskifte** er likevel viktig, for den leder direkte til halveringsmetoden.
'''),
code(r'''def f(x):
    return x**2 - x - 2

x = -5
x_slutt = 5
dx = 0.5

while x < x_slutt and f(x)*f(x + dx) > 0:
    x = x + dx

nullpunkt = (x + x + dx)/2
print("Et første estimat er x =", nullpunkt)'''),
md(r'''## Halveringsmetoden

I stedet for å gå gjennom hele intervallet med like store steg kan vi være smartere. Vi starter med et intervall $[a,b]$ der $f(a)$ og $f(b)$ har motsatt fortegn. Så deler vi intervallet i to og **kaster den halvparten som ikke kan inneholde nullpunktet**.

La oss først se på den enkleste mulige koden. Her velger vi bevisst en funksjon med et nullpunkt som algoritmen kan treffe nøyaktig, slik at selve ideen er lett å følge.
'''),
code(r'''def f(x):
    return 2*x - 2

a = -5
b = 5
m = (a + b)/2

while f(m) != 0:
    if f(a)*f(m) < 0:
        b = m
    elif f(b)*f(m) < 0:
        a = m
    m = (a + b)/2

print("Nullpunktet er x =", m)'''),
md(r'''Studer koden linje for linje. Hver runde gjør intervallet halvparten så stort. Det er derfor metoden kalles **halveringsmetoden**.

Mer generelt går metoden slik:

1. Velg et intervall $[a,b]$ der $f(a)$ og $f(b)$ har motsatt fortegn.
2. Finn midtpunktet

$$m=\frac{a+b}{2}.$$

3. Undersøk hvilken av halvdelene $[a,m]$ eller $[m,b]$ som fortsatt har et fortegnsskifte.
4. Behold denne halvdelen og gjenta.

<img src="../bilder/halveringsmetoden.png" width="500"/>

Figuren viser to runder. Poenget er ikke at vi kjenner nullpunktet på forhånd, men at vi hele tiden vet **hvilken halvdel det må ligge i**.

### Fra eksakt likhet til toleranse

I reelle numeriske problemer bør vi ikke vente på at `f(m) == 0`. Flyttall og kompliserte funksjoner gjør at vi ofte aldri treffer null helt nøyaktig. I stedet bestemmer vi hvor nær null som er godt nok. Dette kalles en **toleranse**.
'''),
code(r'''def f(x):
    return x**2 - x - 2

a = 0
b = 5
toleranse = 1E-8
m = (a + b)/2

while abs(f(m)) > toleranse:
    if f(a)*f(m) < 0:
        b = m
    elif f(b)*f(m) < 0:
        a = m
    m = (a + b)/2

print("Nullpunktet er x =", m)
print("f(x) =", f(m))'''),
md(r'''Nå har vi først forstått algoritmen som en konkret løkke. Da er det naturlig å pakke den inn i en funksjon slik at vi kan bruke den på flere problemer uten å skrive koden på nytt.
'''),
code(r'''def halveringsmetoden(f, a, b, tol=1E-10, maks_iterasjoner=100):
    i = 0
    m = (a + b)/2

    while i < maks_iterasjoner and abs(f(m)) > tol:
        if f(a)*f(m) < 0:
            b = m
        elif f(b)*f(m) < 0:
            a = m
        m = (a + b)/2
        i = i + 1

    if i == maks_iterasjoner:
        print("Maks antall iterasjoner er nådd.")

    return m, i'''),
md(r'''Vi kan nå bruke den samme funksjonen på pH-problemet vårt:
'''),
code(r'''h_null, antall = halveringsmetoden(ladningsbalanse, 1e-7, 1e-2)
pH = -np.log10(h_null)

print(f"[H3O+] = {h_null:.6e} mol/L")
print(f"pH = {pH:.3f}")
print("Iterasjoner:", antall)'''),
md(r'''### Prøv selv

Fullfør halveringsmetoden i editoren og bruk den til å finne pH i den svake syra.

<iframe src="../../basthon/?from=examples/numeriske_likninger_halvering.py" width="100%" height="600" frameborder="0" title="Prøv selv: halveringsmetoden" loading="lazy" allowfullscreen></iframe>
'''),
md(r'''## Newtons metode

Halveringsmetoden utnytter at nullpunktet ligger **mellom** to punkter. Newtons metode bruker en annen idé: Tangenten i ett punkt kan brukes til å gjette hvor nullpunktet ligger.

1. Velg et startgjett $x_0$.
2. Tegn eller tenk deg tangenten i $(x_0,f(x_0))$.
3. Finn hvor tangenten skjærer x-aksen. Dette blir neste gjett, $x_1$.
4. Gjenta prosessen med tangenten i det nye punktet.

<img src="../bilder/newtonsmetode.png" width="500"/>

Figuren viser hvorfor metoden ofte nærmer seg nullpunktet mye raskere enn halveringsmetoden.

La oss utlede formelen. Tangenten gjennom $(x_n,f(x_n))$ har stigning $f'(x_n)$:

$$y=f(x_n)+f'(x_n)(x-x_n).$$

Vi vil finne tangentens nullpunkt, så vi setter $y=0$:

$$0=f(x_n)+f'(x_n)(x-x_n).$$

Løser vi med hensyn på $x$, får vi neste estimat:

$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.$$

Igjen begynner vi med den enkleste mulige implementeringen før vi lager en generell funksjon.
'''),
code(r'''def f(x):
    return x**2 - x - 2

def fder(x):
    return 2*x - 1

x = 5
toleranse = 1E-8

while abs(f(x)) > toleranse:
    x = x - f(x)/fder(x)

print("Nullpunktet er x =", x)'''),
md(r'''Når algoritmen er forståelig som en enkel løkke, kan vi pakke den inn i en funksjon:
'''),
code(r'''def newtons_metode(f, fder, x, tol=1E-10):
    while abs(f(x)) > tol:
        x = x - f(x)/fder(x)
    return x'''),
md(r'''Newtons metode trenger bare ett startgjett og konvergerer ofte raskt. Ulempen er at vi trenger den deriverte, og et uheldig startgjett kan føre oss til feil nullpunkt eller gjøre at metoden ikke konvergerer. Her er det viktigere å **forstå begrensningen** enn å bygge omfattende feilhåndtering inn i den første koden.

Senere, når vi bruker ferdige bibliotekfunksjoner, får vi mer robusthet og informasjon om hvorvidt metoden faktisk konvergerte.
'''),
]

nb.cells = intro + rest
# Gjør korte root_scalar-kall kompakte og fjern eventuell raise fra resten.
for c in nb.cells:
    if c.cell_type == "code":
        s = text(c)
        s = s.replace('bisect_resultat = root_scalar(\n    ladningsbalanse,\n    bracket=[1e-7, 1e-2],\n    method="bisect"\n)', 'bisect_resultat = root_scalar(ladningsbalanse, bracket=[1e-7, 1e-2], method="bisect")')
        s = s.replace('newton_resultat = root_scalar(\n    ladningsbalanse,\n    x0=4e-4,\n    fprime=d_ladningsbalanse,\n    method="newton"\n)', 'newton_resultat = root_scalar(ladningsbalanse, x0=4e-4, fprime=d_ladningsbalanse, method="newton")')
        c.source = s
save(nb, path)


# -----------------------------------------------------------------------------
# NUMERISK DERIVASJON
# -----------------------------------------------------------------------------
path = FILES["derivasjon"]
nb = nbf.read(path, as_version=4)
feil_i = find_heading(nb, "## Feilanalyse")
data_i = find_heading(nb, "## Numerisk derivasjon av", start=feil_i)
rest_after_data = nb.cells[data_i:]
feil_block = nb.cells[feil_i:data_i]

intro = [
md(r'''# Numerisk derivasjon

```{admonition} Læringsutbytte
Etter å ha arbeidet med denne delen av emnet, skal du kunne:

1. forklare forskjellen på analytisk og numerisk derivasjon
2. implementere framover-, bakover- og sentraldifferansen
3. undersøke hvordan steglengde og avrundingsfeil påvirker resultatet
4. derivere eksperimentelle data og tolke hva den numeriske deriverte betyr kjemisk
```

## Derivasjonsbegrepet

Derivasjon handler om endring. Fra videregående kjenner du gjerne den deriverte som $f'(x)$. I naturvitenskap brukes også ofte Leibniz-notasjonen

$$\frac{df}{dx},$$

som betyr «endringen i $f$ med hensyn på $x$». De to notasjonene beskriver det samme når $f$ er en funksjon av $x$:

$$f'(x)=\frac{df}{dx}.$$

I kjemi er denne skrivemåten nyttig fordi variablene har en fysisk betydning. For eksempel beskriver

$$\frac{dc}{dt}$$

hvordan en konsentrasjon endrer seg med tid, mens

$$\frac{d\mathrm{pH}}{dV}$$

beskriver hvordan pH endrer seg når vi tilsetter volum i en titrering.

Den deriverte er definert som grenseverdien

$$f'(x)=\lim_{\Delta x\rightarrow0}\frac{f(x+\Delta x)-f(x)}{\Delta x}.$$

På datamaskinen kan vi ikke bruke et uendelig lite $\Delta x$. Vi erstatter derfor grenseverdien med en liten, endelig steglengde $h$:

$$f'(x)\approx\frac{f(x+h)-f(x)}{h}.$$

Dette kalles **framoverdifferansen**.
'''),
md(r'''```{admonition} Underveisoppgave
:class: tip
Beregn $f'(1)$ numerisk for $f(x)=2x+2$ med $h=10^{-8}$. Hva forventer du fra analytisk derivasjon?
```
'''),
code(r'''def f(x):
    return 2*x + 2

x = 1.0
h = 1E-8
fder = (f(x + h) - f(x))/h

print("Numerisk:", fder)
print("Analytisk:", 2.0)'''),
md(r'''Dette er den enkleste implementeringen: Vi beregner den deriverte i **ett bestemt punkt**. Numerisk derivasjon gir ikke automatisk en ny symbolsk funksjon slik som når vi deriverer for hånd. Den gir funksjonsverdier til den deriverte i de punktene vi velger.

Når prinsippet er tydelig, kan vi pakke det inn i en Python-funksjon:
'''),
code(r'''def deriver_framover(f, x, h=1E-8):
    dy = f(x + h) - f(x)
    return dy/h'''),
md(r'''Hvis vi ønsker å tegne den deriverte som en kurve, beregner vi ganske enkelt den deriverte i mange x-punkter.
'''),
]

andre = [
md(r'''## Andre tilnærminger

Framoverdifferansen bruker punktene $x$ og $x+h$. Men dette er ikke den eneste muligheten. Vi kan like gjerne bruke punktet **bak** $x$. Da får vi bakoverdifferansen:

$$\frac{df}{dx}\approx\frac{f(x)-f(x-h)}{h}.$$

Bakoverdifferansen er ikke introdusert fordi den nødvendigvis er bedre enn framoverdifferansen. Den viser først og fremst at den samme deriverte kan tilnærmes ved å velge datapunkter på ulike måter.

Når vi har én tilnærming som ser framover og én som ser bakover, oppstår en naturlig idé: Hvorfor ikke bruke informasjon fra **begge sider** av punktet? Det gir sentraldifferansen:

$$\frac{df}{dx}\approx\frac{f(x+h)-f(x-h)}{2h}.$$

Her ligger punktet $x$ midt mellom de to punktene som brukes til å beregne stigningen. Dette gir vanligvis en bedre tilnærming enn framover- og bakoverdifferansen for samme steglengde.

<img src="../bilder/numerisk_derivasjon.png" width="500"/>

Figuren viser den geometriske forskjellen mellom tilnærmingene.
'''),
code(r'''def deriver_bakover(f, x, h=1E-8):
    return (f(x) - f(x - h))/h

def deriver_sentral(f, x, h=1E-5):
    return (f(x + h) - f(x - h))/(2*h)

x = 1.0
print("Framover:", deriver_framover(np.sin, x, 1E-5))
print("Bakover:", deriver_bakover(np.sin, x, 1E-5))
print("Sentral:", deriver_sentral(np.sin, x, 1E-5))
print("Analytisk:", np.cos(x))'''),
md(r'''```{admonition} Underveisoppgave
:class: tip
Gjør en feilanalyse av de tre tilnærmingene for flere verdier av $h$. Bruk $f(x)=\sin x$ og sammenlikn med $f'(x)=\cos x$.
```
''')
]

nb.cells = intro + feil_block + andre + rest_after_data
save(nb, path)


# -----------------------------------------------------------------------------
# NUMERISK INTEGRASJON
# -----------------------------------------------------------------------------
path = FILES["integrasjon"]
nb = nbf.read(path, as_version=4)
konv_i = find_heading(nb, "## Konvergens")
trapes_i = find_heading(nb, "## Trapesmetoden", start=konv_i)
bib_i = find_heading(nb, "## Bruk av biblioteker", start=trapes_i)
konv_block = nb.cells[konv_i:trapes_i]
rest = nb.cells[bib_i:]

intro = [
md(r'''# Numerisk integrasjon

```{admonition} Læringsutbytte
Etter å ha arbeidet med dette temaet, skal du kunne:

1. forklare hvordan et bestemt integral kan tilnærmes som en sum av små arealer
2. forklare forskjellen på venstre-, høyre- og midtpunktstilnærming
3. forklare og implementere trapesmetoden
4. sammenlikne numeriske metoder ved hjelp av feil og konvergens
5. integrere funksjoner og eksperimentelle data med SciPy
6. tolke integraler i en kjemisk sammenheng
```

## Integrasjon

Du kjenner integrasjon både som en metode for å finne arealet under en graf og som den motsatte operasjonen av derivasjon. I dette kapitlet er vi først og fremst opptatt av **bestemte integraler**, altså integraler mellom to grenser $a$ og $b$.

En datamaskin arbeider med endelige tall og diskrete punkter. Vi skal derfor ikke be datamaskinen om å «finne en antiderivert» på samme måte som vi gjør symbolsk. I stedet tilnærmer vi arealet under grafen ved å dele det opp i mange små biter.

## Integraler i kjemi

Numerisk integrasjon dukker opp mange steder i kjemi, for eksempel når vi beregner

- arealet under en kromatografisk topp
- arealet under et NMR-signal
- samlet varme eller strøm over tid
- integraler som inngår i numeriske løsninger av differensiallikninger

Den store fordelen med numerisk integrasjon er at vi også kan integrere **måledata**, der vi ikke nødvendigvis har noen analytisk funksjon.

## Rektangelmetoden: fra integral til Riemann-sum

Det bestemte integralet kan forstås som grenseverdien av en **Riemann-sum**: Vi deler området under grafen i smale striper og tilnærmer hver stripe med en enkel geometrisk figur. Den enkleste figuren er et rektangel.

<img src="../bilder/rektangel10_utentall.png" width="500"/>

Her er intervallet delt i 10 rektangler. Hvis intervallet er $[a,b]$ og vi bruker $n$ rektangler, er bredden

$$h=\frac{b-a}{n}.$$

I figuren bestemmes høyden av funksjonsverdien ved **venstre kant** av hvert rektangel. Da får vi venstretilnærmingen.

Øker vi antall rektangler, følger rektanglene grafen bedre:

<img src="../bilder/rektangel_n=50.png" width="500"/>

Dette er den grunnleggende ideen bak numerisk integrasjon: flere og smalere geometriske figurer gir vanligvis en bedre tilnærming.

### Venstretilnærming

Vi begynner med koden uten å lage en funksjon. Da er det lettere å se algoritmen:
'''),
code(r'''import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.cos(x) + 2

a = 2
b = 12
n = 10

h = (b - a) / n
areal = 0.0
x = a

for k in range(n):
    areal = areal + f(x) * h
    x = x + h

print("Numerisk areal:", areal)'''),
md(r'''Løkken gjør nøyaktig det figuren viser: beregn arealet av ett rektangel, legg det til totalen, flytt $x$ én rektangelbredde og gjenta.

Når algoritmen er forståelig, pakker vi den inn i en funksjon:
'''),
code(r'''def rektangel_venstre(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal'''),
md(r'''### Hvor skal vi måle høyden?

Venstrekanten er bare ett mulig valg. For en voksende funksjon vil venstretilnærmingen systematisk ligge **under** grafen:

<img src="../bilder/rektangel_venstre_n=10.png" width="500"/>

Hvis vi i stedet måler høyden på **høyre kant**, får vi en tilsvarende overestimering:

<img src="../bilder/rektangel_høyre_n=10.png" width="500"/>

Dette er et viktig poeng: Det finnes flere måter å tilnærme det samme arealet på. Høyretilnærmingen krever bare én liten endring i algoritmen – vi starter på $a+h$ i stedet for $a$.
'''),
code(r'''def rektangel_hoyre(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a + h

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal'''),
md(r'''### Midtpunktstilnærming

Når venstre kant gir for lite areal og høyre kant gir for mye, er det naturlig å spørre om vi kan velge et punkt **mellom dem**. Vi bruker da funksjonsverdien i midten av hvert delintervall:

<img src="../bilder/rektangel_midt_n=10.png" width="500"/>

For en lineær funksjon blir feilarealet over og under grafen like stort, og midtpunktstilnærmingen blir eksakt. Også for mange krumme funksjoner er den betydelig bedre enn venstre- og høyretilnærmingen.
'''),
code(r'''def rektangel_midt(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a + h/2

    for k in range(n):
        areal = areal + f(x) * h
        x = x + h

    return areal

print("Venstre:", rektangel_venstre(f, 2, 12, 10))
print("Høyre:", rektangel_hoyre(f, 2, 12, 10))
print("Midtpunkt:", rektangel_midt(f, 2, 12, 10))'''),
]

methods = [
md(r'''## Trapesmetoden

Rektangelmetodene antar at toppen av hver lille figur er **horisontal**. Med andre ord erstatter vi funksjonen lokalt med en konstant verdi. Det fungerer, men hvis funksjonen endrer seg tydelig gjennom intervallet, kaster vi bort informasjon.

En naturlig forbedring er å trekke en **rett linje mellom de to endepunktene**. Da får vi et trapes i stedet for et rektangel:

<img src="../bilder/trapes_n=1.png" width="500"/>

For ett delintervall med bredde $h$ er de to parallelle sidene $f(x_i)$ og $f(x_{i+1})$. Arealet blir derfor

$$A_i=\frac{f(x_i)+f(x_{i+1})}{2}h.$$

For hele intervallet summerer vi ett slikt trapes for hvert delintervall. Vi kan skrive dette som

$$\int_a^b f(x)\,dx\approx h\left[\frac{f(a)+f(b)}{2}+\sum_{i=1}^{n-1}f(x_i)\right].$$

Først implementerer vi igjen algoritmen helt konkret:
'''),
code(r'''def f(x):
    return x**3

a = 0
b = 5
n = 100

h = (b - a) / n
areal = 0.0
x = a

for k in range(n):
    areal = areal + (f(x) + f(x + h))/2 * h
    x = x + h

print("Trapes:", areal)'''),
md(r'''Deretter kan vi pakke nøyaktig den samme løkken inn i en funksjon:
'''),
code(r'''def trapesmetoden(f, a, b, n):
    h = (b - a) / n
    areal = 0.0
    x = a

    for k in range(n):
        areal = areal + (f(x) + f(x + h))/2 * h
        x = x + h

    return areal

print("Trapes:", trapesmetoden(f, 0, 5, 100))
print("Eksakt:", 156.25)'''),
md(r'''Når antallet trapeser øker, følger de rette linjestykkene grafen stadig bedre:

<img src="../bilder/trapes10.png" width="500"/>

## Simpsons metode

Vi kan se rektangel- og trapesmetoden som en liten progresjon:

- rektangel: funksjonen tilnærmes lokalt med en **konstant**
- trapes: funksjonen tilnærmes lokalt med en **rett linje**

Neste steg er å bruke et krumt toppstykke. Simpsons metode bruker andregradspolynomer over par av delintervaller. Det gir ofte svært god nøyaktighet for glatte funksjoner.

For et partall $n$ kan metoden skrives

$$\int_a^b f(x)\,dx\approx\frac{h}{3}\left[f(a)+f(b)+4\sum_{\text{odde }k}f(x_k)+2\sum_{\text{partall }k}f(x_k)\right].$$

Koden er litt mindre intuitiv enn rektangel- og trapesmetoden. Derfor er målet først og fremst å kjenne igjen strukturen i formelen.
'''),
code(r'''def simpsons_metode(f, a, b, n):
    if n % 2 != 0:
        print("n må være et partall.")
        return None

    h = (b - a) / n
    areal = f(a) + f(b)
    x = a + h

    for k in range(1, n):
        if k % 2 == 0:
            areal = areal + 2*f(x)
        else:
            areal = areal + 4*f(x)
        x = x + h

    return areal * h/3

print("Simpson:", simpsons_metode(f, 0, 5, 100))'''),
md(r'''Rektangelmetodene, trapesmetoden og Simpsons metode tilhører samme familie av integrasjonsmetoder, **Newton–Cotes-metoder**. Vi trenger ikke lære hele familien; poenget er å se hvordan bedre tilnærminger kan bygges ved å bruke mer informasjon om formen på funksjonen.
''')
]

nb.cells = intro + konv_block + methods + rest
save(nb, path)


# -----------------------------------------------------------------------------
# DIFFERENSLIKNINGER
# -----------------------------------------------------------------------------
path = FILES["diskret"]
nb = nbf.read(path, as_version=4)
chem_i = find_heading(nb, "## Kjemisk eksempel")
rest = nb.cells[chem_i:]
intro = [
md(r'''# Differenslikninger

```{admonition} Læringsutbytte
Etter å ha arbeidet med denne delen av emnet, skal du kunne:

1. forklare forskjellen mellom diskrete og kontinuerlige modeller
2. formulere en enkel differenslikning som beskriver utviklingen fra ett steg til det neste
3. bruke løkker og arrayer til å simulere et dynamisk system iterativt
4. modellere nedbrytning, tilførsel og akkumulering av kjemiske stoffer
5. kontrollere en modell ved å undersøke enheter, grenser og langsiktig oppførsel
```

Mange prosesser kan beskrives ved å finne en regel som forteller hvordan systemet går fra ett steg til det neste. Det kan være mengden av et stoff fra én dag til den neste, en konsentrasjon etter hvert reaksjonstrinn eller en dose som tilføres med jevne mellomrom.

Når samme regel gjentas mange ganger, passer problemet naturlig til en løkke. Hver gjennomkjøring av løkka er en **iterasjon**, og vi kan derfor si at vi løser problemet iterativt.

En **diskret modell** beskriver systemet ved bestemte steg,

$$x_0,\;x_1,\;x_2,\ldots$$

mens en **kontinuerlig modell** beskriver tilstanden som en funksjon av en kontinuerlig variabel, for eksempel $c(t)$. Forskjellen handler om hvordan modellen er formulert – ikke om hvorvidt vi tilfeldigvis har målt systemet mellom punktene.

## Iterativ tenkning med en enkel følge

Vi starter med noe helt enkelt. I den aritmetiske følgen

$$1,4,7,10,13,\ldots$$

får vi neste ledd ved å legge til 3:

$$x_{n+1}=x_n+3.$$

Indeksen $n$ betyr bare «hvilket steg vi er på». Hvis vi starter med $x_0=1$, blir

$$x_1=x_0+3=4,$$

og deretter

$$x_2=x_1+3=7.$$

Det er akkurat denne prosessen en løkke kan gjenta.
'''),
code(r'''x = 1
n = 10

for k in range(1, n):
    x = x + 3

print("Det tiende leddet er", x)'''),
md(r'''Det matematiske problemet er enkelt, men arbeidsmåten er viktig: Vi trenger ikke nødvendigvis en ferdig formel for ledd nummer $n$. Hvis vi kjenner **oppdateringsregelen**, kan datamaskinen gjenta den så mange ganger vi ønsker.

```{admonition} Underveisoppgave
:class: tip
Finn det hundrede tallet i den geometriske følgen $1,2,4,8,16,\ldots$ ved hjelp av en løkke.
```

I kjemi blir denne tankemåten interessant når oppdateringsregelen representerer en fysisk prosess.
''')
]
nb.cells = intro + rest
save(nb, path)


# -----------------------------------------------------------------------------
# DIFFERENSIALLIKNINGER
# -----------------------------------------------------------------------------
path = FILES["ode"]
nb = nbf.read(path, as_version=4)
first_i = find_heading(nb, "## Førsteordens reaksjon med Euler")
coupled_i = find_heading(nb, "## Koblede differensiallikninger", start=first_i)
rest = nb.cells[coupled_i:]

intro = [
md(r'''# Differensiallikninger og fartslover

```{admonition} Læringsutbytte
Etter å ha arbeidet med dette temaet, skal du kunne:

1. forklare hvordan en differensiallikning beskriver endringen i et dynamisk system
2. utlede og implementere Forward Euler
3. modellere enkle og koblede kjemiske fartslover
4. undersøke hvordan tidssteg påvirker numerisk feil og stabilitet
5. bruke `solve_ivp` til å løse initialverdiproblemer
6. kontrollere en simulering med analytiske løsninger, stoffbalanse og kjemisk rimelighet
```

## Motivasjon

Eksperimenter står helt sentralt i kjemi, men simuleringer har blitt et viktig supplement. En simulering kan hjelpe oss å undersøke hvordan et kjemisk system utvikler seg når vi endrer en parameter, teste en modell mot eksperimentelle data eller studere systemer som er vanskelige å følge direkte.

Ofte kjenner vi ikke et ferdig uttrykk for utviklingen, men vi kjenner **endringen**. Et klassisk eksempel er en fartslov. For en førsteordens reaksjon

$$\mathrm{A\rightarrow produkter}$$

har vi

$$\frac{d[A]}{dt}=-k[A].$$

Likningen forteller hvordan konsentrasjonen endrer seg akkurat nå. Oppgaven vår er å bruke denne informasjonen til å finne hele utviklingen $[A](t)$.

## Hva er en differensiallikning?

En differensiallikning er en likning som inneholder en ukjent funksjon og én eller flere av de deriverte til funksjonen. Du kan møte mange skrivemåter:

$$y'=y$$

$$y'=t-y$$

$$u'(t)=u(t)$$

eller mer generelt

$$y'(t)=\frac{dy}{dt}=f(t,y).$$

Felles for dem er at venstresiden beskriver **endringen**, mens høyresiden forteller hva endringen avhenger av.

Når vi løser en vanlig algebraisk likning, leter vi etter et tall. Når vi løser en differensiallikning, leter vi etter en **funksjon** eller, numerisk, en rekke funksjonsverdier.

### Hvorfor trenger vi en startverdi?

Ta den svært enkle differensiallikningen

$$y'=1.$$

Hvis vi integrerer, får vi

$$y=t+C.$$

Det finnes altså uendelig mange løsninger – én for hver verdi av konstanten $C$. Hvis vi i tillegg vet at

$$y(0)=2,$$

blir $C=2$, og vi får én bestemt løsning. En slik opplysning kalles en **initialbetingelse**.

I kjemi kan initialbetingelsen for eksempel være startkonsentrasjonen $[A](0)$.

## Fra den deriverte til Eulers metode

Vi kjenner framoverdifferansen fra numerisk derivasjon:

$$\frac{dy}{dt}\approx\frac{y(t+\Delta t)-y(t)}{\Delta t}.$$

Nå bruker vi den på en litt annen måte. Vi kjenner $y(t)$ og uttrykket for den deriverte $dy/dt$, og ønsker å finne **neste verdi**, $y(t+\Delta t)$.

Vi ganger først med $\Delta t$:

$$\frac{dy}{dt}\Delta t\approx y(t+\Delta t)-y(t).$$

Så flytter vi $y(t)$ over på den andre siden:

$$y(t+\Delta t)\approx y(t)+\frac{dy}{dt}\Delta t.$$

Skriver vi differensiallikningen som $dy/dt=f(t,y)$ og bruker indekser, får vi

$$y_{n+1}=y_n+f(t_n,y_n)\Delta t.$$

Dette er **Forward Euler**. Legg merke til koblingen til forrige kapittel: Vi har gjort en kontinuerlig differensiallikning om til en **differenslikning** som datamaskinen kan gjenta steg for steg.
'''),
md(r'''## Førsteordens reaksjon med Euler

Vi bruker

$$\frac{d[A]}{dt}=-k[A].$$

Før vi lager en generell Euler-funksjon, skriver vi ut algoritmen direkte. Da blir sammenhengen mellom fartsloven og koden tydeligst.
'''),
code(r'''import numpy as np
import matplotlib.pyplot as plt

k = 0.030       # s^-1
A = 1.00        # mol/L
t = 0.0         # s
dt = 1.0        # s
t_slutt = 150.0

tid = [t]
konsentrasjon = [A]

while t < t_slutt:
    dA_dt = -k*A
    A = A + dA_dt*dt
    t = t + dt

    tid.append(t)
    konsentrasjon.append(A)

plt.plot(tid, konsentrasjon)
plt.xlabel("Tid (s)")
plt.ylabel("[A] (mol/L)")
plt.show()'''),
md(r'''Linjen

`A = A + dA_dt*dt`

**er Eulers metode**. Alt det andre i programmet setter startverdier, holder styr på tiden og lagrer resultatene slik at vi kan plotte dem.

Når vi har forstått denne løkken, kan vi pakke Euler-algoritmen inn i en funksjon. Da skiller vi selve løsningsmetoden fra den konkrete kjemiske modellen.
'''),
code(r'''def euler(f, y0, t0, t_slutt, dt):
    t = t0
    y = y0
    tid = [t]
    verdier = [y]

    while t < t_slutt:
        y = y + f(t, y)*dt
        t = t + dt

        tid.append(t)
        verdier.append(y)

    return np.array(tid), np.array(verdier)


def forste_orden(t, A):
    return -k*A

A0 = 1.00
tid, A_euler = euler(forste_orden, A0, 0, 150, 1.0)'''),
md(r'''Denne førsteordens reaksjonen har også en analytisk løsning,

$$[A](t)=[A]_0e^{-kt}.$$

Det gjør den spesielt nyttig når vi lærer en numerisk metode: Vi kan kontrollere resultatet mot en kjent løsning.
'''),
code(r'''A_analytisk = A0*np.exp(-k*tid)

plt.plot(tid, A_euler, label="Euler")
plt.plot(tid, A_analytisk, "--", label="Analytisk")
plt.xlabel("Tid (s)")
plt.ylabel("[A] (mol/L)")
plt.legend()
plt.show()

print("Største absolutte feil:", np.max(np.abs(A_euler - A_analytisk)))'''),
md(r'''## Hvor stort tidssteg bør vi bruke?

Euler antar at stigningen vi har **nå**, er en god tilnærming gjennom hele neste tidssteg. Hvis tidssteget er stort og systemet endrer seg raskt, blir denne antakelsen dårlig.

Vi undersøker derfor ikke bare én verdi av $\Delta t$. Et viktig numerisk kontrollspørsmål er:

> Endrer løsningen seg vesentlig hvis vi reduserer tidssteget?
'''),
code(r'''for dt_test in [10.0, 5.0, 1.0, 0.2]:
    t_test, A_test = euler(forste_orden, A0, 0, 150, dt_test)
    A_eksakt = A0*np.exp(-k*t_test[-1])
    feil = abs(A_test[-1] - A_eksakt)
    print(f"dt = {dt_test:4.1f} s   feil ved slutt = {feil:.3e}")'''),
]

nb.cells = intro + rest
save(nb, path)


# -----------------------------------------------------------------------------
# Felles kontroll
# -----------------------------------------------------------------------------
for path in FILES.values():
    nb = nbf.read(path, as_version=4)
    nbf.validate(nb)
    for c in nb.cells:
        if c.cell_type == "code" and "raise " in text(c):
            raise AssertionError(f"Fant raise i {path}: {text(c)[:100]}")

print("Pedagogisk tilbakeføring ferdig.")
