"""배에서 꼬르륵 했어!(11/20): 상황(하원길, 배 잡고 꼬르륵) → 답(물병 두 개를 꾹꾹 짜 내려감.
빈 배 병은 공기·물이 밀려 뽀글뽀글 꼬르륵 + 부스러기가 아래로 밀려 청소, 밥 가득 병은 짜도 조용).
사용: python3 example_tummy_rumble_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import numpy as np
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146); LY = (226, 186, 96)
HAIR = (120, 96, 82); KID_SHIRT = (176, 206, 232); MOUTH = (200, 110, 118); BAG = (246, 200, 150)
BOTTLE = (236, 244, 250); BOTTLE_D = (176, 196, 220); WATER = (196, 222, 242)
RICE = (250, 236, 196); RICE_D = (236, 214, 160); CRUMB = (196, 160, 126); CAP = (150, 196, 170)


def lab(im, text, xy, col, t, t_on, t_off=None, dy=0):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; y += dy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def face(d, cx, cy, r, mood='smile'):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SKIN)
    d.chord([cx-r-2, cy-r-6, cx+r+2, cy+r*0.38], 180, 360, fill=HAIR)
    ex = r*0.38; ey = cy+r*0.10; er = r*0.10
    for sx in (cx-ex, cx+ex):
        if mood == 'laugh':
            d.arc([sx-er*1.6, ey-er*0.6, sx+er*1.6, ey+er*1.8], 200, 340, fill=INK, width=max(3, int(r*0.07)))
        else:
            d.ellipse([sx-er, ey-er*1.1, sx+er, ey+er*1.1], fill=INK)
    my = cy+r*0.55
    if mood in ('wow', 'laugh'):
        d.chord([cx-r*0.22, my-r*0.12, cx+r*0.22, my+r*0.22], 0, 180, fill=MOUTH)
    else:
        d.arc([cx-r*0.24, my-r*0.16, cx+r*0.24, my+r*0.14], 20, 160, fill=LIP, width=max(3, int(r*0.07)))
    d.ellipse([cx-r*0.72, cy+r*0.32, cx-r*0.48, cy+r*0.48], fill=(250, 206, 196))
    d.ellipse([cx+r*0.48, cy+r*0.32, cx+r*0.72, cy+r*0.48], fill=(250, 206, 196))


def wobble(im, cx, cy, amp, t, col, side=1):
    """배 옆에서 흔들리는 작은 물결(꼬르륵)."""
    if amp <= 0.02: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for k in range(3):
        x0 = cx+side*(k*34)
        pts = []
        for j in range(9):
            y = cy-60+j*15
            pts.append((x0+side*10*math.sin(j*1.3+t*9)*amp, y))
        ld.line(pts, fill=col+(int(220*amp*(1-k*0.25)),), width=7, joint='curve')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


# ---------------- 장면 1: 하원길, 배 잡고 꼬르륵 ----------------
S1 = int(3.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((214, 222, 242), (246, 226, 222), yy/H))
    d.text((W/2, 80), '배에서 꼬르륵 했어!', font=FBW, fill=TXT, anchor='mm')
    # 해질녘 해, 나무, 보도
    d.ellipse([800, 170, 900, 270], fill=(250, 214, 160))
    for x in (110, 960):
        d.rounded_rectangle([x-14, 560, x+14, 800], radius=10, fill=BROWN)
        d.ellipse([x-90, 380, x+90, 600], fill=GREEN)
    d.rectangle([0, 800, W, H], fill=(222, 214, 204))
    for x in range(0, W, 120): d.line([x, 800, x+60, H], fill=(208, 198, 188), width=4)
    cx, cy, r = 540, 470, 120
    bob = 6*math.sin(t*5) if t > 1.0 else 0
    # 몸통(상반신~배) + 가방끈
    by = cy+r*0.85
    d.rounded_rectangle([cx-r*1.05, by+bob, cx+r*1.05, by+r*2.6+bob], radius=int(r*0.6), fill=KID_SHIRT)
    d.line([(cx-r*0.75, by+10+bob), (cx-r*0.55, by+r*1.4+bob)], fill=BAG, width=18)
    d.line([(cx+r*0.75, by+10+bob), (cx+r*0.55, by+r*1.4+bob)], fill=BAG, width=18)
    face(d, cx, cy+bob, r, 'laugh' if t > 1.0 else 'wow')
    # 두 손을 배 위에(짧은 팔: 어깨 → 배 가운데)
    k = ease((t-0.2)/0.7)
    belly = by+r*1.75+bob
    for side in (-1, 1):
        sh = (cx+side*r*0.95, by+r*0.4+bob)
        hand = (cx+side*(r*0.95-k*r*0.55), sh[1]+(belly-sh[1])*k)
        d.line([sh, hand], fill=KID_SHIRT, width=int(r*0.36))
        d.ellipse([sh[0]-r*0.18, sh[1]-r*0.18, sh[0]+r*0.18, sh[1]+r*0.18], fill=KID_SHIRT)
        d.ellipse([hand[0]-r*0.2, hand[1]-r*0.2, hand[0]+r*0.2, hand[1]+r*0.2], fill=SKIN)
    amp = ease((t-0.9)/0.5)
    wobble(im, cx+r*1.3, belly, amp, t, LT, 1)
    wobble(im, cx-r*1.3, belly, amp, t, LT, -1)
    lab(im, '꼬르륵~', (cx+300, belly-170), LT, t, 1.1)
    return im


# ---------------- 장면 2: 빈 배 물병 vs 밥 가득 물병 ----------------
S2 = int(14.0*F)
BX = (300, 780)            # 두 병 가운데 x
TOP, BOT, HW = 380, 875, 150   # 병 몸통 위·아래, 반폭
WLEV = 765                 # 빈 병 물 높이
PASSES = [(1.2, 5.2), (7.0, 10.6)]   # 꾹꾹 짜 내려가는 시간


def squeeze_y(t):
    """짜는 자리(y)와 세기(0~1)."""
    for a, b in PASSES:
        if a <= t <= b:
            u = (t-a)/(b-a)
            return TOP+40+(BOT-TOP-60)*u, math.sin(math.pi*min(1, u*1.15))**0.6
    return None, 0


def half_width(y, t):
    sy, s = squeeze_y(t)
    w = HW
    if sy is not None: w -= 70*s*math.exp(-((y-sy)/55)**2)
    return w


def bottle(d, cx, t, full):
    ys = list(range(TOP, BOT+1, 6))
    left = [(cx-half_width(y, t), y) for y in ys]; right = [(cx+half_width(y, t), y) for y in reversed(ys)]
    # 목·뚜껑
    d.rounded_rectangle([cx-55, TOP-90, cx+55, TOP+10], radius=18, fill=BOTTLE, outline=BOTTLE_D, width=6)
    d.rounded_rectangle([cx-62, TOP-130, cx+62, TOP-80], radius=14, fill=CAP)
    d.polygon(left+right, fill=BOTTLE)
    # 안에 든 것
    if full:
        top = TOP+8
        inner = [(cx-half_width(y, t)+10, y) for y in ys if y >= top] + [(cx+half_width(y, t)-10, y) for y in reversed(ys) if y >= top]
        d.polygon(inner, fill=RICE)
        rng = np.random.default_rng(7)
        for _ in range(70):
            y = rng.uniform(top+20, BOT-20); x = cx+rng.uniform(-1, 1)*(half_width(y, t)-34)
            d.ellipse([x-9, y-5, x+9, y+5], fill=RICE_D)
    else:
        inner = [(cx-half_width(y, t)+10, y) for y in ys if y >= WLEV] + [(cx+half_width(y, t)-10, y) for y in reversed(ys) if y >= WLEV]
        if len(inner) > 2: d.polygon(inner, fill=WATER)
    d.line(left, fill=BOTTLE_D, width=7); d.line(right, fill=BOTTLE_D, width=7)
    d.line([left[-1], right[0]], fill=BOTTLE_D, width=7)
    d.line([(cx-HW+4, TOP), (cx-55, TOP)], fill=BOTTLE_D, width=7); d.line([(cx+55, TOP), (cx+HW-4, TOP)], fill=BOTTLE_D, width=7)
    # 짜는 자리 표시: 양옆 작은 화살촉 ▶ ◀
    sy, s = squeeze_y(t)
    if sy is not None and s > 0.05:
        for side in (-1, 1):
            x = cx+side*(half_width(sy, t)+30)
            d.polygon([(x+side*26, sy-22), (x+side*26, sy+22), (x, sy)], fill=LT)


CRUMBS = [(-80, 430), (40, 490), (-20, 560), (90, 610), (-100, 660), (20, 700), (-50, 520), (70, 410)]


def crumbs(d, cx, t):
    """부스러기: 짜는 자리가 지나가면 아래로 밀려 내려감."""
    for k, (dx, y0) in enumerate(CRUMBS):
        y = y0
        for a, b in PASSES:
            if t > a:
                u = min(1, (t-a)/(b-a)); sy = TOP+40+(BOT-TOP-60)*u
                if sy > y: y = min(BOT-30-(k % 3)*14, sy+24)
        x = cx+dx*min(1, half_width(y, t)/HW)
        d.ellipse([x-12, y-10, x+12, y+10], fill=CRUMB)


def bubbles(im, cx, t):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for a, b in PASSES:
        for k in range(14):
            st = a+0.3+k*(b-a)/14
            u = (t-st)/1.4
            if not (0 <= u <= 1): continue
            x = cx+((k*53) % 160-80)+8*math.sin(u*9+k)
            y = WLEV+60-u*(WLEV-TOP-20)
            r = 12+(k % 3)*6
            al = int(230*(1-u*0.6))
            ld.ellipse([x-r, y-r, x+r, y+r], outline=LM+(al,), width=6, fill=(255, 255, 255, al//3))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((226, 230, 244), (242, 238, 246), yy/H))
    d.text((W/2, 80), '꾹꾹 짜 보면?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=(222, 212, 200))
    bottle(d, BX[0], t, False); crumbs(d, BX[0], t)
    bottle(d, BX[1], t, True)
    bubbles(im, BX[0], t)
    _, s = squeeze_y(t)
    lab(im, '빈 배', (BX[0], 970), LM, t, 0.4)
    lab(im, '밥 가득', (BX[1], 970), LY, t, 0.4)
    lab(im, '꼬르륵', (BX[0], 180), LT, t, 2.0)
    lab(im, '조용', (BX[1], 180), LG, t, 2.6)
    return im


def sounds(total, sr):
    n = int(total*sr); y = np.zeros(n); rng = np.random.default_rng(5)
    off = S1/F-1.0

    def blub(t0, f0, amp):
        L = int(0.12*sr); s = int(t0*sr)
        if s < 0 or s+L >= n: return
        tt = np.arange(L)/sr
        f = f0*(1+2.2*tt/0.12)
        ph = 2*np.pi*np.cumsum(f)/sr
        y[s:s+L] += amp*np.sin(ph)*np.exp(-tt/0.035)
    # 장면1: 배 꼬르륵(낮게)
    for k in range(7): blub(1.1+k*0.17+rng.uniform(0, 0.05), 120+rng.uniform(0, 60), 0.18)
    # 장면2: 빈 병 짜는 동안만 뽀글뽀글
    for a, b in PASSES:
        for k in range(14):
            blub(off+a+0.3+k*(b-a)/14+rng.uniform(-0.04, 0.04), 170+rng.uniform(0, 140), 0.16)
    y[-int(sr*0.5):] *= np.linspace(1, 0, int(sr*0.5))
    return y


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/tummy_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('tummy', s1, S1, s2, S2, out, sounds=sounds,
              preview=[(s1, int(2.6*F), S1), (s2, int(3.0*F), S2), (s2, int(8.5*F), S2), (s2, int(13.5*F), S2)])
