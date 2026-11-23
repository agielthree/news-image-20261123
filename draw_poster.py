#!/usr/bin/env python3
"""Draw 'The World in One Day' — a one-image summary of Monday 23 November 2026.

Pure stdlib + Pillow. Deterministic: no network, no clock, no randomness.
Reads nothing but the fonts on disk; writes entry.png (1024x1024) next to
this file, and /output/entry.png when run as the competition entrypoint
helper. The submitted program itself (main.ts) copies entry.png to
/output/entry.png, so the judged bytes are exactly this file's output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
GAP = 16

PAPER = (246, 241, 231)
INK = (20, 33, 61)
INK_SOFT = (58, 64, 78)
RULE_RED = (192, 57, 43)
CARD = (255, 255, 255)
BORDER = (198, 190, 175)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# (category, colour, headline, summary, stat, pictogram)
STORIES = [
    (
        "CLIMATE",
        (27, 122, 77),
        "COP31 TALKS COLLAPSE",
        "The longest-ever UN climate summit ends in Antalya with no deal, "
        "as the fossil-fuel fight splits nearly 200 nations.",
        "NO DEAL IN ANTALYA",
        "globe",
    ),
    (
        "AMERICA",
        (29, 78, 216),
        "DEMOCRATS TAKE THE HOUSE",
        "Democrats clinch 258 seats in the US House \u2014 their largest "
        "majority in more than three decades.",
        "258 SEATS",
        "ballot",
    ),
    (
        "WAR AT SEA",
        (51, 65, 85),
        "UKRAINE HITS RUSSIAN WARSHIP",
        "A Ukrainian naval drone severely damages the corvette Merkury off "
        "Libya; the cargo ship Angara is hit too.",
        "SHIP HIT OFF LIBYA",
        "ship",
    ),
    (
        "DIPLOMACY",
        (180, 83, 9),
        "TRUMP WARNS IRAN: DEAL OR WAR",
        "Trump says he is \u2018inclined\u2019 to resume conflict if Tehran "
        "strikes no deal by the New Year.",
        "DEADLINE: NEW YEAR",
        "warning",
    ),
    (
        "DISASTER",
        (185, 28, 28),
        "FACTORY FIRE KILLS 24 IN INDONESIA",
        "A blaze at a candy factory in Banten leaves at least 24 dead and "
        "about 30 people unaccounted for.",
        "24 DEAD \u00b7 30 MISSING",
        "flame",
    ),
    (
        "SPORT",
        (21, 128, 61),
        "LIVERPOOL ROUT MAN UNITED 4\u20130",
        "Liverpool thrash 10-man Manchester United 4\u20130 in Mauricio "
        "Pochettino\u2019s first match in charge.",
        "4\u20130 AT ANFIELD",
        "ball",
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_pictogram(draw, kind, cx, cy, r, colour):
    """Small geometric pictogram centred at (cx, cy), radius r, in colour."""
    if kind == "globe":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
        draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=colour, width=3)
        draw.line([cx - r, cy, cx + r, cy], fill=colour, width=3)
        draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=colour, width=3)
    elif kind == "ballot":
        b = r
        draw.rectangle([cx - b, cy - b // 2, cx + b, cy + b], outline=colour, width=4)
        draw.line([cx - b // 2, cy - b // 2, cx + b // 2, cy - b // 2], fill=colour, width=4)
        draw.line(
            [cx - b * 3 // 4, cy + b // 4, cx - b // 4, cy + b * 3 // 4,
             cx + b * 3 // 4, cy - b // 4],
            fill=colour, width=4, joint="curve",
        )
    elif kind == "ship":
        draw.polygon(
            [(cx - r, cy + r // 3), (cx + r, cy + r // 3),
             (cx + r // 2, cy + r), (cx - r // 2, cy + r)],
            fill=colour, outline=colour,
        )
        draw.line([cx, cy - r, cx, cy + r // 3], fill=colour, width=4)
        draw.line([cx, cy - r, cx + r // 2, cy - r // 3], fill=colour, width=3)
        draw.arc([cx - r, cy + r // 2, cx - r // 4, cy + r], 0, 180, fill=colour, width=3)
        draw.arc([cx + r // 4, cy + r // 2, cx + r, cy + r], 0, 180, fill=colour, width=3)
    elif kind == "warning":
        draw.polygon(
            [(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)],
            outline=colour, width=4,
        )
        draw.line([cx, cy - r // 3, cx, cy + r // 3], fill=colour, width=5)
        draw.ellipse([cx - 3, cy + r // 2, cx + 3, cy + r // 2 + 6], fill=colour)
    elif kind == "flame":
        draw.polygon(
            [(cx, cy - r),
             (cx + r // 2, cy - r // 4), (cx + r, cy + r // 2),
             (cx + r // 2, cy + r), (cx - r // 2, cy + r),
             (cx - r, cy + r // 2), (cx - r // 2, cy - r // 4)],
            fill=colour,
        )
        draw.ellipse([cx - r // 3, cy, cx + r // 3, cy + r // 2], fill=PAPER)
    elif kind == "ball":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
        pr = r // 3
        draw.polygon(
            [(cx, cy - pr), (cx + pr, cy - pr // 3), (cx + pr // 2, cy + pr),
             (cx - pr // 2, cy + pr), (cx - pr, cy - pr // 3)],
            fill=colour,
        )
        for dx, dy in [(0, -1), (1, 0), (-1, 0), (0, 1)]:
            draw.line([cx, cy, cx + dx * r, cy + dy * r], fill=colour, width=3)


def draw_panel(draw, x, y, w, h, story):
    category, colour, headline, summary, stat, picto = story
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=2)
    # Colour band with category label + pictogram medallion.
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 40], fill=colour)
    cat_font = font(SANS_B, 20)
    draw.text((x + 16, y + 10), category, font=cat_font, fill=WHITE)
    pcx, pcy, pr = x + w - 46, y + 21, 15
    draw.ellipse([pcx - pr - 4, pcy - pr - 4, pcx + pr + 4, pcy + pr + 4], fill=WHITE)
    draw_pictogram(draw, picto, pcx, pcy, pr, colour)
    # Headline, up to two lines.
    head_font = font(SERIF_B, 29)
    lines = wrap_text(draw, headline, head_font, w - 32)[:2]
    hy = y + 54
    for line in lines:
        draw.text((x + 16, hy), line, font=head_font, fill=INK)
        hy += 36
    # Summary, up to three lines.
    sum_font = font(SANS, 18)
    slines = wrap_text(draw, summary, sum_font, w - 32)[:3]
    sy = y + 54 + len(lines) * 36 + 8
    for line in slines:
        draw.text((x + 16, sy), line, font=sum_font, fill=INK_SOFT)
        sy += 25
    # Key-number strip at the bottom.
    stat_font = font(SANS_B, 23)
    draw.text((x + 16, y + h - 40), stat, font=stat_font, fill=colour)


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Outer frame.
    draw.rectangle([12, 12, W - 12, H - 12], outline=INK, width=3)
    # Masthead.
    mast_font = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=mast_font)
    draw.text(((W - tw) / 2, 40), title, font=mast_font, fill=INK)
    date_font = font(SANS_B, 22)
    dateline = "MONDAY  \u00b7  23 NOVEMBER 2026"
    dw = draw.textlength(dateline, font=date_font)
    draw.text(((W - dw) / 2, 118), dateline, font=date_font, fill=RULE_RED)
    draw.line([MARGIN, 152, W - MARGIN, 152], fill=INK, width=3)
    draw.line([MARGIN, 158, W - MARGIN, 158], fill=RULE_RED, width=2)
    # Grid of six panels: 2 columns x 3 rows.
    pw = (W - 2 * MARGIN - GAP) // 2
    ph = 260
    top = 176
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = MARGIN + col * (pw + GAP)
        y = top + row * (ph + GAP)
        draw_panel(draw, x, y, pw, ph, story)
    # Footer.
    foot_font = font(SANS, 15)
    footer = ("Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Xinhua \u00b7 NPR  "
              "\u2014  Drawn by an AI agent for make.fun")
    fw = draw.textlength(footer, font=foot_font)
    draw.text(((W - fw) / 2, 992), footer, font=foot_font, fill=INK_SOFT)
    return img


def main():
    img = draw_poster()
    here = os.path.dirname(os.path.abspath(__file__))
    out_local = os.path.join(here, "entry.png")
    img.save(out_local, format="PNG", optimize=True)
    print("wrote", out_local, img.size)


if __name__ == "__main__":
    main()
