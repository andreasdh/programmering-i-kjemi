/* ==========================================================================
   kjemiquiz.js — enkel quizmotor for Jupyter Book / vanlige nettsider
   Bruk:  <div class="kq" data-quiz="../../_static/quizzes/quiz5.json"></div>
   eller: <div class="kq" data-quiz="#quiz5-data"></div>  (inline JSON i sida)
   Språk: <div class="kq" data-quiz="..." data-lang="en"></div>   (no | en)

   Datamodellen er kompatibel med jupyterquiz, så eksisterende JSON-filer
   kan brukes uendret. Typer: multiple_choice, many_choice, numeric.
   ========================================================================== */
(function () {
  "use strict";

  /* --- tekster ------------------------------------------------------------ */

  var T = {
    no: {
      progress: function (a, b) { return a + " av " + b + " løst"; },
      qLabel: "Spørsmål",
      check: "Sjekk svaret",
      numPlaceholder: "Tallsvar",
      numAria: "Tallsvar",
      needNumber: "Skriv inn et tall.",
      right: "Riktig.",
      rightAgain: "Riktig — nå sitter det.",
      rightAll: "Riktig — alle de rette, og ingen av de gale.",
      notQuite: "Ikke helt.",
      tryOther: "Prøv et annet alternativ.",
      tryAgain: "Prøv igjen.",
      adjust: "Juster og sjekk igjen.",
      notRight: "Ikke riktig.",
      missing: function (n) { return n + (n === 1 ? " riktig mangler" : " riktige mangler"); },
      extra: function (n) { return n + (n === 1 ? " avkryssing er feil" : " avkryssinger er feil"); },
      partly: "Ikke helt: ",
      perfect: "Alle riktige på første forsøk.",
      summary: "Tallet teller bare svar som var riktige på første forsøk — resten fikk du til etter et forsøk eller to.",
      retake: "Ta quizen på nytt",
      noAttr: "Mangler data-quiz-attributt.",
      noData: function (s) { return "Fant ikke quizdata: " + s; },
      badJson: function (s, e) { return "Ugyldig JSON i " + s + ": " + e; },
      loadFail: function (s, e) { return "Klarte ikke å laste " + s + " (" + e + ")."; }
    },
    en: {
      progress: function (a, b) { return a + " of " + b + " answered"; },
      qLabel: "Question",
      check: "Check answer",
      numPlaceholder: "Numeric answer",
      numAria: "Numeric answer",
      needNumber: "Enter a number.",
      right: "Correct.",
      rightAgain: "Correct — got there.",
      rightAll: "Correct — all the right ones, none of the wrong ones.",
      notQuite: "Not quite.",
      tryOther: "Try another option.",
      tryAgain: "Try again.",
      adjust: "Adjust and check again.",
      notRight: "Not correct.",
      missing: function (n) { return n + (n === 1 ? " correct option missing" : " correct options missing"); },
      extra: function (n) { return n + (n === 1 ? " selection is wrong" : " selections are wrong"); },
      partly: "Not quite: ",
      perfect: "All correct on the first try.",
      summary: "The score counts only answers that were correct on the first try — the rest you got after an attempt or two.",
      retake: "Take the quiz again",
      noAttr: "Missing data-quiz attribute.",
      noData: function (s) { return "Quiz data not found: " + s; },
      badJson: function (s, e) { return "Invalid JSON in " + s + ": " + e; },
      loadFail: function (s, e) { return "Could not load " + s + " (" + e + ")."; }
    }
  };

  /* --- hjelpefunksjoner --------------------------------------------------- */

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Enkel formatering i spørsmål og svar: `kode`, **fet**, *kursiv*
  function fmt(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>");
  }

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function shuffled(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  var LETTERS = "ABCDEFGHIJ";

  /* --- én quiz ------------------------------------------------------------ */

  function Quiz(root, spec) {
    this.root = root;
    this.questions = Array.isArray(spec) ? spec : (spec.questions || []);
    this.shuffleAnswers =
      root.dataset.shuffle === "false" ? false
        : (Array.isArray(spec) ? true : spec.shuffle_answers !== false);
    this.t = T[root.dataset.lang || (Array.isArray(spec) ? null : spec.lang) || "no"] || T.no;
    this.correct = 0;   // riktige på første forsøk
    this.settled = 0;   // spørsmål som er løst
    this.total = this.questions.length;
  }

  Quiz.prototype.render = function () {
    var self = this;
    this.root.innerHTML = "";
    this.root.classList.add("kq");

    var bar = el("div", "kq-bar");
    var track = el("div", "kq-track");
    this.fill = el("div", "kq-fill");
    track.appendChild(this.fill);
    this.count = el("span", "kq-count", this.t.progress(0, this.total));
    bar.appendChild(track);
    bar.appendChild(this.count);
    this.root.appendChild(bar);

    this.questions.forEach(function (q, i) {
      self.root.appendChild(self.renderQuestion(q, i));
    });

    this.done = el("div", "kq-done");
    this.done.hidden = true;
    this.done.setAttribute("aria-live", "polite");
    this.root.appendChild(this.done);
  };

  Quiz.prototype.renderQuestion = function (q, i) {
    var card = el("div", "kq-q");
    card.dataset.state = "open";
    card.appendChild(el("div", "kq-num", this.t.qLabel + " " + (i + 1)));
    card.appendChild(el("div", "kq-text", fmt(q.question)));

    if (q.code) {
      var pre = el("pre");
      pre.appendChild(el("code", null, esc(
        Array.isArray(q.code) ? q.code.join("\n") : q.code
      )));
      card.appendChild(pre);
    }

    var fb = el("div", "kq-fb");
    fb.hidden = true;
    fb.setAttribute("aria-live", "polite");

    var type = q.type || "multiple_choice";
    if (type === "numeric") {
      card.appendChild(this.numericBody(q, card, fb));
    } else if (type === "many_choice") {
      card.appendChild(this.manyBody(q, card, fb));
    } else {
      card.appendChild(this.singleBody(q, card, fb));
    }

    card.appendChild(fb);
    return card;
  };

  /* --- ett riktig svar: klikk gir svar med én gang, feil kan prøves på nytt */

  Quiz.prototype.singleBody = function (q, card, fb) {
    var self = this;
    var wrap = el("div", "kq-opts");
    var answers = this.shuffleAnswers ? shuffled(q.answers) : q.answers;
    var firstTry = true;

    answers.forEach(function (a, idx) {
      var btn = el("button", "kq-opt");
      btn.type = "button";
      btn.dataset.pick = "single";
      btn.appendChild(el("span", "kq-mark", LETTERS[idx] || "•"));
      btn.appendChild(el("span", "kq-label", fmt(a.answer)));

      btn.addEventListener("click", function () {
        if (a.correct) {
          btn.dataset.mark = "ok";
          card.dataset.state = "ok";
          wrap.querySelectorAll(".kq-opt").forEach(function (b) { b.disabled = true; });
          self.settle(firstTry);
          self.say(fb, "ok", fmt(a.feedback || (firstTry ? self.t.right : self.t.rightAgain)));
        } else {
          firstTry = false;
          btn.dataset.mark = "no";
          btn.disabled = true;
          card.dataset.state = "try";
          self.say(fb, "no", fmt(a.feedback || self.t.notQuite) +
            " <strong>" + self.t.tryOther + "</strong>");
        }
      });

      wrap.appendChild(btn);
    });

    return wrap;
  };

  /* --- flere riktige svar: hak av, så sjekk ------------------------------- */

  Quiz.prototype.manyBody = function (q, card, fb) {
    var self = this;
    var box = el("div");
    var wrap = el("div", "kq-opts");
    var answers = this.shuffleAnswers ? shuffled(q.answers) : q.answers;
    var picked = {};
    var firstTry = true;

    answers.forEach(function (a, idx) {
      var btn = el("button", "kq-opt");
      btn.type = "button";
      btn.dataset.pick = "multi";
      btn.setAttribute("aria-pressed", "false");
      btn.appendChild(el("span", "kq-mark", ""));
      btn.appendChild(el("span", "kq-label", fmt(a.answer)));

      btn.addEventListener("click", function () {
        picked[idx] = !picked[idx];
        btn.dataset.mark = picked[idx] ? "on" : "";
        btn.querySelector(".kq-mark").textContent = picked[idx] ? "✓" : "";
        btn.setAttribute("aria-pressed", picked[idx] ? "true" : "false");
      });

      wrap.appendChild(btn);
    });

    var check = el("button", "kq-btn", this.t.check);
    check.type = "button";
    check.style.marginTop = ".7rem";

    check.addEventListener("click", function () {
      var right = answers.every(function (a, idx) {
        return !!a.correct === !!picked[idx];
      });
      if (right) {
        answers.forEach(function (a, idx) {
          if (a.correct) wrap.children[idx].dataset.mark = "ok";
        });
        wrap.querySelectorAll(".kq-opt").forEach(function (b) { b.disabled = true; });
        check.remove();
        card.dataset.state = "ok";
        self.settle(firstTry);
        self.say(fb, "ok", self.t.rightAll);
      } else {
        firstTry = false;
        card.dataset.state = "try";
        var missing = 0, extra = 0;
        answers.forEach(function (a, idx) {
          if (a.correct && !picked[idx]) missing++;
          if (!a.correct && picked[idx]) extra++;
        });
        var hint = [];
        if (missing) hint.push(self.t.missing(missing));
        if (extra) hint.push(self.t.extra(extra));
        self.say(fb, "no", self.t.partly + hint.join(", ") +
          ". <strong>" + self.t.adjust + "</strong>");
      }
    });

    box.appendChild(wrap);
    box.appendChild(check);
    return box;
  };

  /* --- numerisk svar ------------------------------------------------------ */

  Quiz.prototype.numericBody = function (q, card, fb) {
    var self = this;
    var row = el("div", "kq-num-row");
    var input = el("input", "kq-input");
    input.type = "text";
    input.inputMode = "decimal";
    input.placeholder = q.placeholder || this.t.numPlaceholder;
    input.setAttribute("aria-label", this.t.numAria);

    var check = el("button", "kq-btn", this.t.check);
    check.type = "button";
    var firstTry = true;

    function evaluate() {
      var raw = input.value.trim().replace(",", ".");
      if (raw === "" || isNaN(Number(raw))) {
        self.say(fb, "no", self.t.needNumber);
        return;
      }
      var v = Number(raw);
      var p = typeof q.precision === "number" ? q.precision : 3;
      var tol = Math.pow(10, -p) / 2;
      var hit = null, fallback = null;

      (q.answers || []).forEach(function (a) {
        if (a.type === "default") { fallback = a; return; }
        if (hit) return;
        if (a.type === "range" && Array.isArray(a.range)) {
          if (v >= a.range[0] && v <= a.range[1]) hit = a;
        } else if (a.value != null) {
          if (Math.abs(v - Number(a.value)) < tol) hit = a;
        }
      });

      if (hit && hit.correct) {
        card.dataset.state = "ok";
        input.disabled = true;
        check.remove();
        self.settle(firstTry);
        self.say(fb, "ok", fmt(hit.feedback || self.t.right));
      } else {
        firstTry = false;
        card.dataset.state = "try";
        var msg = (hit && hit.feedback) || (fallback && fallback.feedback) || self.t.notRight;
        self.say(fb, "no", fmt(msg) + " <strong>" + self.t.tryAgain + "</strong>");
      }
    }

    check.addEventListener("click", evaluate);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); evaluate(); }
    });

    row.appendChild(input);
    row.appendChild(check);
    return row;
  };

  /* --- felles ------------------------------------------------------------- */

  Quiz.prototype.say = function (node, tone, html) {
    node.dataset.tone = tone;
    node.innerHTML = html;
    node.hidden = false;
  };

  Quiz.prototype.settle = function (firstTry) {
    this.settled += 1;
    if (firstTry) this.correct += 1;
    this.fill.style.width = (100 * this.settled / this.total) + "%";
    this.count.textContent = this.t.progress(this.settled, this.total);
    if (this.settled === this.total) this.finish();
  };

  Quiz.prototype.finish = function () {
    var self = this;
    this.done.innerHTML = "";
    this.done.appendChild(el("div", "kq-score", this.correct + " / " + this.total));
    this.done.appendChild(el("p", null,
      this.correct === this.total ? this.t.perfect : this.t.summary));
    var again = el("button", "kq-btn", this.t.retake);
    again.type = "button";
    again.dataset.variant = "quiet";
    again.addEventListener("click", function () {
      self.correct = 0; self.settled = 0;
      self.render();
      self.root.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    this.done.appendChild(again);
    this.done.hidden = false;
  };

  /* --- oppstart ----------------------------------------------------------- */

  function fail(node, msg) {
    node.innerHTML = "";
    node.classList.add("kq");
    node.appendChild(el("div", "kq-error", esc(msg)));
  }

  function boot(node) {
    if (node.dataset.kqReady) return;   // hindrer dobbel rendering
    node.dataset.kqReady = "1";

    var t = T[node.dataset.lang || "no"] || T.no;
    var src = node.dataset.quiz;
    if (!src) return fail(node, t.noAttr);

    if (src.charAt(0) === "#") {        // inline JSON i sida
      var tag = document.querySelector(src);
      if (!tag) return fail(node, t.noData(src));
      try {
        new Quiz(node, JSON.parse(tag.textContent)).render();
      } catch (e) {
        fail(node, t.badJson(src, e.message));
      }
      return;
    }

    fetch(src)                          // ekstern JSON-fil
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (spec) { new Quiz(node, spec).render(); })
      .catch(function (e) { fail(node, t.loadFail(src, e.message)); });
  }

  function bootAll() {
    document.querySelectorAll("[data-quiz]").forEach(boot);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootAll);
  } else {
    bootAll();
  }

  window.KjemiQuiz = { boot: boot, bootAll: bootAll };
})();
