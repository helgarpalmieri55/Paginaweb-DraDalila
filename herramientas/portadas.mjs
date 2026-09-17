/*
 * Genera las portadas de los artículos que no tienen una pieza de Instagram que
 * les corresponda: docs/assets/img/posts/portada-<tema>.webp, de 1000x1000.
 *
 * La plantilla es herramientas/portadas.html y usa el CSS y la paleta reales del
 * sitio, así que las portadas quedan en la misma familia que el resto.
 *
 *   cd docs && python3 -m http.server 8765 &
 *   node herramientas/portadas.mjs
 */
/*
 * Necesita playwright-core y un Chromium. Si no está instalado en el proyecto,
 * se le puede pasar la ruta del módulo y del navegador:
 *
 *   PLAYWRIGHT_CORE=/ruta/node_modules/playwright-core/index.mjs \
 *   CHROMIUM=/ruta/chrome node herramientas/portadas.mjs
 */
import { copyFileSync, unlinkSync, mkdtempSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const { chromium } = await import(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const RAIZ = new URL('..', import.meta.url).pathname;
const TEMPORAL = RAIZ + 'docs/_portadas-tmp.html';
const SALIDA = RAIZ + 'docs/assets/img/posts/';
const paso = mkdtempSync(join(tmpdir(), 'portadas-'));

copyFileSync(RAIZ + 'herramientas/portadas.html', TEMPORAL);
try {
  const navegador = await chromium.launch({
    executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
  });
  const pagina = await navegador.newPage({ viewport: { width: 1000, height: 1000 } });
  await pagina.goto('http://localhost:8765/_portadas-tmp.html', { waitUntil: 'networkidle' });
  await pagina.waitForTimeout(700);

  // Una sola captura de la página y luego se recortan los cuadros: las capturas
  // por elemento dejaban fuera la ola de alguna portada al desplazar la página.
  const temas = await pagina.$$eval('.portada', ns => ns.map(n => n.id.replace(/^p-/, '')));
  const hoja = join(paso, 'hoja.png');
  await pagina.screenshot({ path: hoja, fullPage: true });
  temas.forEach((tema, i) => {
    execFileSync('python3', ['-c', `
from PIL import Image
hoja = Image.open(${JSON.stringify(hoja)}).convert('RGB')
hoja.crop((0, ${i} * 1000, 1000, ${i + 1} * 1000)).save(
    ${JSON.stringify(SALIDA + 'portada-')} + ${JSON.stringify(tema)} + '.webp',
    'WEBP', quality=88, method=6)
`]);
    console.log('portada-' + tema + '.webp');
  });

  await navegador.close();
  console.log(temas.length + ' portadas generadas');
} finally {
  unlinkSync(TEMPORAL);
  rmSync(paso, { recursive: true, force: true });
}
