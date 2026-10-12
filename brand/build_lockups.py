"""Bangun wordmark + lockup Helmcheck K3 sebagai path (tanpa <text>) dari Archivo variabel.

Jalankan dari root project:  python brand/build_lockups.py
Hasil: brand/logo/helmcheck-wordmark.svg, -horizontal.svg, -stacked.svg (+ versi -reversed untuk latar gelap)
"""
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).parent
INK, SIGN, WHITE = "#141B22", "#0B5CAD", "#FFFFFF"
AXES = {"wght": 700, "wdth": 112}           # sama dengan judul website (font-stretch 112%)
TRACK = -12                                  # satuan font (em 1000); tampilan besar butuh sedikit dirapatkan
KERN = {("c", "k"): -6, ("K", "3"): -14}     # koreksi optis hasil inspeksi render
SYMBOL = "M46 28H90V224H46Z M166 28H210V224H166Z M18 134H238V160H18Z M90 134A38 38 0 0 1 166 134Z"
SYMBOL_REV = "M47 29H89V223H47Z M167 29H209V223H167Z M19 135H237V159H19Z M89 135A39 39 0 0 1 167 135Z"

font = instantiateVariableFont(TTFont(ROOT / "fonts" / "Archivo[wdth,wght].ttf"), AXES)
glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
CAP = font["OS/2"].sCapHeight


def word(runs, cap, x0, baseline):
    """runs = [(teks, warna)]. Return (elemen <path>, lebar akhir)."""
    s = cap / CAP
    out, x, prev = [], 0.0, None
    for text, color in runs:
        pen = SVGPathPen(glyphs)
        for ch in text:
            if ch == " ":
                x += hmtx[cmap[ord(ch)]][0] * 0.7 + TRACK   # spasi dipersempit untuk logo
                prev = None
                continue
            x += KERN.get((prev, ch), 0)
            g = cmap[ord(ch)]
            glyphs[g].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x * s, baseline)))
            x += hmtx[g][0] + TRACK
            prev = ch
        out.append(f'<path fill="{color}" d="{pen.getCommands()}"/>')
    return "\n  ".join(out), (x - TRACK) * s


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}">\n'
            f"  <title>{title}</title>\n  {body}\n</svg>\n")


def build(ink, sign, symbol, suffix):
    runs = [("Helmcheck ", ink), ("K3", sign)]
    out = ROOT / "logo"

    # Wordmark saja: cap height 104, margin = 1/4 cap
    paths, w = word(runs, 104, 26, 26 + 104)
    (out / f"helmcheck-wordmark{suffix}.svg").write_text(svg(w + 52, 156, paths, "Helmcheck K3"), encoding="utf-8")

    # Horizontal: simbol 256 + jarak 40 (≈ lebar tiang) + teks cap 104 berpusat di pusat optis simbol (y 126)
    paths, w = word(runs, 104, 278, 126 + 52)
    body = f'<path fill="{sign}" d="{symbol}"/>\n  {paths}'
    (out / f"helmcheck-horizontal{suffix}.svg").write_text(svg(278 + w + 18, 256, body, "Helmcheck K3"), encoding="utf-8")

    # Bertumpuk: simbol di atas, teks cap 64 di bawah, jarak 40
    cap = 64
    _, w = word(runs, cap, 0, 0)
    width = max(w, 220) + 2 * 32
    paths, _ = word(runs, cap, (width - w) / 2, 224 + 40 + cap)
    sym_x = (width - 256) / 2
    body = f'<path fill="{sign}" transform="translate({sym_x:.2f} 0)" d="{symbol}"/>\n  {paths}'
    (out / f"helmcheck-stacked{suffix}.svg").write_text(svg(width, 224 + 40 + cap + 32, body, "Helmcheck K3"), encoding="utf-8")


build(INK, SIGN, SYMBOL, "")
build(WHITE, WHITE, SYMBOL_REV, "-reversed")
print("ok:", sorted(p.name for p in (ROOT / "logo").glob("helmcheck-*.svg")))
