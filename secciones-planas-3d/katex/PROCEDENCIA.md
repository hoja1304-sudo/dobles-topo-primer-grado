# KaTeX vendorizado

- **Versión:** 0.18.5
- **Fuente:** registro oficial de npm (`https://registry.npmjs.org/katex/-/katex-0.18.5.tgz`)
- **Fecha de incorporación:** 2026-09-02
- **Licencia:** MIT (ver `LICENSE`)

## Contenido

- `katex.min.js` — motor de render.
- `katex.min.css` — estilos y declaraciones `@font-face`.
- `auto-render.min.js` — extensión opcional para renderizar delimitadores `$...$` / `\(...\)` en HTML estático (secciones de teoría).
- `fonts/` — solo formato **woff2** (20 archivos). Todos los navegadores móviles y de escritorio actuales lo soportan; la CSS pide woff2 primero, por lo que no se generan solicitudes 404 a woff/ttf.

## Uso

Se referencia por ruta relativa desde cada interactivo en la raíz del proyecto:

```html
<link rel="stylesheet" href="katex/katex.min.css">
<script defer src="katex/katex.min.js"></script>
<!-- opcional para teoría con $...$ -->
<script defer src="katex/auto-render.min.js"></script>
```

No editar estos archivos. Para actualizar, reemplazar toda la carpeta por una versión nueva del `dist` oficial y actualizar la versión y la fecha de este documento.
