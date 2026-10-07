# Oblig 1: Hvor godt virker et rensefilter?

Et laboratorium undersøker et filter som skal fjerne et fargestoff fra vann. Du skal bruke Python til å analysere måledata og svare på:

**Hvor stor reduksjon i fargestoffkonsentrasjon observerer vi etter filtrering, og hva gir dataene grunnlag for å konkludere?**

Du skal arbeide med en sammenhengende analyse fra rådata til konklusjon. Noen steder får du kode som du skal lese og utvide. Andre steder må du velge framgangsmåte eller vurdere et løsningsforslag.

**Dataene er syntetiske og laget for denne oppgaven.** De representerer et forenklet forsøk, ikke dokumentasjon av et virkelig filterprodukt.

### Dette skal du øve på

- Lese, undersøke og filtrere kjemiske data uten å endre rådatafilene.
- Bruke løkker, lister og funksjoner til å behandle replikater.
- Beregne og tolke gjennomsnitt, standardavvik og kalibreringsmodeller.
- Velge en statistisk sammenlikning som passer til forsøksdesignet.
- Kontrollere kode og tolke resultatene kjemisk.
- Bruke KI som hjelp og undersøke om forslagene faktisk løser oppgaven.

### Arbeidsmåte og innlevering

Lag selv en Jupyter Notebook og lever en **helhetlig rapport** etter [de generelle kriteriene for obligene](https://andreasdh.github.io/programmering-i-kjemi/docs/obliger/obliger.html). Nettsiden her gir oppgaver, kodeeksempler og hint som støtter arbeidet ditt. Organiser rapporten med disse fire hoveddelene:

| Rapportdel | Innhold i denne obligen |
|---|---|
| **Hensikt** | Presenter undersøkelsen, hovedspørsmålet og hvordan programmering skal hjelpe deg å besvare det. |
| **Teori** | Forklar den relevante sammenhengen mellom absorbans og konsentrasjon, kalibreringens gyldighetsområde, gjennomsnitt og standardavvik, og prinsippet bak den statistiske sammenlikningen du bruker.|
| **Beskrivelse og resultater** | Beskriv dataene og behandlingen av dem. Presenter og forklar kode, figurer, resultater og kontroller i en logisk rekkefølge. Begrunn metodevalg og diskuter resultatene underveis. Ta med en kort underdel om KI-sammenlikningen. |
| **Konklusjon** | Besvar hovedspørsmålet med konkrete resultater og relevante begrensninger. Forklar kort hva framgangsmåten er nyttig til, og i hvilke andre kjemiske analyser den kan brukes. |

Bruk del 1–5 nedenfor som arbeidsrekkefølge og sjekkliste. Alle faglige spørsmål skal besvares i rapporten, men forklaringene skal inngå i sammenhengende tekst på relevante steder. Du skal ikke kopiere oppgaveteksten eller lage en egen seksjon for hvert deloppgavenummer. Unngå å gjenta samme forklaring flere steder. Teoridelen skal være kort og knyttet til det du faktisk bruker i analysen.

Kode skal ha hensiktsmessige kommentarer, og tall og figurer skal forklares i teksten. Den ferdige rapporten skal kunne kjøres ovenfra med de vedlagte datafilene. Du kan arbeide i en egen kladdenotebook underveis og velge ut det som trengs i rapporten.

**Startkoden på denne siden er gitt for at du skal kunne bruke og utvide den.** Du kan kopiere disse utdragene til ditt eget arbeid. Vis gjennom endringer, kommentarer og faglige forklaringer at du forstår dem. Oppgi kilder til annen kode og dokumenter relevante KI-bidrag.

I del 1 og del 2a–c skal du gjøre et eget første forsøk uten å bruke KI. Ta vare på dette forsøket, også om det er ufullstendig. I del 2d skal du bruke KI på en avgrenset oppgave. Fra del 3 kan du bruke KI til forklaringer, feilsøking og kodeforslag etter at du har skissert hva du trenger. Oppgi kort hvor KI har bidratt.

Du vurderes på analysen, forklaringene og kontrollene dine. Lange KI-samtaler og avansert kode er ikke et mål. Hvis KI foreslår noe du ikke forstår, undersøk det eller erstatt det med en enklere framgangsmåte.

Hintene er valgfrie. Bruk dem når du står fast.

## Forsøket og dataene

Last ned [kalibrering.csv](data/kalibrering.csv) og [vannprover.csv](data/vannprover.csv). Legg begge filene i en mappe som heter `data`, ved siden av rapportnotebooken din.

Seks vannprøver, V01–V06, er preparert uavhengig med ulike fargestoffkonsentrasjoner. Hver prøve er blandet godt og delt i to like deler. Den ene delen er ufiltrert kontroll. Den andre er behandlet med et nytt filter under samme betingelser som de øvrige filtrerte prøvene. Kontrollene er oppbevart like lenge som de filtrerte prøvene. Ingen prøver er fortynnet.

Absorbansen er målt med et spektrofotometer tre ganger på **den samme løsningen i kyvetten** for hver prøvedel. Disse avlesningene beskriver instrumentets repeterbarhet. De er ikke tre uavhengige filtreringsforsøk. V01 ufiltrert hører sammen med V01 filtrert, og tilsvarende for de andre prøve-ID-ene. Radene i filen er ikke sortert.

Alle målingene er gjort ved samme bølgelengde og med samme lysvei. I denne forenklede analysen antar vi at andre stoffer og lysspredning ikke påvirker absorbansen vesentlig. Kalibreringsstandardene har kjent konsentrasjon og samme løsningsbetingelser som prøvene.

| Fil | Innhold | Viktige kolonner |
|---|---|---|
| `data/kalibrering.csv` | Ni kalibreringsnivåer, inkludert nullstandard, med tre avlesninger per nivå | `maling_id`, `konsentrasjon_umol_L`, `replikat`, `absorbans` |
| `data/vannprover.csv` | Avlesninger fra filtrerte og ufiltrerte deler av V01–V06 | `prove_id`, `behandling`, `replikat`, `absorbans` |

Konsentrasjon er gitt i µmol/L. Absorbans og replikatnummer er uten enhet. `replikat` identifiserer avlesningen, ikke et eget filtreringsforsøk. Nullstandarden inneholder ikke fargestoff.

### Notater fra laboratoriet
I labjournalen fra eksperimentet finner vi følgende observasjoner som du må ta hensyn til under analysen:

- **K30_2:** Kyvetten sto feil. Avlesningen ble ikke lagret. Feltet for absorbans er derfor tomt.
- Instrumentansvarlig har foreløpig anbefalt området **0–60 µmol/L** for en lineær kalibrering. Standardene ved 70 og 80 µmol/L er tatt med for å undersøke om området kan utvides.
- Absorbansen er eksportert uten etterfølgende blankkorreksjon. Bruk en modell med fritt konstantledd, $A=ac+b$, og behandle standarder og prøver på samme måte. Du skal ikke i tillegg trekke fra nullstandardens gjennomsnitt i denne oppgaven.
- Dere har bare data for dette fargestoffet og disse forsøksbetingelsene. Dere har ikke målt stoffets nedbrytningsprodukter eller innholdet i filtermaterialet.

## Del 1: Hva har vi målt, og hva kan vi bruke?

### 1a. Lag en plan før du programmerer

Lag først en arbeidsplan på 4–6 setninger eller en kort punktliste som beskriver veien fra absorbansmålinger til en vurdering av filteret. Bruk planen som utgangspunkt for rapporten; den trenger ikke leveres som en egen besvarelse. Diskuter også følgende: Hvorfor gir tre målinger av den samme løsningen annen informasjon enn målinger fra flere uavhengige filtreringsforsøk? Hva kan vi undersøke med hver av disse typene gjentakelser?

Forutsi hvordan absorbansen vil endre seg dersom filteret reduserer fargestoffkonsentrasjonen. Hvilke forutsetninger bygger forventningen din på?

### 1b. Les og undersøk dataene

Lag en kode som leser av begge datafiler. Utvid den slik at du også undersøker datatyper og manglende verdier i begge filer. Forklar hva én rad representerer i hver fil. Stemmer antall rader med forsøksbeskrivelsen?

### 1c. Håndter den manglende målingen

Lag arbeidskopiene `kalibrering` og `prover` av rådataene. Utelat den dokumenterte mislykkede målingen fra analyser som krever absorbans. Vis hvor mange gyldige avlesninger som gjenstår ved 30 µmol/L.

En student foreslår å erstatte den manglende absorbansen med 0. Forklar først hva du forventer at dette vil gjøre med gjennomsnittet ved 30 µmol/L. Beregn deretter gjennomsnittet med de to framgangsmåtene, uten å endre rådata. Hvilken behandling vil du bruke videre, og hvorfor?

```{admonition} Hint til datarydding
:class: tip dropdown

`df.copy()` lager en arbeidskopi. `mangler = df.isna()` markerer manglende verdier. Deretter teller `mangler.sum()` hvor mange som mangler i hver kolonne. `df.dropna(subset=["kolonnenavn"])` utelater rader som mangler verdi i den angitte kolonnen.

```

## Del 2: Replikater, figurer og KI som kodehjelp

### 2a. Les koden før du kjører den

Koden nedenfor undersøker ett kalibreringsnivå. Forklar hva uttrykket inne i klammeparentesene gjør, og hva `len(malinger)` teller. Hvilken enhet får `gjennomsnitt`?

Kjør deretter koden og kontroller resultatet mot radene i datafilen.

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

Lag en løkke som går gjennom alle konsentrasjonene. Beregn antall gyldige avlesninger, gjennomsnitt og empirisk standardavvik ved hvert nivå. Lagre resultatene i lister.

### 2c. Vis målingene og variasjonen

Lag en egnet figur som viser gjennomsnittlig absorbans ved hvert kalibreringsnivå. Legg til feilstolper som viser ett empirisk standardavvik over og under gjennomsnittet. Figuren skal ha forståelige aksetitler.

Forklar hva de ulike delene i figuren viser.

### 2d. Sammenlikn ditt arbeid med to KI-forslag

Ta vare på ditt eget første forsøk fra 2b–c. Du skal nå bruke KI til den samme avgrensede oppgaven. Bruk GPT-UiO.

**Første forsøk:** Start en ny samtale, legg ved eller lim inn innholdet i `kalibrering.csv`, og skriv bare:

> Oppsummer disse kalibreringsmålingene og lag en god figur i Python.

Les forslaget før du kjører det. Undersøk hva KI har valgt på egen hånd: håndtering av manglende verdier, gruppering av data, statistiske størrelser og figurtype. Hvis forslaget endrer datafiler, fjern den handlingen før du tester det. Prøv det i kladdenotebooken eller i egne celler med egne variabelnavn, slik at din første løsning bevares. Velg senere ut de relevante utdragene til rapporten.

**Andre forsøk:** Skriv selv en mer presis forespørsel. Gi konteksten KI trenger, beskriv ønsket resultat og sett relevante krav til kode og databehandling. Start gjerne en ny samtale med de samme dataene. Hvis du ikke kan legge ved filer, lim inn CSV-teksten. Du skal ikke lime inn hele obligen.

Sammenlikn din egen løsning med de to forslagene fra KI. Dokumenter minst disse kontrollene:

| Kontroll | Egen løsning | Første KI-forslag | Andre KI-forslag |
|---|---|---|---|
| Antall gyldige avlesninger ved 30 µmol/L | | | |
| Gjennomsnitt og standardavvik ved ett valgt nivå | | | |
| Hva feilstolpene faktisk representerer, eller om de mangler | | | |

Velg også én kodelinje eller funksjon fra et KI-forslag som du måtte undersøke. Forklar med utgangspunkt i dataene hva den gjør. Hvis alt er kjent, velg en sentral linje og kontroller den med et lite eksempel.

Ta med sammenlikningstabellen, korte relevante kodeutdrag og **maksimalt 150 ord** om hva du kunne oppdage fordi du hadde arbeidet med problemet selv, i en underdel om KI under «Beskrivelse og resultater». Legg de to forespørslene i samme underdel eller i et kort vedlegg i rapportnotebooken. Hele samtaler og fullstendige alternative programmer trenger ikke leveres. Hvilket valg kunne vært vanskelig å kontrollere uten denne forståelsen?

**Du skal ikke framprovosere eller finne en feil.** Hvis begge forslagene er gode, viser du hvordan du kontrollerte det. At to programmer gir samme resultat, er nyttig informasjon, men kan fortsatt skyldes at de gjør samme antakelse. En presis forespørsel fritar deg heller ikke fra å kontrollere løsningen.

Fra neste del kan du bruke KI etter behov. Noter kort relevante bidrag, og behold ansvar for metodevalg og kontroller.

## Del 3: Fra absorbans til konsentrasjon

### 3a. Lag og vurder kalibreringsmodellen

Når lysvei og kjemiske betingelser holdes konstante, forventer vi en tilnærmet lineær sammenheng innenfor et egnet konsentrasjonsområde:

$$
A=ac+b.
$$

Her er $A$ absorbans, $c$ konsentrasjon i µmol/L, $a$ stigningstall og $b$ konstantledd. Vi lar konstantleddet være fritt fordi nullstandarden kan ha et bakgrunnssignal.

Lag utvalget `lineare_data` med målingene fra og med 0 til og med 60 µmol/L. Tilpass en rett linje til alle gyldige enkeltmålinger i dette utvalget. Lag en figur som viser gjennomsnittlig absorbans ved hvert kalibreringsnivå som punkter, sammen med den tilpassede linjen. Ta med gjennomsnittene ved 70 og 80 µmol/L, slik at du kan vurdere avvik fra modellen. Vis linjens fortsettelse fra 60 til 80 µmol/L som en stiplet linje merket «ekstrapolasjon».

Tilpass så en annen rett linje til alle gyldige enkeltmålinger fra 0 til 80 µmol/L, med egne variabelnavn, og vis den i samme figur. Bruk figurene og laboratorienotatet til å begrunne hvilken modell du vil bruke videre.

Forklar den kjemiske betydningen av $a$ og $b$, og angi enhetene. Hva er problemet med å velge en modell bare fordi programmet klarer å tilpasse en rett linje?


```{admonition} Hint til utvalg og hjelp dersom du står fast
:class: tip dropdown

Du kan velge kalibreringsområdet i to trinn: Behold først radene med konsentrasjon større enn eller lik 0, og velg deretter radene med konsentrasjon mindre enn eller lik 60 fra dette utvalget. Regresjonslinjen tegnes ved å beregne `a*x_linje + b` for selvvalgte x-verdier.

Hvis du ikke får til regresjonen, kan du midlertidig bruke `a = 0.0100` og `b = 0.0120` for å arbeide videre. Oppgi at du har brukt disse hjelpeverdiene, og gå tilbake til kalibreringen før innlevering. De er avrundede kontrollverdier, ikke en erstatning for del 3a.

```

### 3b. Forklar og utvid en funksjon

Funksjonen nedenfor beregner konsentrasjon fra absorbans. Utled uttrykket fra kalibreringslikningen, og forklar hvilke størrelser de tre argumentene representerer.

```python
def konsentrasjon_fra_absorbans(A, a, b):
    return (A - b) / a
```

Utvid funksjonen med parameterne `c_min` og `c_max`. Funksjonen skal skrive en tydelig advarsel hvis beregnet konsentrasjon ligger utenfor kalibreringsområdet. La den returnere den beregnede verdien, men opplys i advarselen at dette er et ekstrapolert estimat som ikke skal brukes som et validert måleresultat. Den skal ikke endre en verdi til null eller til nærmeste grense.

Kontroller først funksjonen med et lite eksempel som du kan regne uten Python: $a=0{,}020$, $b=0{,}100$ og $A=0{,}500$. Skriv forventet konsentrasjon før du kjører koden. Test deretter en absorbans som gir et estimat over 60 µmol/L med din faktiske modell. Hva ville du bedt laboratoriet gjøre med en slik prøve?

### 3c. Bruk funksjonen på vannprøvene

Bruk en løkke og funksjonen til å beregne én konsentrasjon for hver absorbans i `prover`. Lag en ny kolonne, `konsentrasjon_umol_L`, og behold absorbanskolonnen. Vis at prøvemålingene ligger innenfor området du bruker.

Velg én avlesning og kontroller konsentrasjonen ved å sette den tilbake i $A=ac+b$. Forklar hva denne kontrollen kan avdekke, og hva den ikke kontrollerer.


## Del 4: Hvor stor effekt viser dataene?

### 4a. Sammenfatt hver prøvedel

For hver vannprøve (V01–V06) skal du beregne to gjennomsnittlige konsentrasjoner:
- Gjennomsnittet av de tre målingene av den ufiltrerte delen.
- Gjennomsnittet av de tre målingene av den filtrerte delen.

Lag en løkke som beregner gjennomsnittene for alle seks vannprøvene. Lagre dem i listene `ufiltrert_snitt` og `filtrert_snitt`, slik at verdier med samme indeks tilhører samme prøve.

Skriv ut de to gjennomsnittene for hver prøve. Kontroller resultatene for V01 mot målingene som hører til denne prøven. Forklar hvordan du sikrer at riktige prøvedeler hører sammen, selv om radene i rådatafilen er usortert.

Du trenger ikke beregne standardavvik for hver prøvedel eller lage en ny DataFrame i denne delen.

```{admonition} Hint til utvalg og løkke
:class: tip dropdown

Bruk samme framgangsmåte som da du valgte ett kalibreringsnivå i del 2. Her må du velge både behandling og prøve-ID. Det kan gjøres i to trinn: Velg først alle ufiltrerte målinger, og velg deretter én prøve fra dette utvalget. Gjør tilsvarende for filtrerte målinger.

Prøv først med V01. Når det fungerer, lar du en løkke gå gjennom prøve-ID-ene i samme rekkefølge for begge behandlingene. Bruk `.append()` til å legge hvert gjennomsnitt til riktig liste.

```

### 4b. Beskriv forskjellen med tall og figur

Beregn absolutt reduksjon og prosentvis reduksjon for hvert prøvepar:

$$
\Delta c = c_{\text{ufiltrert}}-c_{\text{filtrert}},
\qquad
r = 100\frac{c_{\text{ufiltrert}}-c_{\text{filtrert}}}{c_{\text{ufiltrert}}}.
$$

Bruk gjennomsnittene fra 4a. Lagre de absolutte reduksjonene i en liste som heter `differanser`. Skriv ut absolutt og prosentvis reduksjon for hvert prøvepar.

Oppgi også gjennomsnittlig absolutt reduksjon for de seks prøveparene og det empiriske standardavviket mellom disse reduksjonene. Forklar hva dette standardavviket beskriver.

```{admonition} Hint til å sammenlikne listene
:class: tip dropdown

Verdier med samme indeks tilhører samme prøve. La en løkke gå gjennom indeksene, og hent én verdi fra hver liste i hver runde. Beregn forskjellen og legg den til i `differanser`. Prosentvis reduksjon beregnes i forhold til den ufiltrerte prøvedelen.

```

Lag en figur som viser hvilke ufiltrerte og filtrerte resultater som hører sammen. Forklar hva figuren viser, og skriv en figurtekst. Husk aksetitler og relevante merkelapper. Hvilken informasjon ville blitt skjult dersom du bare viste ett samlet gjennomsnitt før og ett etter filtrering?

```{admonition} Hint til figuren
:class: tip dropdown

Du kan plassere «Ufiltrert» og «Filtrert» på x-aksen og konsentrasjon på y-aksen. Vis de to gjennomsnittene for én prøve som punkter forbundet med en linje. Gjenta for de andre prøvene i samme figur. Bruk prøve-ID som merkelapp, slik at det går fram hvilke punkter som hører sammen.

```

Les av hvilke prøver som har minst 20 % reduksjon. Du trenger ikke programmere en egen opptelling.

### 4c. Vurder et kodeforslag som kan kjøres

En kollega foreslår koden nedenfor. **Dette er et konstruert løsningsforslag for vurdering, ikke et faktisk svar fra en bestemt KI.**

Les koden før du eventuelt kjører den. Forklar hvilke målinger som havner i hver gruppe, hvor mange observasjoner testen vil behandle i hver gruppe, og vurder om forslaget passer til forsøksdesignet.

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

Lag deretter en egnet t-test med utgangspunkt i gjennomsnittslistene fra 4a eller listen `differanser` fra 4b. Forklar hvorfor testen passer, og formuler nullhypotesen. Bruk signifikansnivå 0,05. I denne oppgaven legger vi til grunn at forskjellene mellom uavhengige prøvepar kan beskrives med en tilnærmet normalfordeling. Du trenger ikke gjennomføre en egen normalitetstest.

Tolk p-verdien sammen med størrelsen på reduksjonen. Oppgi hvor mange uavhengige prøvepar analysen bygger på. Forklar hvorfor en liten p-verdi alene ikke viser at reduksjonen er stor, at filteret fungerer for alle prøver, eller at fargestoffet er brutt ned.

```{admonition} Hint til valg av test
:class: tip dropdown

`stats.ttest_1samp` sammenlikner én måleserie med en fast referanseverdi. `stats.ttest_ind` sammenlikner uavhengige grupper. `stats.ttest_rel` sammenlikner observasjoner som hører sammen parvis. Velg ut fra hva som er målt. En ettutvalgs t-test av forskjellene mot null er også en mulig formulering.

```


## Del 5: Kontroll og kjemisk konklusjon

### 5a. Vis at du har kontroll over analysen

Dokumenter tre kontroller du allerede har gjort. Plasser dem ved de aktuelle analysestegene under «Beskrivelse og resultater», eller samle dem i en kort underdel om kontroll:

1. En kontroll av hvilke målinger som ble inkludert eller utelatt.
2. En kontroll av en beregning mot et enkelt eksempel eller rådata.
3. En kontroll av modellens gyldighetsområde eller av at riktige prøver er paret.

Oppgi for hver kontroll hva du forventet, hva du observerte, og hvilken type feil kontrollen kan avdekke. Minst én kontroll skal være uavhengig av KI-forslaget du vurderer, for eksempel en enkel håndberegning. «Koden kjører» og «KI bekreftet at svaret er riktig» er ikke tilstrekkelige kontroller.

Start til slutt Python-kjernen på nytt og kjør den ferdige rapportnotebooken ovenfra. Pass på at den bruker de vedlagte rådatafilene, og at eksperimentering med alternative løsninger ikke overskriver verdier som den endelige analysen trenger. Fjern uferdige kladdeceller fra rapporten. 

### 5b. Gi laboratoriet en kort konklusjon

Skriv rapportens konklusjon på **150–250 ord** og besvar hovedspørsmålet. Bruk konkrete tall, beskriv variasjonen mellom prøvepar og angi hva den statistiske testen bidrar med.

Vurder også disse påstandene:

- «Filteret reduserte konsentrasjonen med minst 20 % i alle seks prøver.»
- «Siden absorbansen gikk ned, vet vi at fargestoffmolekylene ble brutt ned.»

Ta med minst én begrensning ved undersøkelsen og foreslå én konkret tilleggsmåling eller endring av forsøket som ville styrket konklusjonen. Forklar også kort hvor du kan få bruk for en tilsvarende analyse. Utdypende drøfting kan stå under «Beskrivelse og resultater» og oppsummeres kort i konklusjonen.

### Før innlevering
Sjekk følgende:
- Rapporten har hensikt, teori, beskrivelse og resultater, og konklusjon i tråd med emnets rapportmal.
- Alle faglige spørsmål er behandlet, og forklaringene er knyttet til den aktuelle koden eller de aktuelle resultatene.
- Figurer og tabeller har forståelige navn og riktige enheter.
- Du skiller mellom spredningen i instrumentavlesninger og variasjonen mellom uavhengige prøvepar.
- Valg av databehandling, kalibreringsområde og statistisk test er begrunnet.
- KI-delen viser hva du spurte om, hva du undersøkte, og hva du fant.
- Kode og faglige konklusjoner kan forklares med egne ord.

### Valgfri fordypning

Bruk begge kalibreringsmodellene fra 3a på prøvene. Undersøk hvordan modellvalget påvirker konsentrasjonene, absolutt reduksjon og prosentvis reduksjon. Endres p-verdien fra den parede testen? Forklar observasjonen med utgangspunkt i hva som skjer når samme lineære omregning brukes på alle målingene. Dette er ikke nødvendig for godkjenning.
