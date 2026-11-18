#!/usr/bin/env python3
"""Round 2 entry for news-image-20261118: dense newspaper front page, 45 stories.
Drawn by hand with PIL. Deterministic, no network. All artwork is original."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 226)
INK = (28, 28, 28)
MUTED = (90, 86, 72)
PANEL = (255, 255, 255)
BORDER = (198, 190, 168)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
ORANGE = (194, 102, 20)
PURPLE = (106, 62, 140)
GOLD = (176, 141, 30)
LAND = (222, 213, 182)
SEA = (198, 222, 235)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 62)
F_EYE = font("DejaVuSans-Bold.ttf", 14)
F_TAG = font("DejaVuSans-Bold.ttf", 12)
F_TAG_S = font("DejaVuSans-Bold.ttf", 11)
F_HEAD = font("DejaVuSerif-Bold.ttf", 21)
F_HEAD_M = font("DejaVuSerif-Bold.ttf", 17)
F_HEAD_S = font("DejaVuSerif-Bold.ttf", 15)
F_DECK = font("DejaVuSans.ttf", 13)
F_DECK_M = font("DejaVuSans.ttf", 12)
F_DECK_S = font("DejaVuSans.ttf", 11)
F_ALSO = font("DejaVuSans.ttf", 10)
F_ALSO_B = font("DejaVuSans-Bold.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 10)
F_TINY = font("DejaVuSans-Bold.ttf", 9)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, w, text, fnt, lh, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def center(draw, cx, y, text, fnt, fill=INK):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


# --- Simplified world coastlines (lon, lat), hand-drawn approximations ---
NORTH_AMERICA = [(-168, 66), (-160, 58), (-152, 60), (-140, 60), (-135, 57),
                 (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29),
                 (-110, 24), (-105, 20), (-97, 16), (-92, 15), (-86, 12),
                 (-83, 9), (-79, 9), (-81, 13), (-84, 16), (-87, 21),
                 (-90, 21), (-91, 19), (-96, 19), (-97, 26), (-93, 30),
                 (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
                 (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
                 (-55, 47), (-60, 52), (-64, 58), (-68, 58), (-72, 62),
                 (-78, 62), (-85, 66), (-92, 66), (-95, 69), (-110, 68),
                 (-125, 70), (-140, 70), (-155, 71), (-165, 68), (-168, 66)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-74, -50), (-70, -54), (-66, -55), (-68, -50), (-65, -45),
                 (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23),
                 (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
                 (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
                 (-72, 12), (-76, 10), (-79, 9)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (25, 32), (32, 31), (34, 28),
          (35, 23), (37, 18), (40, 15), (43, 11), (48, 11), (51, 12),
          (46, 5), (42, 0), (40, -5), (40, -10), (36, -18), (33, -26),
          (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
          (13, -5), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
           (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62),
           (12, 64), (18, 69), (25, 71), (30, 70), (40, 68), (50, 69),
           (60, 69), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
           (120, 73), (130, 72), (140, 72), (150, 70), (158, 69), (162, 66),
           (170, 66), (178, 65), (178, 62), (170, 60), (162, 58), (158, 52),
           (150, 59), (142, 55), (140, 50), (135, 44), (130, 42), (127, 40),
           (122, 38), (120, 34), (122, 30), (120, 27), (118, 25), (110, 21),
           (108, 18), (105, 10), (103, 8), (100, 7), (98, 10), (95, 16),
           (92, 21), (90, 22), (86, 20), (82, 17), (80, 13), (77, 8),
           (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 25),
           (56, 27), (54, 27), (52, 28), (50, 29), (48, 30), (44, 29),
           (40, 31), (36, 36), (33, 36), (30, 36), (27, 37), (23, 36),
           (22, 37), (19, 40), (15, 38), (12, 42), (10, 44), (7, 44),
           (3, 43), (0, 39), (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AUSTRALIA = [(113, -22), (114, -30), (115, -34), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
             (113, -22)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 62), (-32, 68),
             (-25, 70), (-20, 70), (-22, 74), (-30, 76), (-45, 76),
             (-55, 74), (-60, 70), (-58, 64)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
         (141, 39), (141, 42), (143, 44), (145, 44), (143, 42), (141, 40),
         (140, 37), (139, 35), (137, 34), (135, 33), (132, 32), (130, 31)]
CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, AUSTRALIA,
              GREENLAND, UK, JAPAN]


def project(x0, y0, w, h, lon, lat):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (85.0 - lat) / 140.0 * h
    return (x, y)


def draw_world_map(draw, x0, y0, w, h, pins, dots):
    """pins: list of (num, lon, lat); dots: list of (lon, lat, color)."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    for poly in CONTINENTS:
        pts = [project(x0, y0, w, h, lo, la) for lo, la in poly]
        draw.polygon(pts, fill=LAND, outline=(150, 140, 110))
    for lo, la, col in dots:
        px, py = project(x0, y0, w, h, lo, la)
        draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=col)
    for num, lo, la in pins:
        px, py = project(x0, y0, w, h, lo, la)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        s = str(num)
        tw = draw.textlength(s, font=F_TINY)
        draw.text((px - tw / 2, py - 5), s, font=F_TINY, fill=(255, 255, 255))


