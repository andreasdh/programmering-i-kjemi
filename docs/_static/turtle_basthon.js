(() => {
  "use strict";

  const pagePath = window.location.pathname;
  if (!pagePath.endsWith("/docs/grunnleggende_programmering/lokker.html")) {
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
  ];

  function addEditor(example) {
    const codeCells = Array.from(document.querySelectorAll("div.cell"));
    const codeCell = codeCells.find((cell) => {
      const text = cell.textContent || "";
      return text.includes(example.marker) && text.includes(example.secondaryMarker);
    });

    if (!codeCell || codeCell.dataset.turtleBasthonAdded === "true") {
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "turtle-basthon-editor";
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
    codeCell.dataset.turtleBasthonAdded = "true";
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
