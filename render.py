#!/usr/bin/env python3
"""Render 'THE WORLD TODAY' front page for Monday, 23 November 2026.

Pure Python 3 standard library only. Text is drawn with a built-in 5x7
bitmap font into an RGB buffer, and the PNG is encoded by hand with
zlib + struct (no Pillow, no external libraries).

Run:  python3 render.py        -> writes entry.png (1024x1024) next to
this script.
"""

import struct
import zlib
from pathlib import Path

W, H = 1024, 1024
PAPER = (247, 243, 234)   # warm newsprint off-white
INK = (18, 18, 18)        # near-black ink
RED = (146, 22, 22)       # dark red for kickers / accents
GREY = (96, 90, 80)       # muted grey for source labels

# ---------------------------------------------------------------- font
# Each glyph is 7 rows of 5 pixels, '1' = ink. Uppercase, lowercase,
# digits and common punctuation.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01000", "01110", "01000", "01000", "01000", "01000"),
    "g": ("01110", "10001", "10001", "01110", "00010", "00010", "11100"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "—": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "•": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}

BLANK = ("00000",) * 7


def text_width(text, scale):
    """Pixel width of text at the given scale (6 px advance per glyph)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_width):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if text_width(trial, scale) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 3)
        for i in range(0, len(self.buf), 3):
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = bg

    def pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = color

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.pixel(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_centered(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)


# ---------------------------------------------------------------- stories
# Six stories that happened or were first reported on Monday, 23 Nov 2026.
# Summaries are written from live reporting by the outlets named.
STORIES = [
    {
        "kicker": "CLIMATE",
        "headline": ["COP31 CLIMATE TALKS", "COLLAPSE WITHOUT A DEAL"],
        "body": ("UN climate talks in Turkey ended without a final agreement "
                 "after the EU and others rejected a draft they called too "
                 "weak on fossil fuels. The EU said on Monday it was "
                 "disappointed but would keep pushing for multilateral "
                 "climate action."),
        "source": "Reuters",
    },
    {
        "kicker": "CONFLICT",
        "headline": ["UKRAINE SINKS RUSSIAN", "WARSHIP IN LIBYA"],
        "body": ("President Volodymyr Zelensky said on Monday that Ukrainian "
                 "sea drones sank the Russian corvette Merkury in Benghazi "
                 "and hit the cargo ship MV Angara, extending the war to "
                 "the Mediterranean."),
        "source": "CNN",
    },
    {
        "kicker": "DISASTER",
        "headline": ["INDONESIA CONFIRMS 24", "DEAD IN FACTORY FIRE"],
        "body": ("Indonesia confirmed on Monday that 24 people died in a "
                 "fire at a candy factory in Serang, Banten, as rescuers "
                 "searched for about 30 people still missing."),
        "source": "Reuters",
    },
    {
        "kicker": "TECHNOLOGY",
        "headline": ["NVIDIA BRINGS BACK", "JENSEN HUANG AS CEO"],
        "body": ("Nvidia said on Monday it was reinstating Jensen Huang as "
                 "chief executive, 11 days after he resigned. Shares jumped "
                 "by about a third, lifting global tech stocks."),
        "source": "Reuters",
    },
    {
        "kicker": "HEALTH",
        "headline": ["NHS LAUNCHES WORLD'S", "LARGEST AI BREAST",
                     "SCREENING TRIAL"],
        "body": ("England's NHS began the world's largest trial of "
                 "AI-assisted breast cancer screening, set to involve "
                 "nearly 700,000 women at 30 sites over three years."),
        "source": "University of Cambridge",
    },
    {
        "kicker": "SPORT",
        "headline": ["UK CONFIRMED AS 2035", "WOMEN'S WORLD CUP HOST"],
        "body": ("FIFA confirmed on Monday that England, Northern Ireland, "
                 "Scotland and Wales will host the 2035 Women's World Cup, "
                 "the first World Cup staged in the UK since 1966. The US, "
                 "Mexico, Costa Rica and Jamaica will host the 2031 edition."),
        "source": "Reuters",
    },
]


def draw_story(c, x, y, width, story, head_scale, body_scale,
               head_leading, body_leading):
    """Draw one story block; returns the y just below the source line."""
    c.text(x, y, story["kicker"], 2, RED)
    y += 7 * 2 + 8
    for line in story["headline"]:
        c.text(x, y, line, head_scale, INK)
        y += 7 * head_scale + (head_leading - 7 * head_scale)
    y += 4
    for line in wrap_text(story["body"], body_scale, width):
        c.text(x, y, line, body_scale, INK)
        y += body_leading
    y += 2
    c.text(x, y, "Source: " + story["source"], 2, GREY)
    return y + 7 * 2


def render():
    c = Canvas(W, H, PAPER)
    mx = 40                      # side margin
    content_w = W - 2 * mx

    # Masthead
    c.text_centered(W // 2, 26, "THE WORLD TODAY", 7, INK)
    c.hline(mx, 96, content_w, INK, 3)
    c.hline(mx, 102, content_w, INK, 1)

    # Date bar
    c.text(mx, 112, "EST. 2026", 2, GREY)
    c.text_centered(W // 2, 110, "MONDAY, 23 NOVEMBER 2026", 3, INK)
    right = "FREE EDITION"
    c.text(W - mx - text_width(right, 2), 112, right, 2, GREY)
    c.hline(mx, 140, content_w, INK, 1)

    # Lead story (full width)
    y = draw_story(c, mx, 156, content_w, STORIES[0],
                   head_scale=4, body_scale=2,
                   head_leading=34, body_leading=20)
    c.hline(mx, 348, content_w, INK, 2)

    # Two-column grid: stories 2-3 on row one, 4-5 on row two
    col_w = (content_w - 24) // 2
    col_x = [mx, mx + col_w + 24]
    row_y = [362, 578]
    for i, story in enumerate(STORIES[1:5]):
        x = col_x[i % 2]
        y = row_y[i // 2]
        draw_story(c, x, y, col_w, story,
                   head_scale=3, body_scale=2,
                   head_leading=25, body_leading=19)
    c.vline(mx + col_w + 12, 362, 200, GREY, 1)
    c.vline(mx + col_w + 12, 578, 200, GREY, 1)
    c.hline(mx, 566, content_w, GREY, 1)

    # Bottom strip: story 6 (full width)
    c.hline(mx, 792, content_w, INK, 2)
    draw_story(c, mx, 806, content_w, STORIES[5],
               head_scale=3, body_scale=2,
               head_leading=25, body_leading=19)

    # Footer
    c.hline(mx, 962, content_w, INK, 1)
    c.text_centered(W // 2, 972,
                    "All stories verified from live reporting, 23 November 2026.",
                    2, GREY)
    return c


# ---------------------------------------------------------------- PNG out
def png_bytes(canvas):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.buf[y * stride:(y + 1) * stride]
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    data = png_bytes(render())
    out.write_bytes(data)
    print(f"Wrote {out} ({len(data)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
