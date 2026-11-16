"""Generates docs/readme/diagram.png – hardware overview with product photos.

Usage (from the project root, needs Pillow: pip install pillow):
    python docs/readme/diagram.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
IMG  = HERE / "img"
OUT  = HERE / "diagram.png"

S    = 2                     # render at 2x and downscale – smooth lines and text
W, H = 1600, 1180

TEXT, MUTED, BORDER, CARD = "#1f2328", "#59636e", "#d0d7de", "#ffffff"
LINK = {                     # connection type -> colour
    "USB":         "#59636e",
    "audio":       "#1f2328",
    "Wi-Fi / LAN": "#0969da",
    "LoRaWAN":     "#bc4c00",
    "Zigbee":      "#1a7f37",
    "internet":    "#8250df",
    "API":         "#bf3989",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["segoeuib.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else \
            ["segoeui.ttf", "DejaVuSans.ttf", "Arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size * S)
        except OSError:
            pass
    return ImageFont.load_default(size * S)


F_TITLE, F_NAME, F_SUB = font(26, True), font(22, True), font(20)
F_HEAD, F_LABEL        = font(22, True), font(18)

canvas = Image.new("RGB", (W * S, H * S), "white")
d      = ImageDraw.Draw(canvas)


def s(v: float) -> int:
    return round(v * S)


def wrap(text: str, f, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if d.textlength(test, font=f) <= s(width) or not line:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


def line_h(f) -> int:
    return round(f.size * 1.3) // S


def card(x, y, w, h, title, subtitle=None, photo=None, accent=BORDER):
    d.rounded_rectangle([s(x), s(y), s(x + w), s(y + h)], radius=s(14), fill=CARD, outline=accent, width=s(2))
    lines = [(t, F_TITLE, TEXT) for t in title.split("\n")]      # "\n" forces a line break
    for part in (subtitle.split("\n") if subtitle else []):      # "\n" forces a line break
        lines += [(l, F_SUB, MUTED) for l in wrap(part, F_SUB, w - 24)]
    text_h = sum(line_h(f) for _, f, _ in lines)
    if photo:
        im = Image.open(IMG / photo).convert("RGB")
        aw, ah = s(w - 40), s(h - text_h - 36)                 # photo area
        k = min(aw / im.width, ah / im.height)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        canvas.paste(im, (s(x + w / 2) - im.width // 2, s(y + 14) + (ah - im.height) // 2))
        ty = y + h - text_h - 12
    else:
        ty = y + (h - text_h) / 2
    for text, f, color in lines:
        d.text((s(x + w / 2), s(ty)), text, font=f, fill=color, anchor="mt")
        ty += line_h(f)


def logo(name, cx, cy, h):
    # transparent PNG, scaled to height h and centred on (cx, cy)
    im = Image.open(IMG / name).convert("RGBA")
    k  = s(h) / im.height
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    canvas.paste(im, (s(cx) - im.width // 2, s(cy) - im.height // 2), im)
    return im.width / S


def arrow_head(p_from, p_to, color):
    (x1, y1), (x2, y2) = p_from, p_to
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    size = s(13)
    base = (x2 - ux * size, y2 - uy * size)
    d.polygon([(x2, y2), (base[0] - uy * size * 0.55, base[1] + ux * size * 0.55),
               (base[0] + uy * size * 0.55, base[1] - ux * size * 0.55)], fill=color)


def link(points, kind, label=None, at=None, start=False, end=True, plain=False):
    # plain=True: label as bare text above the line (for short links with no room for a pill)
    color = LINK[kind]
    pts = [(s(x), s(y)) for x, y in points]
    d.line(pts, fill=color, width=s(3), joint="curve")
    if end:
        arrow_head(pts[-2], pts[-1], color)
    if start:
        arrow_head(pts[1], pts[0], color)
    if label and plain:
        cx, cy = at or ((points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2)
        d.text((s(cx), s(cy - 6)), label, font=F_LABEL, fill=color, anchor="mb")
    elif label:
        cx, cy = at or ((points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2)
        tw = d.textlength(label, font=F_LABEL) / S
        d.rounded_rectangle([s(cx - tw / 2 - 8), s(cy - 13), s(cx + tw / 2 + 8), s(cy + 13)],
                            radius=s(13), fill="white", outline=color, width=s(2))
        d.text((s(cx), s(cy)), label, font=F_LABEL, fill=color, anchor="mm")


# --- layout -------------------------------------------------------------------
LX, GX, CX, RX = 40, 425, 740, 1280      # columns: inputs, gateway, centre, actuators
LW, GW, CW, RW = 280, 245, 340, 280
TRUNK = 1180                             # vertical Zigbee line between centre and actuators
ROWS  = [250, 480, 710, 940]             # card tops; cards are 200 high
cy    = [r + 100 for r in ROWS]          # row centre lines
CM    = CX + CW / 2                      # centre column middle

d.text((s(LX + LW / 2), s(205)), "WEJŚCIA", font=F_HEAD, fill=MUTED, anchor="mt")
d.text((s(RX + RW / 2), s(205)), "URZĄDZENIA WYKONAWCZE", font=F_HEAD, fill=MUTED, anchor="mt")

# inputs
card(LX, ROWS[0], LW, 200, "Mikrofon",  "ReSpeaker USB Mic Array",   "respeaker.jpg")
card(LX, ROWS[1], LW, 200, "Kamera",    "TP-Link Tapo C210",         "tapo.jpg")
card(LX, ROWS[3] - 40, LW, 240, "Czujnik temperatury\ni wilgotności", "Milesight EM320-TH", "milesight.jpg")
card(GX, ROWS[2], GW, 200, "Bramka LoRaWAN", "SenseCAP M2",          "sensecap.jpg")

# centre
CLX, CLW = CX - 160, CW + 320                    # cloud box: wider than the centre column
d.rounded_rectangle([s(CLX), s(24), s(CLX + CLW), s(196)], radius=s(14), fill=CARD,
                    outline=LINK["internet"], width=s(2))
d.text((s(CLX + CLW / 2), s(34)), "Chmura", font=F_TITLE, fill=TEXT, anchor="mt")
for fx, file, name, sub in [(0.3, "logo-claude.png",     "Claude",     "model językowy"),
                            (0.7, "logo-elevenlabs.png", "ElevenLabs", "Scribe (STT) · TTS")]:
    x = CLX + CLW * fx
    logo(file, x, 96, 46)
    d.text((s(x), s(126)), name, font=F_NAME, fill=TEXT,  anchor="mt")
    d.text((s(x), s(154)), sub,  font=F_SUB,  fill=MUTED, anchor="mt")

card(CX, ROWS[0], CW, 430, "Raspberry Pi 5", "wake word · agent LangGraph\nharmonogram zadań",
     "rpi-case.jpg", accent=TEXT)

HY = ROWS[2] + 50                                  # Home Assistant: logo + name in one line
d.rounded_rectangle([s(CX), s(HY), s(CX + CW), s(HY + 100)], radius=s(14), fill=CARD, outline=TEXT, width=s(2))
title_w = d.textlength("Home Assistant", font=F_TITLE) / S
x0 = CM - (58 + 14 + title_w) / 2
logo("logo-ha.png", x0 + 29, HY + 50, 56)
d.text((s(x0 + 58 + 14), s(HY + 50)), "Home Assistant", font=F_TITLE, fill=TEXT, anchor="lm")
card(CX, ROWS[3], CW, 200, "Koordynator Zigbee", "Sonoff Dongle Plus MG24", "mg24.jpg")

# actuators
card(RX, ROWS[0], RW, 200, "Głośnik",   "Creative Pebble V2",        "pebble.jpg")
card(RX, ROWS[1], RW, 200, "Adapter żarówki", "LoraTap Zigbee E27",  "loratap.jpg")
card(RX, ROWS[2], RW, 200, "Głowica grzejnika", "Tuya Zigbee",       "tuya.jpg")
card(RX, ROWS[3], RW, 200, "Przycisk",  "Sonoff SNZB-01P",           "snzb01p.jpg")

# links: inputs -> centre
link([(LX + LW, cy[0]), (CX, cy[0])], "USB",         "USB")
link([(LX + LW, cy[1]), (CX, cy[1])], "Wi-Fi / LAN", "Wi-Fi · ONVIF")
GM = GX + GW / 2                         # sensor (bottom-left) -> up into the gateway
link([(LX + LW, cy[3]), (GM, cy[3]), (GM, ROWS[2] + 200)], "LoRaWAN", "LoRaWAN",
     at=((LX + LW + GM) / 2, cy[3]))
link([(GX + GW, cy[2]), (CX, cy[2])], "Wi-Fi / LAN", "LAN",     plain=True)

# links: inside the centre column
link([(CM, 196), (CM, ROWS[0])],                 "internet", "internet", at=(CM + 62, 223), start=True)
link([(CM, ROWS[2] + 50), (CM, ROWS[0] + 430)],  "API", "narzędzia agenta", start=True)
link([(CM, ROWS[3]), (CM, ROWS[2] + 150)],       "USB", "USB", start=True)

# links: centre -> actuators
link([(CX + CW, cy[0]), (RX, cy[0])], "audio", "jack 3,5 mm")
link([(CX + CW, cy[3]), (RX, cy[3])], "Zigbee", start=True, end=False)
link([(TRUNK, cy[3]), (TRUNK, cy[1])], "Zigbee", end=False)
link([(TRUNK, cy[1]), (RX, cy[1])],   "Zigbee")
link([(TRUNK, cy[2]), (RX, cy[2])],   "Zigbee")
d.rounded_rectangle([s(TRUNK - 38), s(cy[1] + 102), s(TRUNK + 38), s(cy[1] + 128)], radius=s(13),
                    fill="white", outline=LINK["Zigbee"], width=s(2))
d.text((s(TRUNK), s(cy[1] + 115)), "Zigbee", font=F_LABEL, fill=LINK["Zigbee"], anchor="mm")

canvas.resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
print(f"saved {OUT}")