def illu_gulf(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # land masses: Arabia below, Iran above
    draw.polygon([(x, y + h), (x + w * 0.30, y + h * 0.55),
                  (x + w * 0.75, y + h * 0.62), (x + w, y + h * 0.45),
                  (x + w, y + h), (x, y + h)], fill=LAND)
    draw.polygon([(x, y), (x + w, y), (x + w, y + h * 0.30),
                  (x + w * 0.55, y + h * 0.42), (x, y + h * 0.38)],
                 fill=(232, 222, 196))
    # gulf water line
    draw.line([(x + w * 0.10, y + h * 0.42), (x + w * 0.45, y + h * 0.50),
               (x + w * 0.80, y + h * 0.36)], fill=(90, 140, 170), width=3)
    # dashed drone path
    for i in range(6):
        px = x + w * (0.42 + i * 0.055)
        py = y + h * (0.52 - i * 0.045)
        draw.line([(px, py), (px + 8, py - 6)], fill=RED, width=2)
    draw.ellipse([x + w * 0.30 - 5, y + h * 0.55 - 5, x + w * 0.30 + 5,
                  y + h * 0.55 + 5], fill=RED)
    draw.text((x + 4, y + 2), "BAHRAIN", font=F_TINY, fill=INK)
    draw.text((x + w - 52, y + h - 13), "HORMUZ", font=F_TINY, fill=INK)


def illu_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # table
    draw.ellipse([x + w * 0.12, y + h * 0.52, x + w * 0.88, y + h * 0.78],
                 fill=(122, 84, 44))
    draw.ellipse([x + w * 0.18, y + h * 0.55, x + w * 0.82, y + h * 0.72],
                 fill=(146, 104, 58))
    # three flags on poles
    def flag(fx, colors):
        draw.line([(fx, y + h * 0.18), (fx, y + h * 0.55)], fill=INK, width=2)
        for j, c in enumerate(colors):
            draw.rectangle([fx, y + h * 0.18 + j * 7, fx + 26,
                            y + h * 0.18 + (j + 1) * 7], fill=c)
    flag(x + w * 0.20, [(178, 34, 52), (255, 255, 255), (178, 34, 52)])
    flag(x + w * 0.48, [(222, 41, 16)])
    draw.ellipse([x + w * 0.48 + 10, y + h * 0.18 + 6,
                  x + w * 0.48 + 16, y + h * 0.18 + 12], fill=(255, 215, 0))
    flag(x + w * 0.76, [(255, 255, 255), (0, 57, 166), (213, 0, 50)])
    draw.text((x + 4, y + h - 13), "SHENZHEN", font=F_TINY, fill=INK)
    draw.text((x + w - 52, y + h - 13), "THURSDAY", font=F_TINY, fill=INK)


def illu_alaska(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
    # capitol dome
    cx = x + w * 0.30
    draw.rectangle([cx - 26, y + h * 0.55, cx + 26, y + h * 0.92],
                   fill=(240, 240, 235), outline=INK)
    draw.pieslice([cx - 26, y + h * 0.28, cx + 26, y + h * 0.62], 180, 360,
                  fill=(240, 240, 235), outline=INK)
    draw.line([(cx, y + h * 0.16), (cx, y + h * 0.30)], fill=INK, width=2)
    for i in range(4):
        lx = cx - 18 + i * 12
        draw.line([(lx, y + h * 0.60), (lx, y + h * 0.90)], fill=INK, width=2)
    # bar chart 56 vs 44
    bx = x + w * 0.62
    draw.rectangle([bx, y + h * 0.62, bx + 18, y + h * 0.92], fill=BLUE)
    draw.rectangle([bx + 26, y + h * 0.72, bx + 44, y + h * 0.92],
                   fill=(178, 34, 52))
    draw.text((bx - 4, y + h * 0.50), "56 DEM", font=F_TINY, fill=BLUE)
    draw.text((bx + 22, y + h * 0.60), "44 REP", font=F_TINY, fill=(178, 34, 52))
    draw.text((x + 4, y + 2), "ALASKA", font=F_TINY, fill=INK)


def illu_drones(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 42, 60))
    # radar dish
    cx, cy = x + w * 0.5, y + h * 0.52
    draw.arc([cx - 15, cy - 13, cx + 15, cy + 13], 200, 340, fill=(250, 200, 60),
             width=3)
    draw.line([(cx, cy), (cx - 11, cy + 13)], fill=(250, 200, 60), width=3)
    draw.line([(cx, cy), (cx + 11, cy + 13)], fill=(250, 200, 60), width=3)
    # signal waves
    for r in (8, 13):
        draw.arc([cx - r, cy - r - 6, cx + r, cy + r - 6], 250, 290,
                 fill=(120, 200, 220), width=2)
    # drones
    for dx, dy in ((0.16, 0.22), (0.84, 0.18), (0.80, 0.48)):
        px, py = x + w * dx, y + h * dy
        draw.ellipse([px - 4, py - 2, px + 4, py + 2], fill=(220, 220, 220))
        draw.line([(px - 9, py), (px + 9, py)], fill=(220, 220, 220), width=2)
        draw.ellipse([px - 2, py - 5, px + 2, py + 5], fill=RED)


def illu_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # warning triangle
    cx, cy = x + w * 0.5, y + h * 0.42
    draw.polygon([(cx, cy - 30), (cx - 30, cy + 22), (cx + 30, cy + 22)],
                 fill=(240, 190, 40), outline=INK)
    draw.text((cx - 4, cy - 14), "!", font=font("DejaVuSans-Bold.ttf", 22),
              fill=INK)
    # olive branch
    draw.line([(x + w * 0.15, y + h * 0.88), (x + w * 0.85, y + h * 0.78)],
              fill=(60, 110, 50), width=3)
    for i in range(5):
        lx = x + w * (0.22 + i * 0.14)
        ly = y + h * (0.86 - i * 0.02)
        draw.ellipse([lx - 7, ly - 5, lx + 7, ly + 5], fill=(90, 140, 70))


def illu_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(206, 226, 238))
    # bay of bengal coastline hint
    draw.polygon([(x, y + h * 0.15), (x + w * 0.35, y + h * 0.10),
                  (x + w * 0.55, y + h * 0.30), (x + w * 0.45, y + h * 0.75),
                  (x + w * 0.15, y + h * 0.95), (x, y + h * 0.70)],
                 fill=LAND)
    # spiral
    cx, cy = x + w * 0.68, y + h * 0.45
    for r, a0, a1 in ((8, 0, 300), (16, 40, 340), (24, 80, 20), (32, 120, 60)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=TEAL, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=TEAL)
    draw.text((x + 4, y + h - 13), "BAY OF BENGAL", font=F_TINY, fill=INK)


