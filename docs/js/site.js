/* ==========================================================
   Dra. Dalila Peñaranda — sitio informativo
   Configuración e interacciones (sin dependencias)
   ========================================================== */

/* -------- CONFIGURACIÓN: edita aquí los datos reales -------- */
const CONFIG = {
  whatsapp: '+57 304 653 2006',            // número visible y del enlace wa.me
  mensajeWhatsApp: 'Hola doctora, quiero agendar una cita',
  correo: 'hola@dradalilapenaranda.com',
  direccion: 'Calle 1C # 30-40, High Park Medical Center',
  direccion2: 'Consultorio 129 · Barranquilla, Colombia',
  precioPresencial: '$180.000',            // pendiente de confirmar con la doctora
  precioVirtual: '45 USD',                 // pendiente de confirmar con la doctora
  mostrarPrecios: true,                    // false oculta la sección "Tu cita"
  mostrarPepe: true,                       // false oculta el bloque de Pepe
  redes: { instagram: '#', facebook: '#', tiktok: '#' }  // pendientes
};

(function () {
  document.documentElement.classList.remove('no-js');

  /* -------- datos de contacto en la página -------- */
  const digits = CONFIG.whatsapp.replace(/\D/g, '');
  const waLink = 'https://wa.me/' + digits + '?text=' + encodeURIComponent(CONFIG.mensajeWhatsApp);
  document.querySelectorAll('[data-wa]').forEach(a => { a.href = waLink; a.target = '_blank'; a.rel = 'noopener'; });
  document.querySelectorAll('[data-tel]').forEach(el => { el.textContent = CONFIG.whatsapp; });
  document.querySelectorAll('[data-correo]').forEach(el => { el.textContent = CONFIG.correo; if (el.tagName === 'A') el.href = 'mailto:' + CONFIG.correo; });
  document.querySelectorAll('[data-direccion]').forEach(el => { el.innerHTML = CONFIG.direccion + '<br>' + CONFIG.direccion2; });
  document.querySelectorAll('[data-precio="presencial"]').forEach(el => { el.textContent = CONFIG.precioPresencial; });
  document.querySelectorAll('[data-precio="virtual"]').forEach(el => { el.textContent = CONFIG.precioVirtual; });
  document.querySelectorAll('[data-red]').forEach(a => { a.href = CONFIG.redes[a.dataset.red] || '#'; });
  if (!CONFIG.mostrarPrecios) document.getElementById('citas')?.remove();
  if (!CONFIG.mostrarPepe) document.getElementById('pepe')?.remove();

  /* -------- menú móvil -------- */
  const barra = document.querySelector('.barra');
  const toggle = document.querySelector('.barra__toggle');
  toggle?.addEventListener('click', () => {
    const abierta = barra.classList.toggle('abierta');
    toggle.setAttribute('aria-expanded', String(abierta));
  });
  document.querySelectorAll('.barra__menu a').forEach(a => a.addEventListener('click', () => {
    barra.classList.remove('abierta'); toggle?.setAttribute('aria-expanded', 'false');
  }));

  /* -------- sombra de la barra + enlace activo -------- */
  const enlaces = [...document.querySelectorAll('.barra__menu a[href^="#"]')];
  const secciones = enlaces.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  function alScroll() {
    barra.classList.toggle('con-sombra', window.scrollY > 12);
    let actual = null;
    for (const s of secciones) { if (s.getBoundingClientRect().top <= 120) actual = s.id; }
    enlaces.forEach(a => a.classList.toggle('activo', a.getAttribute('href') === '#' + actual));
  }
  window.addEventListener('scroll', alScroll, { passive: true });
  alScroll();

  /* -------- aparición al hacer scroll -------- */
  const reveals = document.querySelectorAll('.reveal');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(el => el.classList.add('visible'));
  } else {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.95) el.classList.add('visible');
      else io.observe(el);
    });
  }

  /* -------- FAQ: abrir con animación de altura -------- */
  document.querySelectorAll('details').forEach(d => {
    const cuerpo = d.querySelector('.faq__cuerpo');
    if (!cuerpo || reduce) return;
    d.addEventListener('toggle', () => {
      if (d.open) {
        cuerpo.style.height = '0px'; cuerpo.style.opacity = '0';
        requestAnimationFrame(() => {
          cuerpo.style.transition = 'height .35s ease, opacity .35s ease';
          cuerpo.style.height = cuerpo.scrollHeight + 'px'; cuerpo.style.opacity = '1';
          cuerpo.addEventListener('transitionend', () => { cuerpo.style.height = ''; cuerpo.style.transition = ''; }, { once: true });
        });
      }
    });
  });

  /* -------- año en el pie -------- */
  document.querySelectorAll('[data-anio]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
