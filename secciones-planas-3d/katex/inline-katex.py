#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incrusta KaTeX (JS + CSS + fuentes woff2 en base64) dentro de un archivo HTML
para que el lenguaje matematico se renderice sin depender de archivos externos.

Uso:
    python katex/inline-katex.py "Sistemas de Ecuaciones Lineales.html"

Es idempotente: si el HTML ya tiene KaTeX incrustado (o enlazado por ruta
relativa) reemplaza esos bloques por la version incrustada actual.
Fuente de KaTeX: la carpeta katex/ junto a este script.
"""
import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(HERE, "katex.min.css")
JS_PATH = os.path.join(HERE, "katex.min.js")
FONTS_DIR = os.path.join(HERE, "fonts")


def build_inline_css():
    css = open(CSS_PATH, encoding="utf-8").read()
    # Quitar los src woff/ttf (solo vendorizamos woff2)
    css = re.sub(
        r',url\(fonts/[^)]*\.woff\) format\("woff"\),url\(fonts/[^)]*\.ttf\) format\("truetype"\)',
        "",
        css,
    )

    def repl(m):
        name = m.group(1)
        data = open(os.path.join(FONTS_DIR, name), "rb").read()
        b64 = base64.b64encode(data).decode("ascii")
        return "url(data:font/woff2;base64," + b64 + ")"

    css = re.sub(r"url\(fonts/([^)]+\.woff2)\)", repl, css)
    css = css.replace("</style", "<\\/style")
    return css


def build_inline_js():
    js = open(JS_PATH, encoding="utf-8").read()
    js = js.replace("</script", "<\\/script")
    return js


def inline(html_path):
    html = open(html_path, encoding="utf-8").read()
    css_block = '<style id="katex-inline-css">' + build_inline_css() + "</style>"
    js_block = '<script id="katex-inline-js">' + build_inline_js() + "</script>"

    # CSS: reemplazar <link ...katex.min.css> o el bloque incrustado previo
    if 'id="katex-inline-css"' in html:
        html = re.sub(
            r'<style id="katex-inline-css">.*?</style>', lambda m: css_block, html,
            count=1, flags=re.DOTALL,
        )
    else:
        html, n = re.subn(
            r'<link[^>]*href="katex/katex\.min\.css"[^>]*>', lambda m: css_block, html,
            count=1,
        )
        if n == 0:
            raise SystemExit("No se encontro el <link> de katex.min.css en el HTML.")

    # JS: reemplazar <script src=...katex.min.js> o el bloque incrustado previo
    if 'id="katex-inline-js"' in html:
        html = re.sub(
            r'<script id="katex-inline-js">.*?</script>', lambda m: js_block, html,
            count=1, flags=re.DOTALL,
        )
    else:
        html, n = re.subn(
            r'<script[^>]*src="katex/katex\.min\.js"[^>]*></script>', lambda m: js_block, html,
            count=1,
        )
        if n == 0:
            raise SystemExit("No se encontro el <script src> de katex.min.js en el HTML.")

    open(html_path, "w", encoding="utf-8").write(html)
    size = os.path.getsize(html_path)
    print("OK: KaTeX incrustado en %s (%.0f KB)" % (html_path, size / 1024))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python katex/inline-katex.py <archivo.html>")
    inline(sys.argv[1])