def illu_uk(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 238, 232))
    # fuel pump
    px, py = x + w * 0.16, y + h * 0.30
    draw.rectangle([px, py, px + 34, py + 52], fill=(40, 60, 90))
    draw.rectangle([px + 8, py + 10, px + 26, py + 26], fill=(200, 225, 240))
    draw.text((px + 2, py + 32), "£", font=font("DejaVuSans-Bold.ttf", 16),
              fill=(255, 255, 255))
    # rising arrow chart
    pts = [(x + w * 0.55, y + h * 0.78), (x + w * 0.65, y + h * 0.62),
           (x + w * 0.72, y + h * 0.68), (x + w * 0.86, y + h * 0.38)]
    draw.line(pts, fill=RED, width=4)
    draw.polygon([(x + w * 0.86, y + h * 0.38), (x + w * 0.78, y + h * 0.38),
                  (x + w * 0.86, y + h * 0.48)], fill=RED)
    draw.text((x + w * 0.55, y + h * 0.16), "3.6%", font=F_HEAD_S, fill=RED)


def illu_sudan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
    # africa outline (reuse data, local projection)
    def proj(lo, la):
        return (x + w * (lo + 20) / 75.0, y + h * (35 - la) / 75.0)
    pts = [proj(lo, la) for lo, la in AFRICA]
    draw.polygon(pts, fill=LAND, outline=(150, 140, 110))
    # magnifier over Sudan
    mx, my = proj(30, 13)
    draw.ellipse([mx - 20, my - 20, mx + 20, my + 20], outline=RED, width=3)
    draw.line([(mx + 14, my + 14), (mx + 30, my + 30)], fill=RED, width=4)
    draw.text((x + 4, y + 2), "EL OBEID", font=F_TINY, fill=INK)


