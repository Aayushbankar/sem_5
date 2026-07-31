/* Semester 5 — study progress: reading bar + persisted task checklists */
(function () {
  "use strict";

  /* ---------- dark-first theme (default = slate) ---------- */
  (function () {
    var DEFAULT_PALETTE = {
      index: 0,
      color: {
        media: "(prefers-color-scheme: dark)",
        scheme: "slate",
        primary: "custom",
        accent: "custom",
      },
    };
    var stored = null;
    var wanted = DEFAULT_PALETTE;
    try {
      stored = localStorage.getItem("__palette");
      if (stored) wanted = JSON.parse(stored);
    } catch (e) {}
    try {
      if (!stored) localStorage.setItem("__palette", JSON.stringify(DEFAULT_PALETTE));
    } catch (e) {}

    function apply() {
      if (document.body && wanted && wanted.color) {
        document.body.setAttribute("data-md-color-scheme", wanted.color.scheme);
      }
    }
    apply();
    document.addEventListener("DOMContentLoaded", apply);
    window.addEventListener("load", apply);
  })();

  /* ---------- reading progress bar ---------- */
  var bar = document.createElement("div");
  bar.id = "reading-progress";
  document.documentElement.appendChild(bar);

  function tick() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    bar.style.width = pct + "%";
  }
  window.addEventListener("scroll", tick, { passive: true });
  window.addEventListener("resize", tick, { passive: true });
  tick();

  /* ---------- task list persistence ---------- */
  var PREFIX = "sem5:prog";

  function key(group) {
    return PREFIX + ":" + location.pathname + ":" + group;
  }

  function load(group) {
    try {
      return JSON.parse(localStorage.getItem(key(group)) || "[]");
    } catch (e) {
      return [];
    }
  }

  function save(group, state) {
    try {
      localStorage.setItem(key(group), JSON.stringify(state));
    } catch (e) {
      /* private mode etc. — ignore */
    }
  }

  function bindList(ul, group) {
    var inputs = Array.prototype.slice.call(ul.querySelectorAll("input[type='checkbox']"));
    if (!inputs.length) return;

    /* pymdownx renders the real checkbox off-box; toggle it when the
       visible indicator is clicked */
    inputs.forEach(function (input) {
      var label = input.closest("label");
      if (label) {
        label.addEventListener("click", function (e) {
          input.checked = !input.checked;
          input.dispatchEvent(new Event("change", { bubbles: true }));
          e.preventDefault();
        });
      }
    });

    /* restore */
    var state = load(group);
    inputs.forEach(function (input, i) {
      input.checked = state.indexOf(i) !== -1;
    });

    function refresh() {
      var done = inputs.filter(function (i) { return i.checked; }).length;
      var total = inputs.length;

      /* chip inside the card header */
      var card = ul.closest(".check-card");
      if (card) {
        var h3 = card.querySelector("h3");
        var chip = card.querySelector(".check-chip");
        if (h3 && !chip) {
          chip = document.createElement("span");
          chip.className = "check-chip";
          h3.appendChild(chip);
        }
        if (chip) chip.textContent = done + "/" + total + " done";
      }

      /* global label + bar bound to the same group */
      var labels = document.querySelectorAll('[data-progress-for="' + group + '"]');
      labels.forEach(function (el) {
        if (el.classList.contains("progress-label")) {
          el.textContent = done + "/" + total + (done === total ? " — all done 🎉" : done ? " done" : " to go");
        }
        if (el.classList.contains("progress-bar")) {
          var i = el.querySelector("i");
          if (i) i.style.width = (total ? (done / total) * 100 : 0) + "%";
        }
      });
    }

    inputs.forEach(function (input) {
      input.addEventListener("change", function () {
        var s = [];
        inputs.forEach(function (i, idx) { if (i.checked) s.push(idx); });
        save(group, s);
        refresh();
      });
    });

    refresh();
  }

  function init() {
    /* reset buttons */
    document.querySelectorAll(".progress-reset").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var group = btn.getAttribute("data-progress-for");
        if (!group) return;
        try { localStorage.removeItem(key(group)); } catch (e) {}
        var uls = document.querySelectorAll('ul.task-list[data-progress="' + group + '"]');
        uls.forEach(function (ul) { bindList(ul, group); });
      });
    });

    document.querySelectorAll("ul.task-list[data-progress]").forEach(function (ul) {
      bindList(ul, ul.getAttribute("data-progress"));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
