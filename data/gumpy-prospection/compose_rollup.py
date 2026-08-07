#!/usr/bin/env python3
"""Compose un rollup Gumpy 80x200 cm à partir d'un visuel photobooth généré par IA.

Usage: compose_rollup.py <visuel.png> <sortie.jpg> <bois|alu> [--dpi 150]
"""
import sys
import cairosvg
import qrcode
from PIL import Image, ImageDraw, ImageFont

# ---------- Charte Gumpy (extrapolée des rollups réels) ----------
VERT_FONCE   = (34, 102, 56)     # vert forêt
VERT_VIF     = (106, 190, 74)    # vert lime
TEAL         = (0, 135, 148)     # teal/cyan
NOIR         = (20, 20, 20)
BLANC        = (255, 255, 255)
GRIS_CLAIR   = (245, 245, 242)
FOND_FOOTER  = (30, 45, 55)      # navy/charcoal

# Format rollup : 80 x 200 cm
CM_W, CM_H = 80, 200
DPI = 150
for i, a in enumerate(sys.argv):
    if a == "--dpi":
        DPI = int(sys.argv[i+1])

W = int(CM_W / 2.54 * DPI)   # px
H = int(CM_H / 2.54 * DPI)   # px

def px(cm):
    return int(cm / 2.54 * DPI)

# ---------- Chargement ----------
visuel_path, out_path, variante = sys.argv[1], sys.argv[2], sys.argv[3]

logo_png = "/opt/data/prospecting_mairies/gumpy_logo.png"
cairosvg.svg2png(url="/opt/data/prospecting_mairies/gumpy_logo.svg", write_to=logo_png, output_width=px(14), output_height=px(6.7))
logo = Image.open(logo_png).convert("RGBA")

visuel = Image.open(visuel_path).convert("RGB")
# Recadrage du visuel : ratio 3:4 portrait, centré
v_w, v_h = visuel.size
target_ratio = 0.75  # 3:4 portrait
cur_ratio = v_w / v_h
if cur_ratio > target_ratio:
    nw = int(v_h * target_ratio)
    x0 = (v_w - nw) // 2
    visuel = visuel.crop((x0, 0, x0 + nw, v_h))
else:
    nh = int(v_w / target_ratio)
    y0 = (v_h - nh) // 2
    visuel = visuel.crop((0, y0, v_w, y0 + nh))
visuel = visuel.resize((px(36), px(48)), Image.LANCZOS)

# ---------- Polices ----------
def font(size_px, bold=True):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size_px)
    except Exception:
        return ImageFont.load_default()

F_H1   = font(px(4.2))     # accroche
F_H2   = font(px(3.0))     # sous-titres
F_BODY = font(px(2.2), bold=False)
F_SM   = font(px(1.8), bold=False)
F_SLOG = font(px(2.6))

# ---------- Canvas ----------
canvas = Image.new("RGB", (W, H), BLANC)
d = ImageDraw.Draw(canvas)

# Dégradé doux du haut (crème → blanc)
grad = Image.new("RGB", (1, H), BLANC)
for y in range(H):
    t = y / H
    c = tuple(int(GRIS_CLAIR[i] + (BLANC[i] - GRIS_CLAIR[i]) * min(1, t * 3)) for i in range(3))
    grad.putpixel((0, y), c)
grad = grad.resize((W, H))
canvas.paste(grad, (0, 0))

# ---------- 1. HEADER : logo + accroche ----------
logo_w, logo_h = logo.size
logo_x = (W - logo_w) // 2
logo_y = px(4.5)
canvas.paste(logo, (logo_x, logo_y), logo)

# Pin + accroche
pin_r = px(0.55)
pin_x = W // 2 - px(12)
pin_y = px(12.5)
d.ellipse([pin_x - pin_r, pin_y - pin_r, pin_x + pin_r, pin_y + pin_r], fill=VERT_FONCE)
d.polygon([(pin_x - pin_r, pin_y + pin_r), (pin_x + pin_r, pin_y + pin_r), (pin_x, pin_y + pin_r * 2.6)], fill=VERT_FONCE)

h1 = "Trouvez votre PhotoBox ici !"
tx = W // 2 - px(12) + px(0.6)
ty = px(14.5)
d.text((tx, ty), "Trouvez votre ", font=F_H1, fill=NOIR)
w1 = d.textbbox((0, 0), "Trouvez votre ", font=F_H1)[2]
d.text((tx + w1, ty), "PhotoBox ici !", font=F_H1, fill=TEAL)

