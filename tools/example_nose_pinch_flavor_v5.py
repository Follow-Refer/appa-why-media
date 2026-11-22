"""코 막으니까 딸기 맛이 없어졌어(11/23): 상황(차 뒷자리, 코 막고 젤리 씹는 아이 '딸기 맛이 없어!') →
답(같은 아이 정면. 코를 막으면 입에서 오른 딸기 냄새 방울이 손에 막혀 사라지고 생각 풍선 속 젤리는 하얀 '달기만' →
손을 내리면 냄새 방울이 코로 쏙 들어가고 풍선 속 젤리가 빨간 딸기로 바뀜 '딸기!').
사용: python3 example_nose_pinch_flavor_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146); LP = (230, 140, 160)
HAIR = (120, 96, 82); SHIRT = (176, 206, 232); NOSE = (240, 196, 172)
SEAT = (190, 200, 226); SEAT_D = (170, 180, 210)
BERRY = (236, 120, 130); PALE = (246, 240, 236); PALE_D = (222, 214, 210); LEAF = (140, 190, 150)
SCENT = (244, 150, 168)


def lab(im, text, xy, col, t, t_on, t_off=None):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def face(d, cx, cy, r, t, chew=True):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SKIN)
    d.chord([cx-r-2, cy-r-6, cx+r+2, cy+r*0.30], 180, 360, fill=HAIR)
    ey = cy+r*0.08; er = r*0.10
    for sx in (cx-r*0.38, cx+r*0.38):
        d.ellipse([sx-er*0.8, ey-er, sx+er*0.8, ey+er], fill=INK)
    d.ellipse([cx-r*0.13, cy+r*0.26, cx+r*0.13, cy+r*0.46], fill=NOSE)
    my = cy+r*0.64
    o = (0.5+0.5*math.sin(t*9)) if chew else 0.0   # 오물오물
    d.ellipse([cx-r*0.17, my-r*0.05, cx+r*0.17, my+r*0.05+r*0.10*o], fill=(214, 120, 128))
    d.ellipse([cx-r*0.74, cy+r*0.40, cx-r*0.50, cy+r*0.56], fill=(250, 206, 196))
    d.ellipse([cx+r*0.50, cy+r*0.40, cx+r*0.74, cy+r*0.56], fill=(250, 206, 196))


def body(d, cx, cy, r):
    by = cy+r*0.88
    d.rounded_rectangle([cx-r*1.0, by, cx+r*1.0, by+r*2.4], radius=int(r*0.6), fill=SHIRT)
    return by


def pinch_hand(d, cx, cy, r, down):
    """오른팔(보는 사람 왼쪽) 짧게 굽혀 코를 잡은 손. down 0→1이면 손이 가슴 앞으로 내려감."""
    by = cy+r*0.88
    sh = (cx-r*0.78, by+r*0.30)
    nose = (cx, cy+r*0.36)
    rest = (cx-r*0.35, by+r*0.85)
    hx = nose[0]+(rest[0]-nose[0])*down; hy = nose[1]+(rest[1]-nose[1])*down
    elbow = (cx-r*0.95, by+r*0.95-r*0.25*(1-down))
    d.line([sh, elbow], fill=SHIRT, width=int(r*0.30))
    d.line([elbow, (hx, hy)], fill=SKIN, width=int(r*0.22))
    d.ellipse([hx-r*0.22, hy-r*0.19, hx+r*0.18, hy+r*0.19], fill=SKIN, outline=(226, 190, 164), width=4)
    if down < 0.3:   # 코를 집은 엄지·검지
        d.ellipse([hx+r*0.04, hy-r*0.14, hx+r*0.22, hy+r*0.04], fill=SKIN, outline=(226, 190, 164), width=4)


def jelly(d, x, y, s, k):
    """k=0 하얀 젤리, k=1 빨간 딸기."""
    col = mix(PALE, BERRY, k); line = mix(PALE_D, (214, 96, 110), k)
    pts = []
    for j in range(60):
        a = 2*math.pi*j/60
        rr = s*(1.0-0.22*math.sin(a))          # 아래가 좁은 딸기 모양
        pts.append((x+rr*0.92*math.cos(a), y+rr*1.05*math.sin(a)*(0.85 if math.sin(a) < 0 else 1.15)))
    d.polygon(pts, fill=col, outline=line)
    if k > 0.05:
        seed = mix(col, (250, 236, 170), k)
        for (u, v) in ((-0.35, -0.1), (0.3, -0.15), (0.0, 0.25), (-0.25, 0.5), (0.28, 0.45), (0.0, -0.35)):
            d.ellipse([x+u*s-6, y+v*s-9, x+u*s+6, y+v*s+9], fill=seed)
        lc = mix(PALE, LEAF, k); top = y-s*0.88
        for a in (-1.1, -0.45, 0.45, 1.1, 0.0):
            tx = x+s*0.42*math.sin(a); ty = top-s*0.22*math.cos(a)+s*0.08
            d.polygon([(x-s*0.10, top+s*0.04), (tx, ty-s*0.06), (x+s*0.10, top+s*0.04)], fill=lc)
        d.rounded_rectangle([x-s*0.05, top-s*0.30, x+s*0.05, top], radius=4, fill=lc)


def bubble(d, bx, by, br, hx, hy, k):
    d.ellipse([bx-br, by-br, bx+br, by+br], fill=(255, 255, 255), outline=(220, 214, 232), width=5)
    for j, rr in enumerate((26, 18)):
        x = hx+(bx-hx)*(0.35+0.25*j); y = hy+(by-hy)*(0.35+0.25*j)
        d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(255, 255, 255), outline=(220, 214, 232), width=4)
    jelly(d, bx, by+8, br*0.55, k)


def scent(im, pts):
    """pts: (x, y, alpha) 냄새 방울."""
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for x, y, a, s in pts:
        if a <= 0: continue
        A = int(220*min(1, a))
        ld.ellipse([x-s, y-s, x+s, y+s], fill=SCENT+(A,))
        ld.ellipse([x-s*0.4, y-s*0.6, x, y-s*0.2], fill=(255, 230, 236, A))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def sparkle(d, x, y, s, col):
    for a in range(4):
        aa = a*math.pi/2
        d.line([(x+s*0.25*math.cos(aa), y+s*0.25*math.sin(aa)), (x+s*math.cos(aa), y+s*math.sin(aa))], fill=col, width=6)


# ---------------- 장면 1: 차 뒷자리, 코 막고 젤리 ----------------
S1 = int(3.4*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '딸기 맛이 없어!', font=FBW, fill=TXT, anchor='mm')
    d.rounded_rectangle([90, 200, 990, 1040], radius=80, fill=SEAT)
    d.rounded_rectangle([150, 250, 930, 470], radius=40, fill=(214, 232, 244))
    for k in range(4):
        x = (k*240 - t*160) % 900 + 120
        if 200 < x < 880:
            d.ellipse([x-46, 320, x+46, 410], fill=GREEN); d.rectangle([x-8, 410, x+8, 460], fill=BROWN)
    d.rounded_rectangle([90, 700, 990, 1040], radius=60, fill=SEAT_D)
    cx, cy, r = 430, 640, 150
    body(d, cx, cy, r)
    face(d, cx, cy, r, t)
    pinch_hand(d, cx, cy, r, 0.0)
    hx, hy = cx+r*0.55, cy-r*0.75
    bubble(d, 770, 520, 120, hx, hy, 0.0)
    a = ease((t-1.4)/0.5)
    if a > 0: d.text((770, 520-120-10-a*14), '?', font=FBW, fill=mix(SEAT, LT, a), anchor='mm')
    return im


# ---------------- 장면 2: 코 막음 → 코 열면 ----------------
S2 = int(14.0*F)
CX, CY, CR = 380, 560, 175
BX, BY, BR = 800, 380, 150
T_REL, T_IN, T_MORPH = 4.6, 5.8, 7.4
MOUTH = (CX, CY+CR*0.66); NOSEP = (CX, CY+CR*0.36)


def drops(t):
    pts = []
    for k in range(6):
        ph = (t*0.55+k/6) % 1.0         # 1.8초마다 한 바퀴
        start = t-ph/0.55
        x0 = MOUTH[0]+(k-2.5)*16
        if start < T_REL:
            # 막힌 코: 입에서 오르다 손 아래에서 멈추고 사라짐
            y = MOUTH[1]-ph*CR*0.22; x = x0+math.sin(ph*6+k)*10
            a = (1-ph)*min(1, ph*4)
            if t > T_REL: a *= max(0, 1-(t-T_REL)/0.5)
            pts.append((x, y, a, 16))
        elif start > T_REL+0.6:
            # 열린 코: 입에서 코로 쏙
            yy = MOUTH[1]+(NOSEP[1]-MOUTH[1])*ease(ph/0.7)
            xx = x0+(NOSEP[0]-x0)*ease(ph/0.7)
            a = min(1, ph*4)*(1 if ph < 0.7 else max(0, 1-(ph-0.7)/0.15))
            pts.append((xx, yy, a, 16*(1-0.5*ease(ph/0.7))))
    return pts


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '코를 놓으면?', font=FBW, fill=TXT, anchor='mm')
    down = ease((t-T_REL)/1.0)
    body(d, CX, CY, CR)
    face(d, CX, CY, CR, t)
    scent(im, drops(t)); d = ImageDraw.Draw(im)
    pinch_hand(d, CX, CY, CR, down)
    k = ease((t-T_MORPH)/1.6)
    bubble(d, BX, BY, BR, CX+CR*0.6, CY-CR*0.8, k)
    if t > T_IN+0.6:   # 코가 분홍빛으로 살짝 빛남
        g = 0.6+0.4*math.sin(t*4)
        rr = CR*(0.20+0.03*g)
        d.ellipse([NOSEP[0]-rr, NOSEP[1]-rr*0.85, NOSEP[0]+rr, NOSEP[1]+rr*0.85], outline=mix(SKIN, LP, g), width=6)
    lab(im, '코 막음', (CX-CR*0.15, CY-CR*1.35), LM, t, 0.4, T_REL-0.2)
    lab(im, '달기만', (BX, BY+BR+70), LT, t, 1.6, T_REL-0.2)
    lab(im, '코로 쏙', (CX-CR*0.15, CY-CR*1.35), LP, t, T_IN+0.4)
    lab(im, '딸기!', (BX, BY+BR+70), LG, t, T_MORPH+1.2)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/nose_pinch_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('nosepinch', s1, S1, s2, S2, out,
              preview=[(s1, int(2.2*F), S1), (s2, int(2.8*F), S2), (s2, int(6.6*F), S2), (s2, int(12.0*F), S2)])
