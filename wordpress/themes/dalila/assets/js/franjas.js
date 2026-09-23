/* ==========================================================
   Dra. Dalila Peñaranda — franjas de mar
   Las bandas de olas que separan las secciones. Cada franja del
   HTML es un contenedor vacío:

       <div class="franja franja--crema" data-escena="2"></div>

   ...y este archivo la puebla con los stickers reales del
   consultorio (docs/assets/img/mar/) y cinco capas de olas.
   Son decorativas: sin JavaScript la franja simplemente no ocupa
   espacio y las secciones quedan una tras otra.

   data-escena  0–5  reparto de criaturas (ver ESCENAS)
   data-hasta   crema | agua  color de la sección que viene abajo
                (por defecto, el contrario al de la franja)
   ========================================================== */
(function () {

  /* Cada pieza: nombre  izquierda%  ancho  altura%  duración  retraso
     El sufijo ":x" marca las piezas que se ocultan en móvil.        */
  var ESCENAS = [
    'coral-a -1 93 33 7.6 0|tortuga-der 10 126 34 7 1.4|burbujas 19 .55 - 10 2|pez-der:x 24 74 46 15 0|' +
    'coral-b 35 74 33 8.8 2.2|estrella-naranja 45 104 34 9.4 .6|estrella-teal:x 53 64 34 11.5 2.8|' +
    'burbujas 60 .45 - 13 5|coral-c:x 61 93 33 6.8 1.1|ballena-der 73 252 36 11 0|coral-d 92 74 33 9.6 3.1|' +
    'burbujas 70 .5 - 12.5 3.5',

    'coral-c -1 87 33 8.2 1.8|ballena-izq 6 252 36 12 1.5|burbujas 23 .5 - 11 1|coral-a:x 26 81 33 7.2 0|' +
    'estrella-teal 36 60 34 10.6 1.9|estrella-naranja 42 100 34 8.8 3.2|coral-b 53 87 33 9.1 .7|' +
    'pez-izq:x 64 70 46 16 2|burbujas 70 .5 - 12 4|tortuga-izq 74 126 34 7.4 2.6|coral-d 90 81 33 8.4 1.2|' +
    'burbujas 19 .5 - 11 2',

    'coral-b -1 81 33 7.9 .9|ballena-izq 7 244 36 11.6 0|coral-a 25 87 33 8.6 2.4|burbujas 33 .45 - 12 3|' +
    'estrella-teal:x 37 62 34 10.2 1.2|estrella-naranja 43 100 34 9 2.7|coral-c 54 87 33 7.4 1.6|' +
    'pez-der 65 72 46 14.5 1|tortuga-der 75 128 34 7.2 3|burbujas 85 .55 - 10.5 1.5|coral-d 91 78 33 9.2 2|' +
    'burbujas 88 .5 - 13 5.5',

    'coral-d -1 87 33 8.1 2.1|tortuga-der 9 124 34 6.9 .5|burbujas 17 .5 - 11.5 0|pez-der:x 23 72 46 15.5 2.5|' +
    'coral-b 34 78 33 9.3 1.3|estrella-naranja 46 102 34 8.6 3.4|estrella-teal:x 54 62 34 11 1.7|' +
    'coral-a 62 90 33 7.1 2.9|burbujas 70 .45 - 13.5 6|ballena-der 74 248 36 11.4 2|coral-c 92 81 33 8.8 .4|' +
    'burbujas 66 .5 - 10.8 1',

    'coral-a -1 84 33 8.4 1.1|estrella-naranja 11 98 34 9.8 2.3|burbujas 21 .5 - 11.2 .8|coral-c:x 27 90 33 7.7 3.3|' +
    'tortuga-izq 36 122 34 7.1 1.9|pez-izq 50 74 46 15.2 .4|coral-b 60 80 33 8.2 2.6|burbujas 66 .45 - 12.8 4.4|' +
    'estrella-teal 72 63 34 10.8 1.4|ballena-izq 82 246 36 11.8 3|coral-d 95 86 33 9.5 .2',

    'coral-c -1 90 33 7.5 2.8|pez-der 8 73 46 14.8 1.6|burbujas 14 .55 - 10.9 3.2|ballena-der 20 250 36 12.2 .6|' +
    'coral-a 39 82 33 8.9 1.5|estrella-teal 47 64 34 11.3 3.7|estrella-naranja:x 56 101 34 8.4 .9|' +
    'burbujas 63 .5 - 12.2 5.2|coral-b:x 68 88 33 7.3 2.2|tortuga-izq 79 127 34 7.6 .3|coral-d 93 79 33 9.9 2.5'
  ];

  /* Cinco capas de olas: línea de flotación, amplitud, longitud y color. */
  var CAPAS = [
    { y: 52,  a: 15, l: 1500, f: '#F6FAFF' },
    { y: 78,  a: 16, l: 1720, f: '#DDE6F8' },
    { y: 108, a: 13, l: 1620, f: '#C3CFEE' },
    { y: 146, a: 11, l: 1840, f: '#F7FAFF' },
    { y: 174, a: 9,  l: 2040, f: null }      // f = color de la sección de abajo
  ];

  var FONDOS = { crema: '#FBF5EF', agua: '#EEF4FA' };

  var BURBUJAS = '<svg viewBox="0 0 40 90"><circle cx="14" cy="76" r="8"/>' +
    '<circle cx="27" cy="50" r="5.5"/><circle cx="16" cy="24" r="4"/>' +
    '<circle class="brillo" cx="11" cy="73" r="2.4"/></svg>';

  /* Una ola: curva suave muestreada cada 60 px y cerrada por abajo. */
  function onda(y, a, l, fase) {
    var pts = [], x;
    for (x = -160; x <= 2320; x += 60) pts.push([x, y + a * Math.sin((x / l) * Math.PI * 2 + fase)]);
    var d = 'M ' + pts[0][0] + ' ' + pts[0][1].toFixed(1), i, mx, my;
    for (i = 1; i < pts.length - 1; i++) {
      mx = (pts[i][0] + pts[i + 1][0]) / 2;
      my = (pts[i][1] + pts[i + 1][1]) / 2;
      d += ' Q ' + pts[i][0] + ' ' + pts[i][1].toFixed(1) + ' ' + mx + ' ' + my.toFixed(1);
    }
    return d + ' L 2320 200 L -160 200 Z';
  }

  function olas(semilla, hasta) {
    var svg = '<svg class="franja__olas" viewBox="0 0 2160 200" preserveAspectRatio="none" aria-hidden="true">';
    CAPAS.forEach(function (c, i) {
      var fase = semilla * 1.37 + i * 0.83;
      svg += '<path class="ola ola--' + (i + 1) + '" d="' + onda(c.y, c.a, c.l, fase) +
             '" fill="' + (c.f || hasta) + '"/>';
    });
    return svg + '</svg>';
  }

  function piezas(receta) {
    return receta.split('|').map(function (p) {
      var t = p.split(' '), nombre = t[0], extra = '';
      if (nombre.indexOf(':x') > 0) { nombre = nombre.slice(0, -2); extra = ' mar--extra'; }
      var estilo = 'left:' + t[1] + '%;--w:' + t[2] + ';--dur:' + t[4] + 's;--del:-' + t[5] + 's';
      if (nombre === 'burbujas') {
        return '<span class="mar mar--burbujas' + extra + '" style="' + estilo + '">' + BURBUJAS + '</span>';
      }
      var tipo = nombre.split('-')[0];
      return '<img class="mar mar--' + tipo + extra + '" src="' + BASE + 'assets/img/mar/' + nombre +
             '.webp" alt="" loading="lazy" style="' + estilo + ';--b:' + t[3] + '%">';
    }).join('');
  }

  /* Las páginas interiores viven en la misma carpeta que index.html,
     así que la ruta base es relativa al documento. */
  var BASE = document.documentElement.getAttribute('data-base') || '';

  document.querySelectorAll('.franja[data-escena]').forEach(function (el, orden) {
    var n = (parseInt(el.dataset.escena, 10) || 0) % ESCENAS.length;
    var hasta = el.dataset.hasta || (el.classList.contains('franja--agua') ? 'crema' : 'agua');
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = '<div class="franja__escena">' + piezas(ESCENAS[n]) +
                   olas(n + orden * 0.5, FONDOS[hasta] || hasta) + '</div>';
  });
})();