# ---------- 2. Flèche dégradée ----------
arrow_w = px(3.4)
arrow_h = px(6.0)
arrow_x = W // 2 - arrow_w // 2
arrow_y = px(20)
d.polygon([(W // 2 - px(2.2), arrow_y + arrow_h), (W // 2 + px(2.2), arrow_y + arrow_h), (W // 2, arrow_y + arrow_h + px(2.4))], fill=VERT_VIF)
for i in range(arrow_w):
    t = i / arrow_w
    c = tuple(int(VERT_VIF[k] + (TEAL[k] - VERT_VIF[k]) * t) for k in range(3))
    d.rectangle([arrow_x + i, arrow_y, arrow_x + i + 1, arrow_y + arrow_h], fill=c)

# ---------- 3. Visuel photobooth dans un cadre ----------
frame_w, frame_h = px(42), px(55)
frame_x = W // 2 - frame_w // 2
frame_y = px(27.5)
d.rounded_rectangle([frame_x - px(0.25), frame_y - px(0.25), frame_x + frame_w + px(0.25), frame_y + frame_h + px(0.25)], radius=px(1.2), fill=(230, 230, 228))
v_x = frame_x + (frame_w - visuel.size[0]) // 2
v_y = frame_y + (frame_h - visuel.size[1]) // 2
canvas.paste(visuel, (v_x, v_y))

# ---------- 4. Bénéfices ----------
benefits = [
    ("Une expérience fun & premium", TEAL),
    ("Des souvenirs instantanés", TEAL),
    ("Partagez, imprimez, profitez !", (255, 152, 0)),
]
by = frame_y + frame_h + px(2.5)
for i, (txt, col) in enumerate(benefits):
    ic_y = by + i * px(2.6)
    r = px(0.85)
    cx = W // 2 - px(12)
    d.ellipse([cx - r, ic_y - r, cx + r, ic_y + r], fill=col)
    tb = d.textbbox((0, 0), txt, font=F_BODY)
    d.text((cx + px(2.2), ic_y - (tb[3] - tb[1]) // 2), txt, font=F_BODY, fill=NOIR)

# ---------- 5. Footer : QR + slogan + coordonnées ----------
footer_h = px(30)
footer_y = H - footer_h
d.rectangle([0, footer_y, W, H], fill=FOND_FOOTER)

qr = qrcode.QRCode(box_size=12, border=2)
qr.add_data("https://gumpy.fr")
qr.make(fit=True)
qr_img = qr.make_image(fill_color="white", back_color=FOND_FOOTER).convert("RGBA")
qr_px = px(11)
qr_img = qr_img.resize((qr_px, qr_px), Image.NEAREST)
qr_x = W // 2 - qr_px - px(8)
qr_y = footer_y + px(3)
canvas.paste(qr_img, (qr_x, qr_y), qr_img)

d.text((qr_x, qr_y + qr_px + px(0.6)), "Scannez-moi ou rendez-vous", font=F_SM, fill=(200, 210, 215))
d.text((qr_x, qr_y + qr_px + px(2.2)), "sur gumpy.fr", font=F_SM, fill=(200, 210, 215))

slog = "Souriez, on s'occupe du reste."
sb = d.textbbox((0, 0), slog, font=F_SLOG)
d.text((qr_x + qr_px + px(6), qr_y + qr_px // 2 - (sb[3] - sb[1]) // 2), slog, font=F_SLOG, fill=BLANC)

d.rectangle([0, H - px(6), W, H], fill=(255, 255, 255))
d.text((px(3), H - px(4.2)), "gumpy.fr", font=F_SM, fill=NOIR)
foot_r = "gumpy.fr  ·  @gumpy.photo"
fb = d.textbbox((0, 0), foot_r, font=F_SM)
d.text((W - px(3) - (fb[2] - fb[0]), H - px(4.2)), foot_r, font=F_SM, fill=NOIR)

# ---------- Sauvegarde ----------
canvas.save(out_path, "JPEG", quality=95)
print(f"OK {out_path}  {W}x{H}px  ({DPI} DPI = {CM_W}x{CM_H} cm)")
