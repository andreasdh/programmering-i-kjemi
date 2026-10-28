# Oblig 1: Hvor godt virker et rensefilter?

Et laboratorium undersøker et filter som skal fjerne et fargestoff fra vann. Du skal bruke Python til å analysere måledata og svare på:

**Hvor stor reduksjon i fargestoffkonsentrasjon observerer vi etter filtrering, og hva gir dataene grunnlag for å konkludere?**

Du arbeider med en sammenhengende analyse fra rådata til konklusjon. Noen steder får du kode som du skal lese og utvide, andre steder må du velge framgangsmåte eller vurdere et løsningsforslag.

**Dataene er syntetiske og laget for denne oppgaven.** De representerer et forenklet forsøk, ikke et virkelig filterprodukt.

### Dette skal du øve på

- Lese, undersøke og filtrere kjemiske data uten å endre rådatafilene.
- Bruke løkker, lister og funksjoner til å behandle replikater.
- Beregne og tolke gjennomsnitt, standardavvik og kalibreringsmodeller.
- Velge en statistisk sammenlikning som passer til forsøksdesignet.
- Kontrollere kode og tolke resultatene kjemisk.
- Bruke KI som hjelp og undersøke om forslagene faktisk løser oppgaven.

### Arbeidsmåte og innlevering

