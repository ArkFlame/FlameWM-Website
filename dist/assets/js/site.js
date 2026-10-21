(() => {
  document.documentElement.classList.add('js');
  const header = document.querySelector('[data-header]');
  const button = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-mobile-menu]');
  const setOpen = (open) => {
    if (!button || !menu) return;
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    menu.hidden = !open;
    document.body.classList.toggle('nav-open', open);
  };
  button?.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  menu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setOpen(false); });
  document.addEventListener('click', (event) => {
    if (!menu?.hidden && !header?.contains(event.target)) setOpen(false);
  });
  window.addEventListener('resize', () => { if (innerWidth > 800) setOpen(false); }, { passive: true });
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
  const revealNodes = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries, obs) => {
      for (const entry of entries) if (entry.isIntersecting) { entry.target.classList.add('in-view'); obs.unobserve(entry.target); }
    }, { rootMargin: '0px 0px -4% 0px', threshold: 0.06 });
    revealNodes.forEach((node) => observer.observe(node));
  } else revealNodes.forEach((node) => node.classList.add('in-view'));
})();
