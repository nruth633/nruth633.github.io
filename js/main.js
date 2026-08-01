/* Nicolas Ruth — portfolio
   Theme toggle, project filtering, scroll reveal. No dependencies. */

(function () {
  "use strict";

  /* ---------- Theme toggle ----------
     The initial theme is applied by an inline script in <head> so the page
     never flashes the wrong colours. This only wires up the button. */

  var root = document.documentElement;
  var toggle = document.querySelector(".theme-toggle");

  function currentTheme() {
    var explicit = root.getAttribute("data-theme");
    if (explicit) return explicit;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (toggle) {
      toggle.setAttribute("aria-pressed", String(theme === "dark"));
      toggle.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
    }
  }

  if (toggle) {
    applyTheme(currentTheme());

    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        /* private browsing — the toggle still works for this page load */
      }
    });
  }

  /* ---------- Project filtering ---------- */

  var filterBar = document.querySelector(".filter-bar");

  if (filterBar) {
    var cards = Array.prototype.slice.call(
      document.querySelectorAll("[data-tags]")
    );
    var buttons = Array.prototype.slice.call(
      filterBar.querySelectorAll(".filter-btn")
    );
    var status = document.getElementById("filter-status");

    filterBar.addEventListener("click", function (event) {
      var btn = event.target.closest(".filter-btn");
      if (!btn) return;

      var filter = btn.dataset.filter;
      var shown = 0;

      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });

      cards.forEach(function (card) {
        var tags = card.dataset.tags.split(/\s+/);
        var match = filter === "all" || tags.indexOf(filter) !== -1;
        card.hidden = !match;
        if (match) shown++;
      });

      if (status) {
        status.textContent =
          filter === "all"
            ? "Showing all " + shown + " projects."
            : "Showing " + shown + " project" + (shown === 1 ? "" : "s") +
              " tagged " + filter + ".";
      }
    });
  }

  /* ---------- Reveal on scroll ---------- */

  var revealTargets = document.querySelectorAll(".reveal");

  var prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (!("IntersectionObserver" in window) || prefersReducedMotion) {
    // No observer support, or the user asked for no motion — just show everything.
    Array.prototype.forEach.call(revealTargets, function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    Array.prototype.forEach.call(revealTargets, function (el) {
      observer.observe(el);
    });
  }

  /* ---------- Footer year ---------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