def illu_gta(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(26, 30, 44))
    # game controller
    cx, cy = x + w * 0.5, y + h * 0.52
    draw.rounded_rectangle([cx - 42, cy - 18, cx + 42, cy + 18], radius=12,
                           fill=(90, 60, 140))
    draw.ellipse([cx - 30, cy - 8, cx - 18, cy + 4], fill=(220, 220, 220))
    draw.ellipse([cx + 18, cy - 8, cx + 30, cy + 4], fill=(220, 220, 220))
    for bx, by, c in ((cx - 26, cy - 12, (255, 80, 80)),
                      (cx - 14, cy - 14, (255, 220, 80)),
                      (cx + 12, cy - 14, (80, 200, 120)),
                      (cx + 24, cy - 12, (80, 140, 255))):
        draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=c)
    draw.text((x + 4, y + 2), "MIDNIGHT LAUNCH", font=F_TINY,
              fill=(255, 255, 255))


def illu_antibiotic(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244))
    # capsule
    cx, cy = x + w * 0.45, y + h * 0.42
    draw.rounded_rectangle([cx - 34, cy - 13, cx + 34, cy + 13], radius=13,
                           fill=(60, 120, 200))
    draw.rounded_rectangle([cx, cy - 13, cx + 34, cy + 13], radius=13,
                           fill=(240, 240, 240))
    draw.line([(cx, cy - 13), (cx, cy + 13)], fill=INK, width=1)
    # bacteria: small rods with tails
    for bx, by, ang in ((0.78, 0.30, 30), (0.82, 0.62, -20), (0.70, 0.78, 10)):
        px, py = x + w * bx, y + h * by
        draw.ellipse([px - 7, py - 4, px + 7, py + 4], fill=(180, 60, 60))
        draw.line([(px + 7, py), (px + 16, py - 6)], fill=(180, 60, 60),
                  width=2)
    draw.text((x + 4, y + h - 13), "+72% SINCE 2019", font=F_TINY, fill=RED)


def illu_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(224, 238, 230))
    # globe
    cx, cy = x + w * 0.38, y + h * 0.48
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(140, 190, 220),
                 outline=BLUE, width=2)
    draw.arc([cx - 30, cy - 30, cx + 30, cy + 30], 90, 270, fill=BLUE, width=2)
    draw.ellipse([cx - 12, cy - 30, cx + 12, cy + 30], outline=BLUE, width=1)
    draw.line([(cx - 30, cy), (cx + 30, cy)], fill=BLUE, width=1)
    draw.ellipse([cx - 16, cy - 12, cx + 2, cy + 4], fill=(90, 160, 90))
    draw.ellipse([cx + 4, cy + 8, cx + 18, cy + 22], fill=(90, 160, 90))
    # thermometer
    tx = x + w * 0.80
    draw.rounded_rectangle([tx - 6, cy - 28, tx + 6, cy + 22], radius=6,
                           fill=(255, 255, 255), outline=INK)
    draw.ellipse([tx - 11, cy + 14, tx + 11, cy + 36], fill=RED)
    draw.rectangle([tx - 3, cy - 20, tx + 3, cy + 22], fill=RED)
    draw.text((x + 4, y + h - 13), "35x35 GOAL", font=F_TINY, fill=INK)


