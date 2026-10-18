import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_favicons():
    coo = Image.open('cooeducar_perfect_circle.png').convert('RGBA')
    
    # 1. Favicon 32x32 & 16x16
    fav32 = coo.resize((32, 32), Image.Resampling.LANCZOS)
    fav32.save('favicon-32x32.png')
    fav32.save('favicon.png')
    
    fav16 = coo.resize((16, 16), Image.Resampling.LANCZOS)
    fav16.save('favicon-16x16.png')
    
    # 2. Apple touch icon 180x180 (centered on crisp transparent or white with breathing room)
    apple = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
    coo_apple = coo.resize((156, 156), Image.Resampling.LANCZOS)
    apple.paste(coo_apple, (12, 12), coo_apple)
    apple.save('apple-touch-icon.png')
    
    # 3. Favicon.ico
    fav48 = coo.resize((48, 48), Image.Resampling.LANCZOS)
    coo.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("Favicons generated successfully!")

def make_og_image():
    W, H = 1200, 630
    img = Image.new('RGBA', (W, H), (7, 21, 59, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(H):
        ratio = y / H
        r = int(9 * (1 - ratio) + 15 * ratio)
        g = int(24 * (1 - ratio) + 48 * ratio)
        b = int(66 * (1 - ratio) + 110 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Ambient glows
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([850, -50, 1300, 350], fill=(40, 155, 214, 55))
    g_draw.ellipse([-80, 360, 380, 780], fill=(183, 28, 43, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)
    
    # Glassmorphism outer card
    card_x0, card_y0 = 40, 35
    card_x1, card_y1 = 1160, 595
    card_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_overlay)
    c_draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=28, fill=(255, 255, 255, 16), outline=(255, 255, 255, 50), width=2)
    img = Image.alpha_composite(img, card_overlay)
    draw = ImageDraw.Draw(img)
    
    # White container for logos
    capsule_w, capsule_h = 620, 105
    capsule = Image.new('RGBA', (capsule_w, capsule_h), (255, 255, 255, 245))
    mask = Image.new('L', (capsule_w, capsule_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, capsule_w, capsule_h], radius=20, fill=255)
    
    coo = Image.open('cooeducar_perfect_circle.png').convert('RGBA')
    obli = Image.open('extracted_Logo_OBLI.png').convert('RGBA')
    seleta = Image.open('extracted_Logo_Seleta_Educa__o.png').convert('RGBA')
    
    target_h = 82
    coo_res = coo.resize((target_h, target_h), Image.Resampling.LANCZOS)
    obli_res = obli.resize((int(obli.width * target_h / obli.height), target_h), Image.Resampling.LANCZOS)
    seleta_h = 58
    seleta_res = seleta.resize((int(seleta.width * seleta_h / seleta.height), seleta_h), Image.Resampling.LANCZOS)
    
    capsule.paste(coo_res, (40, (capsule_h - coo_res.height)//2), coo_res)
    capsule.paste(obli_res, (175, (capsule_h - obli_res.height)//2), obli_res)
    capsule.paste(seleta_res, (315, (capsule_h - seleta_res.height)//2), seleta_res)
    
    cap_x = (W - capsule_w) // 2
    cap_y = 65
    img.paste(capsule, (cap_x, cap_y), mask)
    
    # Fonts
    font_bold_path = "C:/Windows/Fonts/segoeuib.ttf" if os.path.exists("C:/Windows/Fonts/segoeuib.ttf") else "C:/Windows/Fonts/arialbd.ttf"
    font_reg_path = "C:/Windows/Fonts/segoeui.ttf" if os.path.exists("C:/Windows/Fonts/segoeui.ttf") else "C:/Windows/Fonts/arial.ttf"
    
    f_tag = ImageFont.truetype(font_bold_path, 17)
    f_title = ImageFont.truetype(font_bold_path, 42)
    f_sub = ImageFont.truetype(font_reg_path, 22)
    f_pill_title = ImageFont.truetype(font_bold_path, 16)
    f_pill_sub = ImageFont.truetype(font_reg_path, 14)
    f_url = ImageFont.truetype(font_bold_path, 17)
    
    # Institution Badge/Tag
    tag_text = "COOEDUCAR • COOPERATIVA EDUCACIONAL DE CARLOS CHAGAS"
    tb = draw.textbbox((0, 0), tag_text, font=f_tag)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 195), tag_text, fill=(245, 158, 11), font=f_tag)
    
    # Main Title
    title_text = "OBLI 2024.2 • Relatório Oficial de Resultados"
    tb = draw.textbbox((0, 0), title_text, font=f_title)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 230), title_text, fill=(255, 255, 255), font=f_title)
    
    # Subtitle
    sub_text = "Portal Interativo • Reading (20 pts) & Listening (10 pts)"
    sb = draw.textbbox((0, 0), sub_text, font=f_sub)
    sw = sb[2] - sb[0]
    draw.text(((W - sw) // 2, 290), sub_text, fill=(226, 232, 240), font=f_sub)
    
    # 4 Cards
    cards = [
        ("78 ALUNOS", "70 presentes (89.7%)"),
        ("7 SALAS", "6º Fund. ao 3º Médio"),
        ("RAIO-X DO ALUNO", "Diagnóstico Individual"),
        ("PÓDIOS & ITENS", "30 Questões Avaliadas")
    ]
    
    card_w = 236
    card_h = 76
    c_gap = 18
    total_w = len(cards) * card_w + (len(cards) - 1) * c_gap
    c_start_x = (W - total_w) // 2
    c_y = 350
    
    for i, (title, subtitle) in enumerate(cards):
        cx0 = c_start_x + i * (card_w + c_gap)
        cy0 = c_y
        cx1 = cx0 + card_w
        cy1 = cy0 + card_h
        
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=14, fill=(13, 27, 68, 235), outline=(56, 189, 248, 130), width=2)
        draw.rounded_rectangle([cx0 + 15, cy0, cx1 - 15, cy0 + 3], radius=2, fill=(40, 155, 214, 255))
        
        t_box = draw.textbbox((0, 0), title, font=f_pill_title)
        tw = t_box[2] - t_box[0]
        draw.text((cx0 + (card_w - tw) // 2, cy0 + 16), title, fill=(255, 255, 255), font=f_pill_title)
        
        s_box = draw.textbbox((0, 0), subtitle, font=f_pill_sub)
        sw = s_box[2] - s_box[0]
        draw.text((cx0 + (card_w - sw) // 2, cy0 + 44), subtitle, fill=(148, 163, 184), font=f_pill_sub)
        
    # URL Pill at Bottom
    url_w, url_h = 440, 48
    url_x0 = (W - url_w) // 2
    url_y0 = 485
    draw.rounded_rectangle([url_x0, url_y0, url_x0 + url_w, url_y0 + url_h], radius=24, fill=(40, 155, 214, 240), outline=(255, 255, 255, 120), width=2)
    
    url_str = "obli-cooeducar-2024.vercel.app"
    ub = draw.textbbox((0, 0), url_str, font=f_url)
    uw = ub[2] - ub[0]
    draw.text((url_x0 + (url_w - uw) // 2, url_y0 + 12), url_str, fill=(255, 255, 255), font=f_url)
    
    final = img.convert('RGB')
    final.save('og-image.png', optimize=True, quality=92)
    print("New polished og-image.png generated! Size:", os.path.getsize('og-image.png'))

make_favicons()
make_og_image()
