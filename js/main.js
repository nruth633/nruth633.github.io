/* Nicolas Ruth, portfolio
   Project filtering and the footer year. No dependencies. */

(function () {
  "use strict";

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

  /* ---------- Footer year ---------- */

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
