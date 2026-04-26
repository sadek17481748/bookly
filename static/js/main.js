// ---------------------------------------------------------------------------
// Small scripts for base.html (loaded with defer)
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Mobile nav: toggles .open on #navLinks and updates aria-expanded
// ---------------------------------------------------------------------------
function setupNavToggle() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.getElementById("navLinks");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

// ---------------------------------------------------------------------------
// Buttons/links with data-confirm: browser confirm() before default action
// ---------------------------------------------------------------------------
function setupConfirmButtons() {
  document.addEventListener("click", (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;

    const confirmText = target.getAttribute("data-confirm");
    if (!confirmText) return;

    const ok = window.confirm(confirmText);
    if (!ok) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
}

setupNavToggle();
setupConfirmButtons();
