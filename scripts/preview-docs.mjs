import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { readdir, readFile, realpath, stat } from 'node:fs/promises';
import { dirname, extname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Liquid } from 'liquidjs';
import { Marked } from 'marked';

// This previews the Liquid/Markdown used by docs/index.html without publishing.
// GitHub Pages uses Jekyll/Kramdown; this lightweight preview uses LiquidJS/Marked.
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../docs');
const port = Number(process.env.DOCS_PORT || 4173);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error('DOCS_PORT must be an integer from 1 to 65535.');
}
const markdown = new Marked({ gfm: true });
const engine = new Liquid();
engine.registerFilter('uri_escape', value => encodeURIComponent(String(value)));
engine.registerFilter('markdownify', value => markdown.parse(String(value)));

function stripFrontMatter(text) {
  return text.replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/, '');
}

async function getSnapshot() {
  const files = [];
  async function visit(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      if (entry.name.startsWith('.') || entry.name.startsWith('_')) continue;
      const fullPath = join(directory, entry.name);
      if (entry.isDirectory()) await visit(fullPath);
      // Symlinks are intentionally not followed outside the docs source.
      else if (entry.isFile()) files.push(fullPath);
    }
  }
  await visit(root);
  files.sort();
  const pages = [];
  const hash = createHash('sha256');
  let template;
  for (const fullPath of files) {
    const path = relative(root, fullPath).split(sep).join('/');
    const buffer = await readFile(fullPath);
    hash.update(path).update(buffer);
    if (path === 'index.html') template = stripFrontMatter(buffer.toString('utf8'));
    if (extname(path) !== '.md') continue;
    const content = stripFrontMatter(buffer.toString('utf8'));
    const title = content.match(/^#\s+(.+)$/m)?.[1] || path;
    pages.push({ path, name: path.split('/').at(-1), title, content, url: '/' + path.replace(/\.md$/, '.html') });
  }
  for (const file of ['README.md', 'CONTRIBUTING.md']) hash.update(await readFile(resolve(root, '..', file)));
  if (!template) throw new Error('docs/index.html is missing.');
  return { pages, template, version: hash.digest('hex') };
}

function liveReload(version) {
  return `<script>
    document.querySelector('.sidebar-foot span:last-child').textContent = 'LOCAL';
    setInterval(async () => {
      try {
        const response = await fetch('/__docs/version', { cache: 'no-store' });
        if (response.ok && (await response.json()).version !== ${JSON.stringify(version)}) location.reload();
      } catch { /* A stopped preview server must not interrupt reading. */ }
    }, 1000);
  </script>`;
}

const contentTypes = { '.html': 'text/html; charset=utf-8', '.md': 'text/plain; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp' };
const server = createServer(async (request, response) => {
  response.setHeader('Cache-Control', 'no-store');
  try {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      response.writeHead(405, { Allow: 'GET, HEAD' }).end();
      return;
    }
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const rootDocument = { '/__docs/root-readme': 'README.md', '/__docs/root-contributing': 'CONTRIBUTING.md' }[pathname];
    if (rootDocument) {
      const content = await readFile(resolve(root, '..', rootDocument), 'utf8');
      response.writeHead(200, { 'Content-Type': contentTypes['.html'] });
      response.end(request.method === 'HEAD' ? undefined : markdown.parse(stripFrontMatter(content)));
      return;
    }
    if (pathname === '/__docs/version') {
      const { version } = await getSnapshot();
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(request.method === 'HEAD' ? undefined : JSON.stringify({ version }));
      return;
    }
    if (pathname === '/' || pathname === '/index.html') {
      const snapshot = await getSnapshot();
      const rendered = await engine.parseAndRender(snapshot.template, { site: { pages: snapshot.pages } });
      response.writeHead(200, { 'Content-Type': contentTypes['.html'] });
      response.end(request.method === 'HEAD' ? undefined : rendered.replace('</body>', liveReload(snapshot.version) + '</body>'));
      return;
    }
    const candidate = resolve(root, '.' + pathname);
    const actual = await realpath(candidate);
    const subpath = relative(root, actual);
    if (subpath.startsWith('..' + sep) || subpath === '..' || isAbsolute(subpath) || subpath.split(sep).some(part => part.startsWith('.') || part.startsWith('_'))) {
      response.writeHead(404).end('Not found');
      return;
    }
    if (!(await stat(actual)).isFile()) {
      response.writeHead(404).end('Not found');
      return;
    }
    response.writeHead(200, { 'Content-Type': contentTypes[extname(actual)] || 'application/octet-stream' });
    response.end(request.method === 'HEAD' ? undefined : await readFile(actual));
  } catch (error) {
    const missing = ['ENOENT', 'ENOTDIR', 'EACCES'].includes(error.code);
    response.writeHead(missing ? 404 : 500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end(missing ? 'Not found' : '문서 미리보기에 실패했습니다. 터미널의 오류를 확인하세요.');
    if (!missing) console.error(error);
  }
});
server.on('error', error => {
  if (error.code === 'EADDRINUSE') console.error(`포트 ${port}가 사용 중입니다. DOCS_PORT=4174 npm run docs:dev 로 다른 포트를 사용하세요.`);
  else console.error(error);
  process.exitCode = 1;
});
server.listen(port, '127.0.0.1', () => {
  console.log(`문서 미리보기: http://localhost:${port}`);
  console.log('docs/ 파일을 저장하면 브라우저가 자동으로 갱신됩니다. 종료: Ctrl+C');
});
