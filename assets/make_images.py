"""Generate og.png (link preview) and bot_avatar.png from the brand shapes.

Run: python assets/make_images.py   (from the qaytar folder)
Replace with your own logo files any time.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NAVY, BLUE, GREEN, BG = (13, 40, 72), (11, 79, 158), (31, 171, 75), (245, 248, 252)
FONTS = "C:/Windows/Fonts/"


def font(name: str, size: int):
    for candidate in (name, "segoeuib.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(FONTS + candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_logo(img: Image.Image, x: int, y: int, s: float):
    """Shield + % + green arrow, drawn on a 64x64 grid scaled by s."""
    d = ImageDraw.Draw(img)
    P = lambda px, py: (x + px * s, y + py * s)  # noqa: E731
    shield = [P(32, 5), P(53, 13), P(53, 30), P(50, 42), P(42, 52), P(32, 59), P(22, 52), P(14, 42), P(11, 30), P(11, 13)]
    d.polygon(shield, fill="white", outline=BLUE, width=int(5 * s))
    for cx, cy in ((25, 24), (39, 38)):
        r = 4.2 * s
        d.ellipse([P(cx, cy)[0] - r, P(cx, cy)[1] - r, P(cx, cy)[0] + r, P(cx, cy)[1] + r], outline=BLUE, width=int(3.4 * s))
    d.line([P(40, 20), P(24, 42)], fill=BLUE, width=int(4 * s))
    # green swoosh (quadratic curve approximation)
    pts = []
    for i in range(41):
        t = i / 40
        bx = (1 - t) ** 3 * 5 + 3 * (1 - t) ** 2 * t * 11 + 3 * (1 - t) * t ** 2 * 38 + t ** 3 * 54
        by = (1 - t) ** 3 * 38 + 3 * (1 - t) ** 2 * t * 55 + 3 * (1 - t) * t ** 2 * 57 + t ** 3 * 34
        pts.append(P(bx, by))
    d.line(pts, fill=GREEN, width=int(5 * s), joint="curve")
    d.polygon([P(47, 29.5), P(61, 27), P(56.5, 40.5)], fill=GREEN)


def og():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    d.ellipse([760, -260, 1460, 440], fill=(226, 244, 233))
    draw_logo(img, 80, 70, 2.2)
    d.text((240, 92), "Qaytar", font=font("segoeuib.ttf", 92), fill=NAVY)
    d.text((80, 260), "Kontraktdan 12% ni", font=font("segoeuib.ttf", 70), fill=NAVY)
    d.text((80, 345), "qaytarib oling", font=font("segoeuib.ttf", 70), fill=GREEN)
    d.text((80, 455), "20 mln kontrakt → 2 400 000 so'm qaytadi", font=font("segoeui.ttf", 36), fill=(60, 76, 98))
    d.rounded_rectangle([80, 520, 520, 584], radius=20, fill=GREEN)
    d.text((108, 532), "t.me/QaytarStartupBot", font=font("segoeuib.ttf", 32), fill="white")
    img.save(ROOT / "site" / "og.png", optimize=True)


def avatar():
    img = Image.new("RGB", (640, 640), BG)
    draw_logo(img, 80, 70, 7.6)
    img.save(ROOT / "assets" / "bot_avatar.png", optimize=True)


if __name__ == "__main__":
    og()
    avatar()
    print("saved site/og.png and assets/bot_avatar.png")
