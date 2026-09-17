/*
 * Genera docs/assets/img/og-portada.jpg, la tarjeta de 1200x630 que se ve cuando
 * alguien comparte el sitio por WhatsApp, Facebook o LinkedIn.
 *
 * La plantilla es herramientas/tarjeta-social.html y usa el CSS y las imágenes
 * reales del sitio, así que la tarjeta siempre queda con la tipografía y los
 * colores de la marca.
 *
 *   cd docs && python3 -m http.server 8765 &
 *   node herramientas/tarjeta-social.mjs
 */
/*
 * Necesita playwright-core y un Chromium. Si no está instalado en el proyecto,
 * se le puede pasar la ruta del módulo y del navegador:
 *
 *   PLAYWRIGHT_CORE=/ruta/node_modules/playwright-core/index.mjs \
 *   CHROMIUM=/ruta/chrome node herramientas/tarjeta-social.mjs
 */
import { copyFileSync, unlinkSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const { chromium } = await import(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const RAIZ = new URL('..', import.meta.url).pathname;
const TEMPORAL = RAIZ + 'docs/_tarjeta-tmp.html';

copyFileSync(RAIZ + 'herramientas/tarjeta-social.html', TEMPORAL);
try {
  const navegador = await chromium.launch({
    executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
  });
  const pagina = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
  await pagina.goto('http://localhost:8765/_tarjeta-tmp.html', { waitUntil: 'networkidle' });
  await pagina.waitForTimeout(600);
  await pagina.screenshot({ path: RAIZ + 'docs/assets/img/og-portada.png' });
  await navegador.close();

  // El PNG pesa medio mega; las redes prefieren JPEG y se ve igual.
  execFileSync('python3', ['-c', `
from PIL import Image
im = Image.open('${RAIZ}docs/assets/img/og-portada.png').convert('RGB')
im.save('${RAIZ}docs/assets/img/og-portada.jpg', 'JPEG', quality=86, optimize=True, progressive=True)
`]);
  unlinkSync(RAIZ + 'docs/assets/img/og-portada.png');
  console.log('docs/assets/img/og-portada.jpg generada');
} finally {
  unlinkSync(TEMPORAL);
}
