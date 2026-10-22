(() => {
  "use strict";

  const pageName = window.DOCUMENTATION_OPTIONS?.pagename || "";
  const onLoopsPage =
    pageName === "docs/grunnleggende_programmering/lokker" ||
    window.location.pathname.endsWith("/docs/grunnleggende_programmering/lokker.html");

  if (!onLoopsPage) {
    return;
  }

  const examples = [
    {
      marker: 'shape("turtle")',
      secondaryMarker: 'forward(80)',
      file: "loops_turtle_intro.py",
      title: "Interactive Python editor for introductory turtle graphics",
      lead: "Du kan kjøre og endre turtle-programmet i editoren nedenfor.",
      height: 620,
    },
    {
      marker: "antall_sider = 6",
      secondaryMarker: "dreievinkel = 360 / antall_sider",
      file: "loops_turtle_benzene.py",
      title: "Interactive Python editor for drawing a simplified benzene ring",
      lead: "Prøv benzeneksemplet i editoren nedenfor. Endre for eksempel antall sider, sidelengden eller dreievinkelen.",
      height: 680,
    },
    {
      marker: "antall_steg = 200",
      secondaryMarker: "setheading(retning)",
      file: "loops_turtle_random_walk.py",
      title: "Interactive Python editor for a turtle random walk",
      lead: "Kjør den tilfeldige vandringen flere ganger og undersøk hvordan banen endrer seg.",
      height: 720,
    },
    {
      marker: "for måling in range(5)",
      secondaryMarker: "Gjennomfører måling nummer",
      file: "loops_for_measurements.py",
      title: "Interactive Python editor for a basic for loop",
      lead: "Prøv den enkle for-løkka i editoren nedenfor. Endre antall målinger og undersøk hvilke verdier løkkevariabelen får.",
      height: 560,
    },
    {
      marker: "for _ in range(5)",
      secondaryMarker: "Etter fem halveringstider",
      file: "loops_half_life.py",
      title: "Interactive Python editor for repeated half-lives",
      lead: "Kjør halveringstidseksemplet og modifiser det slik at mengden skrives ut etter hver løkkerunde.",
      height: 600,
    },
    {
      marker: "tid_slutt = 10",
      secondaryMarker: "endring = k * A * dt",
      file: "loops_kinetic_model.py",
      title: "Interactive Python editor for a simple kinetic model",
      lead: "Utforsk den kinetiske modellen i editoren nedenfor. Sammenlikn særlig resultatene for ulike tidssteg.",
      height: 720,
    },
    {
      marker: "for antall_halveringstider in range(11)",
      secondaryMarker: "mengde = mengde / 2",
      file: "loops_radioactive_sequence.py",
      title: "Interactive Python editor for a recursive sequence",
      lead: "Kjør og endre tallfølgeprogrammet i editoren nedenfor.",
      height: 620,
    },
    {
      marker: "antall_ledd = 100",
      secondaryMarker: "ledd = (2 / 3)**n",
      file: "loops_geometric_series.py",
      title: "Interactive Python editor for a geometric series",
      lead: "Undersøk hvordan antall ledd påvirker tilnærmingen til rekkesummen.",
      height: 650,
    },
  ];

  function addEditor(example) {
    const codeCells = Array.from(document.querySelectorAll("div.cell"));
    const codeCell = codeCells.find((cell) => {
      const text = cell.textContent || "";
      return text.includes(example.marker) && text.includes(example.secondaryMarker);
    });

    if (!codeCell || codeCell.dataset.loopsBasthonAdded === "true") {
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "loops-basthon-editor";
    wrapper.style.margin = "1.25rem 0 1.75rem";

    const lead = document.createElement("p");
    lead.textContent = example.lead;

    const iframe = document.createElement("iframe");
    iframe.src = `../../basthon/?from=examples/${example.file}`;
    iframe.width = "100%";
    iframe.height = String(example.height);
    iframe.frameBorder = "0";
    iframe.title = example.title;
    iframe.loading = "lazy";
    iframe.allowFullscreen = true;

    wrapper.append(lead, iframe);
    codeCell.insertAdjacentElement("afterend", wrapper);
    codeCell.dataset.loopsBasthonAdded = "true";
  }

  function initialize() {
    examples.forEach(addEditor);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
