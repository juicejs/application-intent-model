(function initSiteChrome() {
  const body = document.body;
  const base = body.getAttribute("data-base") || "./";
  const page = body.getAttribute("data-page") || "";

  const host = document.createElement("div");
  host.className = "site-shell";
  host.innerHTML = `
    <header class="site-header">
      <a class="site-brand" href="${base}">
        <svg class="site-logo" width="30" height="30" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 28 L16 4 L27 28" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="10" y1="18" x2="22" y2="18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="16" cy="4" r="3" fill="currentColor"/>
        </svg>
        <span>Application Intent Model</span>
        <span class="site-version">v2.2</span>
      </a>
      <nav class="site-nav" aria-label="Primary">
        <a data-nav="home" href="${base}">Home</a>
        <a data-nav="spec" href="${base}spec/">Specification</a>
        <a data-nav="registry" href="${base}registry/">Registry</a>
        <a data-nav="publish" href="${base}registry/publish.html">Publish</a>
      </nav>
    </header>
    <main class="content" id="content-root"></main>
  `;

  while (body.firstChild) {
    host.querySelector("#content-root").appendChild(body.firstChild);
  }
  body.appendChild(host);

  const active = host.querySelector(`[data-nav="${page}"]`);
  if (active) {
    active.classList.add("active");
  }
})();

/**
 * Generic copy functionality for prompts
 * @param {string} textToCopy - The literal string to copy
 * @param {HTMLElement} button - The button element that was clicked
 */
function copyPrompt(textToCopy, button) {
  if (!textToCopy) return;

  navigator.clipboard.writeText(textToCopy).then(() => {
    const originalHTML = button.innerHTML;
    button.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      <span>Copied!</span>
    `;
    button.classList.add('copied');

    setTimeout(() => {
      button.innerHTML = originalHTML;
      button.classList.remove('copied');
    }, 2000);
  }).catch(err => {
    console.error('Failed to copy:', err);
  });
}