def illu_bangladesh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 230, 214))
    # factory
    fx, fy = x + w * 0.10, y + h * 0.55
    draw.rectangle([fx, fy, fx + 74, fy + 34], fill=(150, 90, 60))
    draw.rectangle([fx + 6, fy - 22, fx + 14, fy], fill=(120, 70, 50))
    draw.rectangle([fx + 22, fy - 30, fx + 30, fy], fill=(120, 70, 50))
    for wx in (fx + 8, fx + 28, fx + 48):
        draw.rectangle([wx, fy + 8, wx + 12, fy + 20], fill=(255, 230, 140))
    # protest sign
    sx = x + w * 0.72
    draw.line([(sx, y + h * 0.44), (sx, y + h * 0.92)], fill=INK, width=3)
    draw.rectangle([sx - 26, y + h * 0.06, sx + 26, y + h * 0.44],
                   fill=(255, 255, 255), outline=RED, width=2)
    draw.text((sx - 22, y + h * 0.20), "Tk 30,000", font=F_TINY, fill=RED)


def illu_australia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(236, 230, 214))
    # australia outline
    def proj(lo, la):
        return (x + w * (lo - 112) / 44.0, y + h * (-10 - la) / 32.0)
    pts = [proj(lo, la) for lo, la in AUSTRALIA]
    draw.polygon(pts, fill=(222, 190, 140), outline=(150, 120, 80))
    # gavel
    gx, gy = x + w * 0.72, y + h * 0.30
    draw.line([(gx - 16, gy + 10), (gx + 16, gy - 10)], fill=(90, 60, 30),
              width=6)
    draw.line([(gx - 6, gy + 22), (gx + 12, gy + 4)], fill=(120, 80, 40),
              width=4)
    draw.text((x + 4, y + h - 13), "SANCTIONS", font=F_TINY, fill=INK)


def lead_panel(draw, x, y, w, h, illu, tag, tag_col, headline, deck):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER)
    illu(draw, x + 6, y + 6, w - 12, 94)
    draw.text((x + 8, y + 106), tag, font=F_TAG, fill=tag_col)
    yy = block(draw, x + 8, y + 122, w - 16, headline, F_HEAD, 23, max_lines=3)
    block(draw, x + 8, yy + 3, w - 16, deck, F_DECK, 14, max_lines=3)


def med_panel(draw, x, y, w, h, illu, tag, tag_col, headline, deck):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER)
    illu(draw, x + 5, y + 5, w - 10, 46)
    draw.text((x + 7, y + 56), tag, font=F_TAG_S, fill=tag_col)
    yy = block(draw, x + 7, y + 72, w - 14, headline, F_HEAD_S, 18,
               max_lines=3)
    block(draw, x + 7, yy + 2, w - 14, deck, F_DECK_S, 13, max_lines=4)


LEADS = [
    (illu_gulf, "1  MIDDLE EAST · IRAN WAR", RED,
     "Kuwait, Bahrain say they intercepted Iranian drones",
     "Iran's army says it aimed at US forces at Ali Al Salem. ADNOC says "
     "its ship was hit in Hormuz: 1 missing, 11 injured."),
    (illu_summit, "2  ASIA · DIPLOMACY", PURPLE,
     "Xi greets Trump on eve of Trump–Xi–Putin summit",
     "Xi and Putin vowed to \u201clead\u201d a multipolar world; at APEC Xi "
     "urged AI and free-trade cooperation. Talks Thursday."),
    (illu_alaska, "3  AMERICAS · US POLITICS", BLUE,
     "Democrat Peltola wins Alaska; Senate now 56–44",
     "AP calls it: 144,302 votes to Sullivan's 131,844. A ninth Democratic "
     "gain, the most in a midterm since 1958, AP says."),
]

MED2 = [
    (illu_drones, "4  EUROPE · UKRAINE WAR", BLUE,
     "Russia fires 141 drones at Ukraine overnight",
     "Air force: 126 downed. Officials: 5 killed, 15 injured in a day; "
     "power cut to 80+ Rivne settlements."),
    (illu_gaza, "5  MIDDLE EAST · GAZA", RED,
     "Board of Peace warns UN the Gaza truce may collapse",
     "First report to the Security Council, obtained by AP, says Israel "
     "blocked the civil administration."),
    (illu_cyclone, "6  ASIA · DISASTER", PURPLE,
     "Cyclone Akvan strengthens in the Bay of Bengal",
     "IMD: landfall on Andhra Pradesh around Friday. Odisha readies up to "
     "204,070 to evacuate."),
    (illu_uk, "7  EUROPE · ECONOMY", TEAL,
     "UK inflation rises to 3.6%, highest in a year",
     "October CPI up from 3.5% as diesel hits a record high, the ONS says."),
    (illu_sudan, "8  AFRICA · SUDAN WAR", GREEN,
     "Amnesty: RSF drone strikes killed 37 civilians in El Obeid",
     "It says they should be investigated as war crimes; the RSF denies "
     "responsibility."),
]

