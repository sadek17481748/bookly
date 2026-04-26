function setupNavToggle() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.getElementById("navLinks");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

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

