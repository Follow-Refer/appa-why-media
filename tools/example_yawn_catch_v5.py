"""아빠도 하품했다!(11/8): 상황(잠자리 그림책, 아이 하품 → 아빠도 하품) → 답(아빠 하품이 옆으로 퍼지는데, 아기·두 살은 멀뚱, 네 살·여섯 살은 따라 하암).
사용: python3 example_yawn_catch_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
ROOM_T, ROOM_B = (206, 200, 228), (232, 226, 240)
FLOOR = (214, 204, 186); BED = (246, 226, 214); BLANKET = (196, 214, 236); BLANKET_D = (170, 192, 222)
HAIR = (120, 96, 82); DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 200, 150)
PANTS = (150, 170, 210); MOUTH = (200, 110, 118); BOOK = (246, 214, 140); BOOK_D = (226, 186, 110)
WAVE = (232, 150, 120)


def lab(im, text, xy, col, t, t_on, t_off=None):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def yawn_k(t, t0, dur=2.4):
    """0→1→0 하품 곡선 (입 벌림)."""
    if t < t0 or t > t0+dur: return 0.0
    u = (t-t0)/dur
    if u < 0.35: return ease(u/0.35)
    if u < 0.65: return 1.0
    return 1-ease((u-0.65)/0.35)


def yawn_hold(t, t0):
    """마지막 하품: 열린 채로 멈춤(끝 장면 정지용)."""
    return 0.0 if t < t0 else ease((t-t0)/0.8)


def face(d, cx, cy, r, yk, mood='smile', hair=HAIR, baby=False):
    """둥근 얼굴. yk(0~1) 하품 정도: 눈은 감기고 입은 세로로 크게."""
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SKIN)
    if baby:
        d.arc([cx-r*0.4, cy-r-6, cx+r*0.1, cy-r*0.55], 200, 340, fill=hair, width=max(3, int(r*0.08)))
    else:
        d.chord([cx-r-2, cy-r-6, cx+r+2, cy+r*0.38], 180, 360, fill=hair)
    ex = r*0.38; ey = cy+r*0.08; er = r*0.10
    for sx in (cx-ex, cx+ex):
        if yk > 0.25:   # 감은 눈
            d.arc([sx-er*1.6, ey-er*1.2, sx+er*1.6, ey+er*1.2], 200, 340, fill=INK, width=max(3, int(r*0.07)))
        else:
            d.ellipse([sx-er, ey-er*1.1, sx+er, ey+er*1.1], fill=INK)
    my = cy+r*0.52
    if yk > 0.05:
        mw = r*(0.16+0.10*yk); mh = r*(0.10+0.32*yk)
        d.ellipse([cx-mw, my-mh*0.6, cx+mw, my+mh], fill=MOUTH)
    elif mood == 'wow':
        d.ellipse([cx-r*0.16, my-r*0.06, cx+r*0.16, my+r*0.22], fill=MOUTH)
    elif mood == 'flat':
        d.line([cx-r*0.14, my+r*0.05, cx+r*0.14, my+r*0.05], fill=INK, width=max(3, int(r*0.06)))
    else:
        d.arc([cx-r*0.26, my-r*0.16, cx+r*0.26, my+r*0.16], 20, 160, fill=LIP, width=max(3, int(r*0.07)))
    d.ellipse([cx-r*0.70, cy+r*0.30, cx-r*0.46, cy+r*0.46], fill=(250, 206, 196))
    d.ellipse([cx+r*0.46, cy+r*0.30, cx+r*0.70, cy+r*0.46], fill=(250, 206, 196))


def stander(d, cx, gy, s, yk, shirt, head_r, mood='smile'):
    """서 있는 사람. 팔은 몸 옆에 짧게 붙임."""
    leg = 130*s; torso = 170*s
    hip = gy-leg; sh = hip-torso
    for dx in (-30*s, 30*s):
        d.rounded_rectangle([cx+dx-22*s, hip-10*s, cx+dx+22*s, gy], radius=int(20*s), fill=PANTS)
        d.ellipse([cx+dx-28*s, gy-18*s, cx+dx+28*s, gy+8*s], fill=SKIN)
    d.rounded_rectangle([cx-72*s, sh, cx+72*s, hip+18*s], radius=int(46*s), fill=shirt)
    for dx in (-1, 1):
        x0 = cx+dx*72*s
        d.rounded_rectangle([x0-20*s, sh+18*s, x0+20*s, sh+130*s], radius=int(20*s), fill=shirt)
        d.ellipse([x0-18*s, sh+118*s, x0+18*s, sh+152*s], fill=SKIN)
    hy = sh-head_r+8*s
    face(d, cx, hy, head_r, yk, mood)
    return hy, head_r


def bassinet_baby(d, cx, gy, yk=0.0):
    """누워 있는 아기(바구니 침대). 하품 안 함."""
    d.rounded_rectangle([cx-110, gy-70, cx+110, gy], radius=30, fill=(236, 214, 200))
    d.rectangle([cx-90, gy, cx-80, gy+0], fill=(236, 214, 200))
    d.rounded_rectangle([cx-120, gy-120, cx+120, gy-58], radius=30, fill=(246, 230, 220))
    face(d, cx-40, gy-136, 50, yk, mood='flat', baby=True)
    d.rounded_rectangle([cx-8, gy-150, cx+108, gy-96], radius=26, fill=(250, 214, 200))   # 이불
    return gy-136, 50


# ---------------- 장면 1: 잠자리 그림책 ----------------
S1 = int(4.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((120, 126, 176), (176, 170, 210), yy/H))
    d.text((W/2, 80), '아빠도 하품했다!', font=FBW, fill=(244, 240, 252), anchor='mm')
    # 창밖 달
    d.rounded_rectangle([70, 170, 300, 360], radius=30, fill=(90, 100, 150))
    d.ellipse([200, 200, 270, 270], fill=(250, 236, 180)); d.ellipse([220, 192, 282, 258], fill=(90, 100, 150))
    # 침대 머리판 + 베개
    d.rounded_rectangle([170, 430, 910, 640], radius=40, fill=(214, 190, 160))
    d.rounded_rectangle([220, 520, 480, 610], radius=40, fill=(250, 246, 240))
    d.rounded_rectangle([560, 540, 820, 620], radius=40, fill=(250, 246, 240))
    # 아빠(왼쪽, 큰 몸) / 아이(오른쪽)
    dk = yawn_k(t, 1.7, 2.2); kk = yawn_k(t, 0.4, 2.2)
    # 아빠 몸통
    d.rounded_rectangle([250, 600, 470, 860], radius=70, fill=DAD_SHIRT)
    face(d, 360, 520, 92, dk)
    # 아이 몸통
    d.rounded_rectangle([600, 660, 780, 860], radius=60, fill=KID_SHIRT)
    face(d, 690, 590, 80, kk, mood='wow' if t > 3.9 else 'smile')
    # 그림책: 둘 사이, 펼친 책 + 짧은 손
    bx, by = 540, 760
    d.polygon([(bx-130, by-60), (bx, by-40), (bx, by+60), (bx-130, by+40)], fill=BOOK)
    d.polygon([(bx+130, by-60), (bx, by-40), (bx, by+60), (bx+130, by+40)], fill=(250, 226, 160))
    d.line([bx, by-40, bx, by+60], fill=BOOK_D, width=5)
    for hx, hy in ((bx-140, by), (bx+140, by+4)): d.ellipse([hx-24, hy-24, hx+24, hy+24], fill=SKIN)
    # 이불
    d.rounded_rectangle([140, 800, 940, 1080], radius=60, fill=BLANKET)
    for x in range(200, 900, 140): d.ellipse([x, 860, x+40, 900], fill=BLANKET_D)
    lab(im, '하암~', (690, 400), LT, t, 0.7, 2.6)
    return im


# ---------------- 장면 2: 누구한테 옮을까? ----------------
GY = 930
CAST = [  # (이름, x, 크기, 하품 시작 지연)
    ('baby', 400, 0, None),
    ('two', 590, 0.62, None),
    ('four', 770, 0.80, 0.45),
    ('six', 950, 0.94, 0.45),
]
DAD_X = 150
CYCLES = (1.0, 6.0)   # 아빠 하품 시작 시각


def wave_x(t, t0):
    """아빠 입에서 오른쪽으로 퍼지는 물결의 앞머리 x."""
    u = t-(t0+0.5)
    if u < 0: return None
    return DAD_X + 80 + u*360


S2 = int(13.6*F)
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(ROOM_T, ROOM_B, yy/H))
    d.text((W/2, 80), '하품, 누구한테 옮을까?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, GY, W, H], fill=FLOOR)
    # 아빠
    dk = max(yawn_k(t, CYCLES[0], 2.4), yawn_hold(t, CYCLES[-1]))
    dhy, dhr = stander(d, DAD_X, GY, 1.32, dk, DAD_SHIRT, 74)
    mouth = (DAD_X, dhy+dhr*0.6)
    # 물결 (반투명 호)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for c in CYCLES:
        fx = wave_x(t, c)
        if fx is None: continue
        for k in range(3):
            r = fx - mouth[0] - k*70
            if r < 40: continue
            a = max(0, 1-(r/1150))*(1 if t-c < 4.5 else max(0, 1-(t-c-4.5)/0.8))
            if a <= 0: continue
            ld.arc([mouth[0]-r, mouth[1]-r*0.45, mouth[0]+r, mouth[1]+r*0.45], -40, 40, fill=WAVE+(int(170*a),), width=10)
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')); d = ImageDraw.Draw(im)
    tops = {}
    for name, x, s, lag in CAST:
        yk = 0.0; reached = False
        for c in CYCLES:
            fx = wave_x(t, c)
            if fx is not None and fx >= x-60:
                reached = True
                if lag is not None:
                    tr = c+0.5+(x-60-DAD_X-80)/360
                    yk = max(yk, yawn_k(t, tr+lag, 2.4) if c != CYCLES[-1] else yawn_hold(t, tr+lag))
        if name == 'baby':
            hy, hr = bassinet_baby(d, x, GY); tops[name] = hy-hr
        else:
            hy, hr = stander(d, x, GY, s, yk, KID_SHIRT, 78*s+12, mood='flat' if (lag is None and reached) else 'smile')
            tops[name] = hy-hr
    lab(im, '하암~', (DAD_X+40, dhy-dhr-70), LT, t, 1.4, 4.2)
    lab(im, '멀뚱', (495, min(tops['baby'], tops['two'])-80), LM, t, 3.4)
    lab(im, '네 살부터', (860, min(tops['four'], tops['six'])-80), LG, t, 4.6)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/yawn_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('yawn', s1, S1, s2, S2, out,
              preview=[(s1, int(2.6*F), S1), (s2, int(2.2*F), S2), (s2, int(5.4*F), S2), (s2, int(13.0*F), S2)])
