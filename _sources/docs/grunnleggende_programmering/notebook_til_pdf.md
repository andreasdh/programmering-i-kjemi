# Lag PDF av en notebook

Noen ganger trenger du en notebook som PDF, for eksempel for å levere den eller dele den med noen som ikke har Jupyter. Verktøyet Jupyter til PDF gjør dette i nettleseren. Du trenger ikke installere noe, og notebooken din blir ikke lastet opp noe sted.

<p><a href="../../_static/jupyter-til-pdf.html" target="_blank" rel="noopener"><strong>Åpne Jupyter til PDF</strong></a> (åpnes i en ny fane)</p>

## Slik gjør du det

1. Kjør alle cellene i notebooken (Restart & Run All) og lagre den.
2. Åpne verktøyet og velg .ipynb-filen, eller dra den inn i vinduet.
3. Se over sjekken. Den viser feil i LaTeX-formler, kodelinjer som er for lange, celler som ikke er kjørt og feilmeldinger i utdata. Klikk på et punkt for å se hvor i notebooken det gjelder.
4. Skriv gjerne inn tittel og navn, og velg om kode og utdata skal være med.
5. Trykk på «Last ned PDF».

Forhåndsvisningen viser hvor sidene deles. Teksten i PDF-en kan søkes i og kopieres.

```{note}
Interaktive figurer, for eksempel fra Plotly eller widgets, kan ikke vises i en PDF. Bruk heller matplotlib, eller lagre figuren som bilde og vis bildet.
```