MED3 = [
    (illu_gta, "9  GLOBAL · CULTURE", GOLD,
     "Grand Theft Auto VI goes on sale after a 13-year wait",
     "Midnight launch starts in New Zealand; Sensor Tower estimates 15m+ "
     "pre-release sales."),
    (illu_antibiotic, "10  EUROPE · HEALTH", BLUE,
     "Europe off track on antibiotic resistance, ECDC warns",
     "Carbapenem-resistant K. pneumoniae bloodstream infections up 72% "
     "since 2019."),
    (illu_cop, "11  GLOBAL · CLIMATE", TEAL,
     "COP31: 75 countries back Türkiye's \u201c35x35\u201d power goal",
     "Electricity 35% of energy use by 2035 (Anadolu). Johan Rockström "
     "warns of 2.8–3°C."),
    (illu_bangladesh, "12  ASIA · LABOUR", PURPLE,
     "Bangladesh garment protests shut at least 55 factories",
     "Tk 30,000 minimum wage sought; Dhaka–Mymensingh highway blocked, "
     "police vehicle torched."),
    (illu_australia, "13  OCEANIA · DIPLOMACY", TEAL,
     "Australia sanctions settler leader Daniella Weiss",
     "Also two others and four groups incl. Nachala, Amana, over West Bank "
     "settlements (Penny Wong)."),
]

PINS = [(1, 48, 26), (2, 114, 22), (3, -150, 64), (4, 32, 49),
        (5, 34.5, 31.5), (6, 88, 18), (7, -1, 52), (8, 30, 13),
        (9, 174, -41), (10, 18, 59), (11, 30, 37), (12, 90, 24),
        (13, 149, -35)]

AM, EU, AF, ME, AS, OC = RED, BLUE, GREEN, ORANGE, PURPLE, TEAL
DOTS = [(47, 25, ME), (35, 32, ME), (13, 52, EU), (10, 51, EU),
        (0, 52, EU), (114, 22, AS), (121, 15, AS), (140, 36, AS),
        (127, 37, AS), (104, 1, AS), (100, 14, AS), (74, 32, AS),
        (73, 34, AS), (102, 3, AS), (135, 35, AS), (0, 51, EU),
        (114, 22, AS), (-160, -21, OC), (172, -42, OC), (151, -34, OC),
        (115, -32, OC), (-76, 45, AM), (-72, -15, AM), (-84, 39, AM),
        (-100, 26, AM), (-118, 34, AM), (-58, -35, AM), (-68, -14, AM),
        (-77, 39, AM), (28, -26, AF), (29, -27, AF), (30, 19, AF)]