Lag selv en Jupyter Notebook og lever en **helhetlig rapport** etter [de generelle kriteriene for obligene](https://andreasdh.github.io/programmering-i-kjemi/docs/obliger/obliger.html). Organiser den med disse fire hoveddelene:

| Rapportdel | Innhold i denne obligen |
|---|---|
| **Hensikt** | Undersøkelsen, hovedspørsmålet og hvordan programmering hjelper deg å besvare det. |
| **Teori** | Kort om absorbans og konsentrasjon, kalibreringens gyldighetsområde, gjennomsnitt og standardavvik og den statistiske sammenlikningen. |
| **Beskrivelse og resultater** | Data, kode, figurer, resultater og kontroller i logisk rekkefølge, med begrunnede valg. Inkluder en kort underdel om KI-sammenlikningen. |
| **Konklusjon** | Svar på hovedspørsmålet med tall og begrensninger, og kort om bruk i andre kjemiske analyser. |

Bruk del 1–5 som arbeidsrekkefølge og sjekkliste. Ikke kopier oppgaveteksten eller lag en seksjon per deloppgave: Svar på de faglige spørsmålene i sammenhengende tekst der de hører hjemme. Kode skal ha kommentarer, og tall og figurer skal forklares i teksten. Rapporten skal kunne kjøres ovenfra med de vedlagte datafilene.

Du kan bruke startkoden på denne siden, men må vise at du forstår den, og oppgi kilder til annen kode.

**Bruk av KI:** I del 1 og 2a–c gjør du et eget første forsøk uten KI og tar vare på det. I 2d bruker du KI på en avgrenset oppgave. Fra del 3 kan du bruke KI til forklaringer, feilsøking og kodeforslag, men du skal oppgi kort hvor den har bidratt og selv ha ansvaret for metodevalg og kontroller.

Du vurderes på analysen, forklaringene og kontrollene dine, ikke på lange KI-samtaler eller avansert kode. Hintene er valgfrie.

## Forsøket og dataene

Last ned [kalibrering.csv](data/kalibrering.csv) og [vannprover.csv](data/vannprover.csv), og legg dem i mappen `data` ved siden av rapportnotebooken.

Seks vannprøver, V01–V06, er preparert uavhengig med ulike fargestoffkonsentrasjoner. Hver prøve er blandet godt og delt i to like deler: en ufiltrert kontroll og en del behandlet med et nytt filter under samme betingelser som de andre filtrerte prøvene. Kontrollene er oppbevart like lenge som de filtrerte prøvene, og ingen prøver er fortynnet.

Absorbansen er målt tre ganger på **den samme løsningen i kyvetten** for hver prøvedel. Avlesningene beskriver instrumentets repeterbarhet og er ikke tre uavhengige filtreringsforsøk. V01 ufiltrert hører sammen med V01 filtrert, og tilsvarende for de andre prøve-ID-ene. Radene i filen er ikke sortert.

Alle målingene er gjort ved samme bølgelengde og med samme lysvei. Vi antar at andre stoffer og lysspredning ikke påvirker absorbansen vesentlig, og at kalibreringsstandardene har kjent konsentrasjon og samme løsningsbetingelser som prøvene.

| Fil | Innhold | Viktige kolonner |
|---|---|---|
| `data/kalibrering.csv` | Ni kalibreringsnivåer, inkludert nullstandard, med tre avlesninger per nivå | `maling_id`, `konsentrasjon_umol_L`, `replikat`, `absorbans` |
| `data/vannprover.csv` | Avlesninger fra filtrerte og ufiltrerte deler av V01–V06 | `prove_id`, `behandling`, `replikat`, `absorbans` |

Konsentrasjon er gitt i µmol/L, mens absorbans og replikatnummer er uten enhet. `replikat` identifiserer avlesningen, ikke et eget filtreringsforsøk. Nullstandarden inneholder ikke fargestoff.

### Sammenhengen vi ser etter

Når bølgelengde, lysvei og kjemiske betingelser holdes konstante, forventer vi en tilnærmet lineær sammenheng mellom absorbans og konsentrasjon innenfor et egnet konsentrasjonsområde:

$$
A=ac+b.
$$

Her er $A$ absorbans, $c$ konsentrasjon i µmol/L, $a$ stigningstall og $b$ konstantledd. Vi lar konstantleddet være fritt fordi nullstandarden kan ha et bakgrunnssignal. Med kalibreringsstandardene finner du $a$ og $b$, og med dem regner du om absorbansen i vannprøvene til konsentrasjon. Sammenhengen gjelder bare innenfor et begrenset område, og du skal selv vurdere hvor langt det rekker.

### Notater fra laboratoriet

I labjournalen står disse observasjonene, som du må ta hensyn til:

- **K30_2:** Kyvetten sto feil, og avlesningen ble ikke lagret. Feltet for absorbans er tomt.
- Instrumentansvarlig anbefaler foreløpig området **0–60 µmol/L** for lineær kalibrering. Standardene ved 70 og 80 µmol/L er med for å undersøke om området kan utvides.
- Absorbansen er eksportert uten blankkorreksjon. Bruk $A=ac+b$ med fritt konstantledd for både standarder og prøver, og ikke trekk i tillegg fra nullstandardens gjennomsnitt.
- Du har bare data for dette fargestoffet og disse forsøksbetingelsene, og har ikke målt nedbrytningsprodukter eller innholdet i filtermaterialet.

## Del 1: Hva har vi målt, og hva kan vi bruke?

### 1a. Lag en plan før du programmerer

Lag en arbeidsplan på 4–6 setninger eller en kort punktliste som beskriver veien fra absorbansmålinger til en vurdering av filteret. Planen er utgangspunkt for rapporten og trenger ikke leveres separat.

Diskuter også: Hvorfor gir tre målinger av den samme løsningen annen informasjon enn målinger fra flere uavhengige filtreringsforsøk, og hva kan vi undersøke med hver type gjentakelse?

Forutsi hvordan absorbansen endres hvis filteret reduserer fargestoffkonsentrasjonen. Hvilke forutsetninger bygger forventningen på?

### 1b. Les og undersøk dataene

Les begge datafilene og undersøk datatyper og manglende verdier. Hva representerer én rad i hver fil, og stemmer antall rader med forsøksbeskrivelsen?

### 1c. Håndter den manglende målingen

Lag arbeidskopiene `kalibrering` og `prover` av rådataene, og utelat den mislykkede målingen K30_2 fra `kalibrering`. Det er disse kopiene du bruker i resten av obligen. Vis hvor mange gyldige avlesninger som gjenstår ved 30 µmol/L.

En student foreslår å erstatte den manglende absorbansen med 0. Hva forventer du at dette gjør med gjennomsnittet ved 30 µmol/L? Beregn gjennomsnittet med begge framgangsmåter uten å endre rådata eller `kalibrering`. Hvilken behandling bruker du videre, og hvorfor?

```{admonition} Hint til datarydding
:class: tip dropdown

`df.copy()` lager en arbeidskopi. `df.isna().sum()` teller manglende verdier i hver kolonne. `df.dropna(subset=["kolonnenavn"])` utelater rader som mangler verdi i den angitte kolonnen.

```

## Del 2: Replikater, figurer og KI som kodehjelp

### 2a. Les koden før du kjører den

Koden nedenfor undersøker ett kalibreringsnivå. Forklar hva uttrykket inne i klammeparentesene gjør, hva `len(malinger)` teller, og hvilken enhet `gjennomsnitt` får. Kjør koden og kontroller resultatet mot radene i datafilen.

```python
kons = 20
utvalg = kalibrering[kalibrering["konsentrasjon_umol_L"] == kons]
malinger = utvalg["absorbans"]
gjennomsnitt = np.mean(malinger)

print("Konsentrasjon:", kons, "µmol/L")
print("Antall avlesninger:", len(malinger))
print("Gjennomsnittlig absorbans:", gjennomsnitt)
```

### 2b. Utvid til alle kalibreringsnivåene

Lag en løkke som går gjennom alle konsentrasjonene. Beregn antall gyldige avlesninger, gjennomsnitt og empirisk standardavvik ved hvert nivå, og lagre resultatene i lister.

### 2c. Vis målingene og variasjonen

Lag en figur som viser gjennomsnittlig absorbans ved hvert kalibreringsnivå, med feilstolper for ett empirisk standardavvik over og under gjennomsnittet. Bruk forståelige aksetitler, og forklar hva de ulike delene av figuren viser. Ligger punktene tilnærmet langs en rett linje, og hvor eventuelt ikke?

### 2d. Sammenlikn ditt arbeid med to KI-forslag

Bruk KI (GPT-UiO) på den samme oppgaven som i 2b–c, og sammenlikn med ditt eget første forsøk.

**Første forsøk:** Start en ny samtale, legg ved eller lim inn `kalibrering.csv`, og skriv bare:

> Oppsummer disse kalibreringsmålingene og lag en god figur i Python.

Les forslaget før du kjører det, og undersøk hva KI har valgt på egen hånd: håndtering av manglende verdier, gruppering, statistiske størrelser og figurtype. Fjern handlinger som endrer datafiler, og test forslaget med egne variabelnavn slik at din egen løsning bevares.

**Andre forsøk:** Skriv selv en mer presis forespørsel i en ny samtale med de samme dataene: Gi konteksten KI trenger, beskriv ønsket resultat og sett krav til kode og databehandling. Du skal ikke lime inn hele obligen.

Dokumenter minst disse kontrollene for din egen løsning og de to forslagene:

| Kontroll | Egen løsning | Første KI-forslag | Andre KI-forslag |
|---|---|---|---|
| Antall gyldige avlesninger ved 30 µmol/L | | | |
| Gjennomsnitt og standardavvik ved ett valgt nivå | | | |
| Hva feilstolpene faktisk representerer, eller om de mangler | | | |

Velg én kodelinje eller funksjon fra et KI-forslag som du måtte undersøke, og forklar med utgangspunkt i dataene hva den gjør. Hvis alt er kjent, velg en sentral linje og kontroller den med et lite eksempel.

Ta med tabellen, korte kodeutdrag, de to forespørslene og **maksimalt 150 ord** om hva du kunne oppdage fordi du hadde arbeidet med problemet selv, i en underdel om KI under «Beskrivelse og resultater». Hvilket valg kunne vært vanskelig å kontrollere uten denne forståelsen?

**Du skal ikke framprovosere eller finne en feil.** Hvis begge forslagene er gode, viser du hvordan du kontrollerte det. At to programmer gir samme resultat, kan skyldes at de gjør samme antakelse, og en presis forespørsel fritar deg ikke fra å kontrollere løsningen.

## Del 3: Fra absorbans til konsentrasjon

### 3a. Lag og vurder kalibreringsmodellen

Bruk sammenhengen $A=ac+b$ fra «Sammenhengen vi ser etter».

Lag utvalget `lineare_data` med målingene fra og med 0 til og med 60 µmol/L, og tilpass en rett linje til alle enkeltmålingene i utvalget. Lag en figur med gjennomsnittlig absorbans ved hvert kalibreringsnivå som punkter, sammen med den tilpassede linjen. Ta med gjennomsnittene ved 70 og 80 µmol/L, slik at du kan vurdere avvik fra modellen, og vis linjens fortsettelse fra 60 til 80 µmol/L som en stiplet linje merket «ekstrapolasjon».

Tilpass så en annen rett linje til alle enkeltmålinger fra 0 til 80 µmol/L, med egne variabelnavn, og vis den i samme figur. Bruk figuren og laboratorienotatet til å begrunne hvilken modell du bruker videre.

Forklar den kjemiske betydningen og enheten til $a$ og $b$. Hva er problemet med å velge en modell bare fordi programmet klarer å tilpasse en rett linje?

```{admonition} Hint til utvalg og hjelp dersom du står fast
:class: tip dropdown

Velg kalibreringsområdet i to trinn: Behold først radene med konsentrasjon større enn eller lik 0, og velg deretter radene med konsentrasjon mindre enn eller lik 60 fra dette utvalget. Tegn regresjonslinjen ved å beregne `a*x_linje + b` for selvvalgte x-verdier.

Hvis du ikke får til regresjonen, kan du midlertidig bruke `a = 0.0100` og `b = 0.0120`. Oppgi at du har gjort det, og gå tilbake til kalibreringen før innlevering. Dette er avrundede kontrollverdier, ikke en erstatning for del 3a.

```

### 3b. Forklar og utvid en funksjon

Funksjonen nedenfor beregner konsentrasjon fra absorbans. Utled uttrykket fra kalibreringslikningen, og forklar hva de tre argumentene representerer.

```python
def konsentrasjon_fra_absorbans(A, a, b):
    return (A - b) / a
```

Utvid funksjonen med parameterne `c_min` og `c_max`. Hvis beregnet konsentrasjon ligger utenfor kalibreringsområdet, skal den skrive en tydelig advarsel om at verdien er et ekstrapolert estimat som ikke skal brukes som validert måleresultat. Den skal likevel returnere den beregnede verdien, uten å endre den til null eller nærmeste grense.

Kontroller funksjonen først med et eksempel du kan regne uten Python: $a=0{,}020$, $b=0{,}100$ og $A=0{,}500$. Skriv forventet konsentrasjon før du kjører koden. Test deretter en absorbans som gir et estimat over 60 µmol/L med din faktiske modell. Hva ville du bedt laboratoriet gjøre med en slik prøve?

### 3c. Bruk funksjonen på vannprøvene

Bruk en løkke og funksjonen til å beregne én konsentrasjon for hver absorbans i `prover`. Lagre dem i en ny kolonne, `konsentrasjon_umol_L`, og behold absorbanskolonnen. Vis at prøvemålingene ligger innenfor området du bruker.

Velg én avlesning og sett konsentrasjonen tilbake i $A=ac+b$. Hva kan denne kontrollen avdekke, og hva kontrollerer den ikke?

## Del 4: Hvor stor effekt viser dataene?

### 4a. Sammenfatt hver prøvedel

For hver vannprøve (V01–V06) skal du beregne gjennomsnittlig konsentrasjon av de tre målingene av den ufiltrerte delen og av den filtrerte delen. Bruk en løkke og lagre dem i listene `ufiltrert_snitt` og `filtrert_snitt`, slik at verdier med samme indeks tilhører samme prøve. Skriv ut de to gjennomsnittene for hver prøve.

Kontroller V01 mot målingene som hører til prøven. Forklar hvordan du sikrer at riktige prøvedeler hører sammen, selv om radene i rådatafilen er usortert. Du trenger ikke standardavvik for hver prøvedel eller en ny DataFrame her.

```{admonition} Hint til utvalg og løkke
:class: tip dropdown

Bruk samme framgangsmåte som i del 2, men velg både behandling og prøve-ID: Velg først alle ufiltrerte målinger, og deretter én prøve fra dette utvalget. Gjør tilsvarende for filtrerte målinger.

Prøv først med V01. Når det fungerer, lar du en løkke gå gjennom prøve-ID-ene i samme rekkefølge for begge behandlingene. Bruk `.append()` til å legge hvert gjennomsnitt til riktig liste.

```

### 4b. Beskriv forskjellen med tall og figur

Beregn absolutt og prosentvis reduksjon for hvert prøvepar ut fra gjennomsnittene i 4a:

$$
\Delta c = c_{\text{ufiltrert}}-c_{\text{filtrert}},
\qquad
r = 100\frac{c_{\text{ufiltrert}}-c_{\text{filtrert}}}{c_{\text{ufiltrert}}}.
$$

Lagre de absolutte reduksjonene i listen `differanser`, og skriv ut begge størrelsene for hvert prøvepar. Oppgi også gjennomsnittlig absolutt reduksjon og det empiriske standardavviket mellom reduksjonene for de seks parene. Forklar hva dette standardavviket beskriver.

```{admonition} Hint til å sammenlikne listene
:class: tip dropdown

Verdier med samme indeks tilhører samme prøve. La en løkke gå gjennom indeksene, og hent én verdi fra hver liste i hver runde. Prosentvis reduksjon beregnes i forhold til den ufiltrerte prøvedelen.

```

Lag en figur som viser hvilke ufiltrerte og filtrerte resultater som hører sammen. Forklar hva figuren viser, og skriv en figurtekst. Husk aksetitler og merkelapper. Hvilken informasjon ville blitt skjult dersom du bare viste ett samlet gjennomsnitt før og ett etter filtrering?

```{admonition} Hint til figuren
:class: tip dropdown

Plasser «Ufiltrert» og «Filtrert» på x-aksen og konsentrasjon på y-aksen. Vis de to gjennomsnittene for hver prøve som punkter forbundet med en linje, og bruk prøve-ID som merkelapp, slik at det går fram hvilke punkter som hører sammen.

```

Les av hvilke prøver som har minst 20 % reduksjon. Du trenger ikke programmere en egen opptelling.

### 4c. Vurder et kodeforslag som kan kjøres

En kollega foreslår koden nedenfor. **Dette er et konstruert løsningsforslag for vurdering, ikke et faktisk svar fra en bestemt KI.**

Les koden før du eventuelt kjører den. Hvilke målinger havner i hver gruppe, hvor mange observasjoner behandler testen i hver gruppe, og passer forslaget til forsøksdesignet?

```python
# Vurder denne koden. Ikke bruk resultatet som din endelige analyse.
# Fjern kommentartegnene dersom du vil undersøke resultatet.

# utvalg_u = prover[prover["behandling"] == "ufiltrert"]
# utvalg_f = prover[prover["behandling"] == "filtrert"]
# ufiltrert_alle = utvalg_u["konsentrasjon_umol_L"]
# filtrert_alle = utvalg_f["konsentrasjon_umol_L"]
# test_forslag = stats.ttest_ind(ufiltrert_alle, filtrert_alle, equal_var=False)
# print(test_forslag.pvalue)
```

Lag deretter en egnet t-test med utgangspunkt i gjennomsnittslistene fra 4a eller `differanser` fra 4b. Forklar hvorfor testen passer, og formuler nullhypotesen. Bruk signifikansnivå 0,05. Du kan legge til grunn at forskjellene mellom uavhengige prøvepar er tilnærmet normalfordelte, og trenger ikke teste normaliteten.

Tolk p-verdien sammen med størrelsen på reduksjonen, og oppgi hvor mange uavhengige prøvepar analysen bygger på. Forklar hvorfor en liten p-verdi alene ikke viser at reduksjonen er stor, at filteret fungerer for alle prøver, eller at fargestoffet er brutt ned.

```{admonition} Hint til valg av test
:class: tip dropdown

`stats.ttest_1samp` sammenlikner én måleserie med en fast referanseverdi, `stats.ttest_ind` sammenlikner uavhengige grupper, og `stats.ttest_rel` sammenlikner observasjoner som hører sammen parvis. Velg ut fra hva som er målt. En ettutvalgs t-test av forskjellene mot null er også en mulig formulering.

```


## Del 5: Kontroll og kjemisk konklusjon

### 5a. Vis at du har kontroll over analysen

Dokumenter tre kontroller du har gjort, enten ved de aktuelle analysestegene eller i en kort underdel om kontroll:

1. Hvilke målinger som ble inkludert eller utelatt.
2. En beregning mot et enkelt eksempel eller rådata.
3. Modellens gyldighetsområde, eller at riktige prøver er paret.

Oppgi for hver kontroll hva du forventet, hva du observerte, og hvilken type feil den kan avdekke. Minst én kontroll skal være uavhengig av KI-forslaget du vurderer, for eksempel en enkel håndberegning. «Koden kjører» og «KI bekreftet at svaret er riktig» er ikke tilstrekkelige kontroller.

Start til slutt Python-kjernen på nytt og kjør den ferdige rapportnotebooken ovenfra med de vedlagte rådatafilene. Pass på at alternative løsninger ikke overskriver verdier den endelige analysen trenger, og fjern uferdige kladdeceller.

### 5b. Gi laboratoriet en kort konklusjon

Skriv konklusjonen på **150–250 ord** og besvar hovedspørsmålet. Bruk konkrete tall, beskriv variasjonen mellom prøvepar og angi hva den statistiske testen bidrar med.

Vurder også disse påstandene:

- «Filteret reduserte konsentrasjonen med minst 20 % i alle seks prøver.»
- «Siden absorbansen gikk ned, vet vi at fargestoffmolekylene ble brutt ned.»

Ta med minst én begrensning ved undersøkelsen, og foreslå én konkret tilleggsmåling eller endring av forsøket som ville styrket konklusjonen. Forklar også kort hvor du kan få bruk for en tilsvarende analyse. Utdypende drøfting kan stå under «Beskrivelse og resultater».

### Før innlevering
Sjekk følgende:
- Rapporten har hensikt, teori, beskrivelse og resultater, og konklusjon.
- Alle faglige spørsmål er behandlet, og forklaringene er knyttet til koden eller resultatene.
- Figurer og tabeller har forståelige navn og riktige enheter.
- Du skiller mellom spredningen i instrumentavlesninger og variasjonen mellom uavhengige prøvepar.
- Valg av databehandling, kalibreringsområde og statistisk test er begrunnet.
- KI-delen viser hva du spurte om, hva du undersøkte, og hva du fant.
- Du kan forklare kode og faglige konklusjoner med egne ord.

### Valgfri fordypning

Bruk begge kalibreringsmodellene fra 3a på prøvene. Hvordan påvirker modellvalget konsentrasjonene, den absolutte reduksjonen og den prosentvise reduksjonen? Endres p-verdien fra den parede testen? Forklar observasjonen med utgangspunkt i hva som skjer når samme lineære omregning brukes på alle målingene. Dette er ikke nødvendig for godkjenning.
