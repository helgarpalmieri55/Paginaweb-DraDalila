/* ==========================================================
   Dra. Dalila Peñaranda — sitio informativo
   Configuración e interacciones (sin dependencias)
   ========================================================== */

/* -------- CONFIGURACIÓN: edita aquí los datos reales -------- */
const CONFIG = {
  whatsapp: '+57 304 653 2006',            // número visible y del enlace wa.me
  mensajeWhatsApp: 'Hola doctora, quiero agendar una cita',
  correo: 'nutripedcm@gmail.com',
  direccion: 'Calle 1C # 30-40, High Park Medical Center',
  direccion2: 'Consultorio 129 · Barranquilla, Colombia',
  precioPresencial: '$180.000',            // pendiente de confirmar con la doctora
  precioVirtual: '45 USD',                 // pendiente de confirmar con la doctora
  mostrarPrecios: true,                    // false oculta la sección "Tu cita"
  mostrarPepe: true,                       // false oculta el bloque de Pepe
  redes: { instagram: 'https://www.instagram.com/dra.dalilapenaranda/' },   // por ahora solo tiene Instagram
  // Enlaces de compra. Mientras estén vacíos, el botón abre WhatsApp con el
  // nombre del curso escrito; al pegar un enlace, ese curso pasa a comprarse allí.
  hotmart: {
    complementaria: '',
    lonchera: '',
    habitos: '',
    escuela: ''
  }
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
  /* Botón de compra: va a Hotmart si ya hay enlace; si no, abre WhatsApp
     con el curso escrito, para acordar el pago directamente con la doctora. */
  document.querySelectorAll('[data-curso]').forEach(a => {
    const url = CONFIG.hotmart[a.dataset.curso];
    a.target = '_blank'; a.rel = 'noopener';
    if (url) { a.href = url; return; }
    a.href = 'https://wa.me/' + digits + '?text=' +
      encodeURIComponent('Hola doctora, quiero tomar ' + (a.dataset.nombre || 'uno de sus cursos') +
                         '. ' + (a.dataset.pregunta || '¿Cómo hago el pago?'));
  });

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

  /* -------- sombra de la barra al bajar -------- */
  function alScroll() { barra?.classList.toggle('con-sombra', window.scrollY > 12); }
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

  /* -------- blog: filtro por categoría -------- */
  const filtros = document.querySelectorAll('.filtro[data-cat]');
  if (filtros.length) {
    const articulos = [...document.querySelectorAll('[data-cat]:not(.filtro)')];
    const vacio = document.querySelector('.sin-resultados');
    filtros.forEach(b => b.addEventListener('click', () => {
      const cat = b.dataset.cat;
      filtros.forEach(o => o.setAttribute('aria-pressed', String(o === b)));
      let visibles = 0;
      articulos.forEach(a => {
        const va = cat === 'todo' || a.dataset.cat === cat;
        a.hidden = !va;
        if (va) { visibles++; a.classList.remove('visible'); requestAnimationFrame(() => a.classList.add('visible')); }
      });
      if (vacio) vacio.hidden = visibles > 0;
    }));
  }

  /* -------- contacto: validación y envío simulado --------
     Aún no hay servidor: el formulario valida, muestra el mensaje de
     confirmación y abre WhatsApp con el texto ya redactado.          */
  const form = document.querySelector('.formulario');
  if (form) {
    const marcar = (campo, mal) => campo.classList.toggle('malo', mal);
    form.querySelectorAll('input,select,textarea').forEach(c => {
      c.addEventListener('blur', () => { if (c.value.trim()) marcar(c.closest('.campo') || c.parentElement, !c.checkValidity()); });
      c.addEventListener('input', () => { const w = c.closest('.campo'); if (w && w.classList.contains('malo') && c.checkValidity()) marcar(w, false); });
    });
    form.addEventListener('submit', e => {
      e.preventDefault();
      let ok = true;
      form.querySelectorAll('input,select,textarea').forEach(c => {
        const w = c.closest('.campo');
        if (!c.checkValidity()) { ok = false; if (w) marcar(w, true); else c.focus(); }
      });
      if (!ok) { form.querySelector('.malo input,.malo select,.malo textarea,:invalid')?.focus(); return; }
      const nombre = form.querySelector('#nombre')?.value.trim() || '';
      const motivo = form.querySelector('#motivo')?.value || '';
      const mensaje = form.querySelector('#mensaje')?.value.trim() || '';
      const texto = 'Hola doctora, soy ' + nombre + '. Escribo por: ' + motivo + '. ' + mensaje;
      form.classList.add('listo');
      form.querySelector('.enviado')?.focus?.();
      window.open('https://wa.me/' + digits + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
    });
  }

  /* -------- año en el pie -------- */
  document.querySelectorAll('[data-anio]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