ALSO = [
    "Riyadh: coalition downed Houthi missile.",
    "Jerusalem: Knesset picks 9 deputy speakers.",
    "Berlin: coalition to cut power tax, cap fuel.",
    "Germany: accuses Russia of chemical breaches.",
    "Cambridge: \u201chuman\u201d is word of the year.",
    "Shenzhen: Xi, Lee conclude FTA services talks.",
    "Manila: Trump claims deal; Manila: none signed.",
    "Tokyo: Japan posts 6th monthly trade deficit.",
    "Seoul: court acquits Daegu mayor.",
    "Singapore: Princess Aiko's first visit in 20 yrs.",
    "Bangkok: director jailed over collapsed tower.",
    "Lahore: most polluted big city again, AQI 339.",
    "Rawalpindi: Sri Lanka all out for 98 v Pakistan.",
    "Kuala Lumpur: ringgit at five-month low.",
    "Asia markets: Kospi +2%; Nikkei falls.",
    "Oil: Brent falls 1.4% to $91.82.",
    "China: Tencent revenue up 8%, below forecasts.",
    "Cook Islands: Cyclone Xavier hits Category 5.",
    "New Zealand: tsunami advisory lifted.",
    "Sydney: Tame Impala sweeps ARIA Awards.",
    "Australia: Bancroft: team knew of 2018 plot.",
    "Canada: Carney: China trade no worry for Trump.",
    "Peru: M5.9 quake off south coast, no damage.",
    "Cincinnati: USA beat Haiti 2–0, into semis.",
    "Monterrey: Mexico edge Jamaica, set up semi.",
    "Los Angeles: Grimes scores 47; 76ers win 9th.",
    "Buenos Aires: deputies debate Malvinas bill.",
    "Bolivia: 99 bat species recorded in Madidi.",
    "Washington: NSA confirms classified outage.",
    "South Africa: inflation jumps to 5.2%.",
    "Johannesburg: SA Rugby seeks Erasmus ban.",
    "Sudan: archaeologists reach Dongola church.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # eyebrow
    d.text((10, 8), "THE DAY IN WORLD NEWS", font=F_EYE, fill=INK)
    r = "45 STORIES · 6 CONTINENTS · ONE DAY"
    d.text((1014 - d.textlength(r, font=F_EYE), 8), r, font=F_EYE, fill=INK)

    # masthead + colour rule (fit masthead to the page width)
    mast = "Wednesday 18 November 2026"
    msize = 62
    mfont = font("DejaVuSerif-Bold.ttf", msize)
    while d.textlength(mast, font=mfont) > 1000 and msize > 10:
        msize -= 1
        mfont = font("DejaVuSerif-Bold.ttf", msize)
    center(d, W // 2, 26, mast, mfont)
    cols = [RED, ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
    seg = 1004 // len(cols)
    for i, c in enumerate(cols):
        d.rectangle([10 + i * seg, 98, 10 + (i + 1) * seg - 1, 102], fill=c)

    # row 1: three leads
    xs1, ws1 = [10, 347, 684], [329, 329, 330]
    for (illu, tag, col, head, deck), x, w in zip(LEADS, xs1, ws1):
        lead_panel(d, x, 108, w, 240, illu, tag, col, head, deck)

    # rows 2 and 3: five medium panels each
    xs5, ws5 = [10, 212, 414, 616, 818], [194, 194, 194, 194, 196]
    for (illu, tag, col, head, deck), x, w in zip(MED2, xs5, ws5):
        med_panel(d, x, 354, w, 182, illu, tag, col, head, deck)
    for (illu, tag, col, head, deck), x, w in zip(MED3, xs5, ws5):
        med_panel(d, x, 542, w, 182, illu, tag, col, head, deck)

    # bottom left: map
    d.text((10, 730), "WHERE IT HAPPENED", font=F_EYE, fill=RED)
    draw_world_map(d, 14, 754, 378, 172, PINS, DOTS)
    d.rectangle([14, 754, 14 + 378, 754 + 172], outline=BORDER)
    lx = 14
    for col, name in ((AM, "Americas"), (EU, "Europe"), (AF, "Africa"),
                      (ME, "Middle East"), (AS, "Asia"), (OC, "Oceania")):
        d.ellipse([lx, 938, lx + 8, 946], fill=col)
        d.text((lx + 11, 936), name, font=F_TINY, fill=INK)
        lx += 11 + d.textlength(name, font=F_TINY) + 8
    d.text((14, 952), "Numbered pins: stories 1–13  •  dots: briefs 14–45",
           font=F_TINY, fill=MUTED)

    # bottom right: ALSO ON
    d.text((408, 730), "ALSO ON WEDNESDAY 18 NOVEMBER", font=F_EYE, fill=RED)
    for ci, col_x in enumerate((414, 712)):
        for j in range(16):
            idx = ci * 16 + j
            num = 14 + idx
            yy = 754 + j * 13
            d.text((col_x, yy), str(num), font=F_ALSO_B, fill=RED)
            d.text((col_x + 20, yy), ALSO[idx], font=F_ALSO, fill=INK)

    # footer
    foot = ("Every story was reported on Wednesday 18 November 2026; "
            "disputed claims are attributed. Sources: Reuters, AP, AFP, "
            "BBC, Al Jazeera and others. Original drawings.")
    center(d, W // 2, 984, foot, F_FOOT, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
