import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_og_image():
    W, H = 1200, 630

    # 1. Base texture background
    try:
        bg = Image.open('assets/texture-bg.webp').convert('RGBA')
        target_ratio = W / H
        bg_ratio = bg.width / bg.height
        if bg_ratio > target_ratio:
            new_w = int(bg.height * target_ratio)
            left = (bg.width - new_w) // 2
            bg = bg.crop((left, 0, left + new_w, bg.height))
        else:
            new_h = int(bg.width / target_ratio)
            top = (bg.height - new_h) // 2
            bg = bg.crop((0, top, bg.width, top + new_h))
        base = bg.resize((W, H), Image.Resampling.LANCZOS)
    except Exception as e:
        print('Texture note:', e)
        base = Image.new('RGBA', (W, H), (247, 239, 219, 255))

    # Soft glowing radial gradients
    vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    v_draw.ellipse([640, 40, 1180, 580], fill=(255, 248, 225, 180))
    v_draw.ellipse([40, 50, 680, 580], fill=(255, 252, 244, 230))
    vignette = vignette.filter(ImageFilter.GaussianBlur(40))
    base = Image.alpha_composite(base, vignette)

    # 2. Ornate Double Gold & Maroon Royal Borders
    border_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border_layer)
    gold_outer = (185, 138, 47, 230)   # #b98a2f
    gold_inner = (217, 179, 106, 170)  # #d9b36a
    maroon_accent = (140, 35, 35, 230) # #8c2323

    b_draw.rectangle([22, 22, W - 22, H - 22], outline=gold_outer, width=2)
    b_draw.rectangle([30, 30, W - 30, H - 30], outline=gold_inner, width=1)

    for cx, cy in [(22, 22), (W - 22, 22), (22, H - 22), (W - 22, H - 22)]:
        b_draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=gold_outer)
        b_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=maroon_accent)

    for cx, cy in [(30, 30), (W - 30, 30), (30, H - 30), (W - 30, H - 30)]:
        b_draw.polygon([(cx, cy - 3), (cx + 3, cy), (cx, cy + 3), (cx - 3, cy)], fill=gold_outer)

    base = Image.alpha_composite(base, border_layer)

    # 3. Mandap & Couple on the Right Side
    right_cx = 890
    try:
        mandap_raw = Image.open('editable/assets/mandap-footer.webp').convert('RGBA')
        m_bbox = mandap_raw.getbbox()
        if m_bbox:
            mandap_raw = mandap_raw.crop(m_bbox)
        m_h = 555
        m_w = int(m_h * (mandap_raw.width / mandap_raw.height))
        mandap = mandap_raw.resize((m_w, m_h), Image.Resampling.LANCZOS)

        m_x = right_cx - m_w // 2
        m_y = H - m_h - 22

        m_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ms_draw = ImageDraw.Draw(m_shadow)
        ms_draw.ellipse([m_x + 30, H - 48, m_x + m_w - 30, H - 18], fill=(61, 43, 31, 80))
        m_shadow = m_shadow.filter(ImageFilter.GaussianBlur(14))
        base = Image.alpha_composite(base, m_shadow)

        base.paste(mandap, (m_x, m_y), mandap)
    except Exception as e:
        print('Mandap error:', e)

    try:
        couple_raw = Image.open('editable/assets/couple.webp').convert('RGBA')
        c_bbox = couple_raw.getbbox()
        if c_bbox:
            couple_raw = couple_raw.crop(c_bbox)
        c_h = 425
        c_w = int(c_h * (couple_raw.width / couple_raw.height))
        couple = couple_raw.resize((c_w, c_h), Image.Resampling.LANCZOS)

        c_x = right_cx - c_w // 2
        c_y = H - c_h - 28

        c_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(c_shadow)
        cs_draw.ellipse([c_x + 20, H - 40, c_x + c_w - 20, H - 18], fill=(61, 43, 31, 110))
        c_shadow = c_shadow.filter(ImageFilter.GaussianBlur(10))
        base = Image.alpha_composite(base, c_shadow)

        base.paste(couple, (c_x, c_y), couple)
    except Exception as e:
        print('Couple error:', e)

    # 4. Top Garland
    try:
        garland_raw = Image.open('editable/assets/garland-top.webp').convert('RGBA')
        top_h = int(garland_raw.height * 0.085)
        toran = garland_raw.crop((0, 0, garland_raw.width, top_h))
        t_w = W - 48
        t_h = int(t_w * (toran.height / toran.width))
        toran_resized = toran.resize((t_w, t_h), Image.Resampling.LANCZOS)

        g_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        g_layer.paste(toran_resized, (24, 24), toran_resized)
        base = Image.alpha_composite(base, g_layer)
    except Exception as e:
        print('Garland error:', e)

    # 5. Left Typography & Content
    draw = ImageDraw.Draw(base)

    f_shloka = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 16)
    f_eyebrow = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 12)
    f_name = ImageFont.truetype('C:/Windows/Fonts/palab.ttf', 52)
    f_weds = ImageFont.truetype('C:/Windows/Fonts/palabi.ttf', 28)
    f_date_hdr = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 13)
    f_date_time = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 17)
    f_venue_title = ImageFont.truetype('C:/Windows/Fonts/palab.ttf', 15)
    f_venue_sub = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 12)
    f_tag = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 12)

    c_maroon = (123, 30, 30, 255)       # #7b1e1e
    c_gold = (154, 107, 31, 255)        # #9a6b1f
    c_gold_bright = (185, 138, 47, 255) # #b98a2f
    c_dark = (61, 43, 31, 255)          # #3d2b1f
    c_muted = (107, 84, 58, 255)        # #6b543a

    left_cx = 345

    def draw_centered(y, text, font, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text((left_cx - w // 2, y), text, fill=color, font=font)

    draw_centered(104, "॥  శ్రీ  మ హాగ ణాధి ప త యే  న మః  ॥", f_shloka, c_maroon)
    draw_centered(132, "S H U B H A   M U H U R T H A M", f_eyebrow, c_gold)

    div_y = 154
    draw.line([left_cx - 95, div_y, left_cx + 95, div_y], fill=(185, 138, 47, 180), width=1)
    draw.polygon([(left_cx, div_y - 4), (left_cx + 5, div_y), (left_cx, div_y + 4), (left_cx - 5, div_y)], fill=c_maroon)

    draw_centered(168, "Maruthi", f_name, c_maroon)
    draw_centered(224, "—  weds  —", f_weds, c_gold_bright)
    draw_centered(260, "Vinod", f_name, c_maroon)

    div_y2 = 330
    draw.line([left_cx - 95, div_y2, left_cx + 95, div_y2], fill=(185, 138, 47, 180), width=1)
    draw.polygon([(left_cx, div_y2 - 4), (left_cx + 5, div_y2), (left_cx, div_y2 + 4), (left_cx - 5, div_y2)], fill=c_maroon)

    card_y = 348
    c_box = [left_cx - 265, card_y, left_cx + 265, card_y + 84]
    draw.rounded_rectangle(c_box, radius=12, fill=(255, 252, 246, 245), outline=(217, 179, 106, 200), width=1)
    draw.rounded_rectangle([c_box[0], c_box[1], c_box[0] + 6, c_box[3]], radius=3, fill=c_maroon)

    draw.text((c_box[0] + 18, card_y + 12), "WEDNESDAY, 25TH NOVEMBER 2026", fill=c_gold, font=f_date_hdr)
    draw.text((c_box[0] + 18, card_y + 34), "Muhurtham at 8:38 PM sharp", fill=c_maroon, font=f_date_time)
    draw.text((c_box[0] + 18, card_y + 59), "Auspicious Shubha Muhurtham Ceremony", fill=c_muted, font=f_venue_sub)

    vcard_y = 444
    v_box = [left_cx - 265, vcard_y, left_cx + 265, vcard_y + 88]
    draw.rounded_rectangle(v_box, radius=12, fill=(255, 252, 246, 245), outline=(217, 179, 106, 200), width=1)
    draw.rounded_rectangle([v_box[0], v_box[1], v_box[0] + 6, v_box[3]], radius=3, fill=c_gold)

    draw.text((v_box[0] + 18, vcard_y + 11), "VENUE", fill=c_maroon, font=f_date_hdr)
    draw.text((v_box[0] + 18, vcard_y + 30), "Sri Lakshmi AC Convention Hall", fill=c_dark, font=f_venue_title)
    draw.text((v_box[0] + 18, vcard_y + 51), "Karmanghat Rd, opp. Indra Nagendra Theater, Saroornagar", fill=c_muted, font=f_venue_sub)
    draw.text((v_box[0] + 18, vcard_y + 68), "Hyderabad, Telangana — 500035", fill=c_muted, font=f_venue_sub)

    tag_text = "•   #MARUTHIWEDSVINOD   •   INVITESTORY.IN   •"
    draw_centered(552, tag_text, f_tag, c_maroon)

    os.makedirs('assets', exist_ok=True)
    rgb = base.convert('RGB')
    rgb.save('assets/og-image.jpg', 'JPEG', quality=95, optimize=True, progressive=True)
    base.save('assets/og-image.png', 'PNG', optimize=True)
    rgb.save('og-image.jpg', 'JPEG', quality=95, optimize=True, progressive=True)
    rgb.save('editable/assets/og-image.jpg', 'JPEG', quality=95, optimize=True, progressive=True)

    print("Created OG image!")

def create_og_logo():
    S = 512
    logo = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    cx, cy = S // 2, S // 2

    r_outer = 244
    r_inner = 236
    r_gold = 224

    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(255, 252, 245, 255), outline=(185, 138, 47, 240), width=4)
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=None, outline=(140, 35, 35, 180), width=2)
    draw.ellipse([cx - r_gold, cy - r_gold, cx + r_gold, cy + r_gold], fill=None, outline=(217, 179, 106, 180), width=1)

    try:
        g = Image.open('editable/assets/garland-top.webp').convert('RGBA')
        top_g = g.crop((0, 0, g.width, int(g.height * 0.16)))
        t_w = 260
        t_h = int(t_w * top_g.height / top_g.width)
        top_g = top_g.resize((t_w, t_h), Image.Resampling.LANCZOS)
        logo.paste(top_g, (cx - t_w // 2, 48), top_g)
    except Exception as e:
        print('Garland note:', e)

    f_initials = ImageFont.truetype('C:/Windows/Fonts/palab.ttf', 124)
    f_amp = ImageFont.truetype('C:/Windows/Fonts/palabi.ttf', 82)
    f_names = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 20)
    f_date = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 15)

    c_ruby = (123, 30, 30, 255)   # #7b1e1e
    c_gold = (185, 138, 47, 255)  # #b98a2f
    c_dark = (61, 43, 31, 255)    # #3d2b1f

    bbox_m = draw.textbbox((0, 0), 'M', font=f_initials)
    bbox_amp = draw.textbbox((0, 0), '&', font=f_amp)
    bbox_v = draw.textbbox((0, 0), 'V', font=f_initials)

    w_m = bbox_m[2] - bbox_m[0]
    w_amp = bbox_amp[2] - bbox_amp[0]
    w_v = bbox_v[2] - bbox_v[0]

    gap = 12
    total_w = w_m + gap + w_amp + gap + w_v
    start_x = (S - total_w) // 2

    target_top = 168
    y_m = target_top - bbox_m[1]
    y_v = target_top - bbox_v[1]
    cap_h = bbox_m[3] - bbox_m[1]
    amp_h = bbox_amp[3] - bbox_amp[1]
    y_amp = target_top + (cap_h - amp_h) // 2 - bbox_amp[1]

    x_m = start_x
    x_amp = x_m + w_m + gap
    x_v = x_amp + w_amp + gap

    draw.text((x_m, y_m), 'M', fill=c_ruby, font=f_initials)
    draw.text((x_amp, y_amp), '&', fill=c_gold, font=f_amp)
    draw.text((x_v, y_v), 'V', fill=c_ruby, font=f_initials)

    draw.line([cx - 85, 335, cx + 85, 335], fill=(185, 138, 47, 180), width=1)
    draw.polygon([(cx, 332), (cx + 4, 335), (cx, 338), (cx - 4, 335)], fill=c_ruby)

    def draw_centered_logo(y, text, font, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text((cx - w // 2, y), text, fill=color, font=font)

    draw_centered_logo(355, 'MARUTHI   ·   VINOD', f_names, c_dark)
    draw_centered_logo(395, '·   25  NOVEMBER  2026   ·', f_date, c_gold)

    logo.save('og-logo.png', 'PNG', optimize=True)
    logo.save('assets/og-logo.png', 'PNG', optimize=True)
    logo.save('editable/assets/og-logo.png', 'PNG', optimize=True)
    apple_icon = logo.resize((180, 180), Image.Resampling.LANCZOS)
    apple_icon.save('apple-touch-icon.png', 'PNG', optimize=True)
    apple_icon.save('assets/apple-touch-icon.png', 'PNG', optimize=True)
    logo.save('favicon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

    print("Created OG logo!")

if __name__ == '__main__':
    create_og_image()
    create_og_logo()
