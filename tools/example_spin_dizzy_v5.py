"""멈췄는데 세상이 빙글빙글 돌아!(11/21): 상황(놀이터 뺑뺑이에서 내려 비틀비틀) → 답(위에서 본 물컵.
컵을 돌리다 딱 멈추면 컵은 섰는데 물 위 종이 조각은 계속 돈다. 옆의 아이 머리 위 빙글이도 물과 같이 돌다가
물이 멈추면 사라짐 = 귓속 물이 멈출 때까지 어지러움).
사용: python3 example_spin_dizzy_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import numpy as np
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146); LY = (226, 186, 96)
HAIR = (120, 96, 82); KID_SHIRT = (176, 206, 232); MOUTH = (200, 110, 118)
WATER = (200, 224, 244); WATER_D = (176, 204, 232); RIM = (250, 250, 252); RIM_D = (196, 204, 222)
BITS = [(246, 190, 170), (246, 214, 140), (170, 206, 180), (200, 186, 232), (246, 190, 170), (246, 214, 140),
        (170, 206, 180), (200, 186, 232), (246, 214, 140)]


def lab(im, text, xy, col, t, t_on, t_off=None):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def face(d, cx, cy, r, mood='smile', spin=0.0):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SKIN)
    d.chord([cx-r-2, cy-r-6, cx+r+2, cy+r*0.38], 180, 360, fill=HAIR)
    ex = r*0.38; ey = cy+r*0.10; er = r*0.12
    for sx in (cx-ex, cx+ex):
        if mood == 'dizzy':
            # 작은 소용돌이 눈(부드럽게)
            pts = []
            for j in range(40):
                a = j*0.42+spin; rr = er*1.3*j/40
                pts.append((sx+rr*math.cos(a), ey+rr*math.sin(a)))
            d.line(pts, fill=INK, width=max(3, int(r*0.05)), joint='curve')
        else:
            d.ellipse([sx-er*0.8, ey-er*0.9, sx+er*0.8, ey+er*0.9], fill=INK)
    my = cy+r*0.55
    if mood == 'dizzy':
        pts = [(cx-r*0.24+j*r*0.06, my+r*0.05*math.sin(j*1.6)) for j in range(9)]
        d.line(pts, fill=LIP, width=max(3, int(r*0.06)), joint='curve')
    else:
        d.arc([cx-r*0.26, my-r*0.18, cx+r*0.26, my+r*0.16], 20, 160, fill=LIP, width=max(3, int(r*0.07)))
    d.ellipse([cx-r*0.74, cy+r*0.32, cx-r*0.50, cy+r*0.48], fill=(250, 206, 196))
    d.ellipse([cx+r*0.50, cy+r*0.32, cx+r*0.74, cy+r*0.48], fill=(250, 206, 196))


def halo(im, cx, cy, rx, ang, strength):
    """머리 위를 도는 작은 별 세 개(어질어질)."""
    if strength <= 0.02: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    A = int(235*min(1, strength))
    ld.ellipse([cx-rx, cy-rx*0.28, cx+rx, cy+rx*0.28], outline=LM+(A//3,), width=4)
    for k in range(3):
        a = ang+k*2*math.pi/3
        x = cx+rx*math.cos(a); y = cy+rx*0.28*math.sin(a)
        s = 18+6*math.sin(a)  # 앞쪽이 조금 크게
        col = [YEL, (246, 190, 170), (200, 186, 232)][k]
        star = []
        for j in range(10):
            rr = s if j % 2 == 0 else s*0.45
            aa = -math.pi/2+j*math.pi/5
            star.append((x+rr*math.cos(aa), y+rr*math.sin(aa)))
        ld.polygon(star, fill=col+(A,))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


# ---------------- 장면 1: 놀이터 뺑뺑이에서 내려 비틀비틀 ----------------
S1 = int(3.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((206, 220, 240), (238, 232, 244), yy/H))
    d.text((W/2, 80), '세상이 빙글빙글!', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 760, W, H], fill=(232, 222, 200))
    # 뒤쪽 뺑뺑이(회전 놀이기구)
    mx, my = 830, 700
    d.ellipse([mx-190, my-40, mx+190, my+40], fill=(236, 176, 160))
    d.ellipse([mx-190, my-52, mx+190, my+28], fill=(246, 196, 178))
    for k in range(4):
        a = t*1.2+k*math.pi/2
        x = mx+150*math.cos(a)
        if math.sin(a) > -0.2:
            d.line([(x, my-12+10*math.sin(a)), (x, my-170)], fill=(150, 170, 214), width=10)
    d.ellipse([mx-140, my-200, mx+140, my-150], outline=(150, 170, 214), width=10)
    d.rounded_rectangle([mx-10, my-200, mx+10, my-20], radius=6, fill=(150, 170, 214))
    # 나무
    d.rounded_rectangle([110-14, 520, 110+14, 770], radius=10, fill=BROWN)
    d.ellipse([20, 330, 200, 560], fill=GREEN)
    # 아이(비틀비틀: 살짝 좌우로 흔들림)
    sway = 26*math.sin(t*3.2)
    cx, cy, r = 430+sway, 430, 115
    by = cy+r*0.85
    d.rounded_rectangle([cx-r*0.95, by, cx+r*0.95, by+r*2.1], radius=int(r*0.55), fill=KID_SHIRT)
    # 다리(짧게)
    for side in (-1, 1):
        lx = cx+side*r*0.42
        d.rounded_rectangle([lx-r*0.22, by+r*2.0, lx+r*0.22, by+r*2.85], radius=int(r*0.2), fill=(150, 150, 190))
        d.ellipse([lx-r*0.32, by+r*2.72, lx+r*0.32, by+r*3.0], fill=(236, 150, 140))
    # 팔: 균형 잡으려고 옆으로 살짝(짧게)
    for side in (-1, 1):
        sh = (cx+side*r*0.85, by+r*0.35)
        hand = (cx+side*r*1.45, by+r*0.75+side*10*math.sin(t*3.2))
        d.line([sh, hand], fill=KID_SHIRT, width=int(r*0.34))
        d.ellipse([hand[0]-r*0.19, hand[1]-r*0.19, hand[0]+r*0.19, hand[1]+r*0.19], fill=SKIN)
    face(d, cx, cy, r, 'dizzy', spin=t*4)
    halo(im, cx, cy-r*1.25, r*0.95, t*3.0, ease((t-0.4)/0.6))
    return im


# ---------------- 장면 2: 위에서 본 물컵 + 옆의 아이 ----------------
S2 = int(14.0*F)
CX, CY, CR = 400, 560, 300           # 컵(위에서 본 모습)
KX, KY, KR = 860, 800, 105           # 아이 얼굴
T_START, T_STOP, TAU_UP, TAU_DN = 0.6, 5.0, 0.9, 2.0
W_CUP = 2.4                            # 컵 최고 각속도(rad/s)


def cup_w(t):
    if t < T_START: return 0.0
    if t < T_STOP: return W_CUP*ease((t-T_START)/0.8)
    return W_CUP*max(0.0, 1-(t-T_STOP)/0.25)


# 각도 적분(미리 계산)
DT = 1/F/8
_ts = np.arange(0, 15, DT)
_cupA = np.zeros_like(_ts); _watW = np.zeros_like(_ts); _watA = np.zeros_like(_ts)
for k in range(1, len(_ts)):
    t = _ts[k]; wc = cup_w(t)
    tau = TAU_UP if t < T_STOP else TAU_DN
    ww = _watW[k-1]
    if t < T_STOP: ww += (wc-ww)*DT/tau
    else: ww -= ww*DT/tau if ww > 0.02 else ww
    _watW[k] = ww
    _cupA[k] = _cupA[k-1]+wc*DT; _watA[k] = _watA[k-1]+ww*DT


def at(arr, t): return float(arr[min(len(arr)-1, int(t/DT))])


BITPOS = [(0.25, 0.3), (0.55, 1.4), (0.72, 2.5), (0.45, 3.3), (0.8, 4.2), (0.35, 5.1), (0.62, 5.8), (0.15, 4.0), (0.78, 0.9)]


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(236, 228, 220))       # 식탁(위에서)
    for x in range(-40, W, 150): d.line([x, 0, x+40, H], fill=(228, 220, 212), width=6)
    d.rounded_rectangle([0, 0, W, 150], radius=0, fill=BG)
    d.text((W/2, 80), '컵을 돌리다 멈추면?', font=FBW, fill=TXT, anchor='mm')
    ca = at(_cupA, t); wa = at(_watA, t); ww = at(_watW, t)
    # 컵 그림자 + 테두리 + 물
    d.ellipse([CX-CR+14, CY-CR+18, CX+CR+14, CY+CR+18], fill=(222, 212, 204))
    d.ellipse([CX-CR, CY-CR, CX+CR, CY+CR], fill=RIM, outline=RIM_D, width=6)
    wr = CR-34
    d.ellipse([CX-wr, CY-wr, CX+wr, CY+wr], fill=WATER)
    # 물결 고리(물과 같이 돎)
    for rr in (0.35, 0.6, 0.85):
        a0 = wa*1.0+rr*3
        R = wr*rr
        d.arc([CX-R, CY-R, CX+R, CY+R], math.degrees(a0), math.degrees(a0)+70, fill=WATER_D, width=6)
        d.arc([CX-R, CY-R, CX+R, CY+R], math.degrees(a0)+180, math.degrees(a0)+250, fill=WATER_D, width=6)
    # 종이 조각(물과 같이 돎)
    for k, (rr, a) in enumerate(BITPOS):
        ang = a+wa; R = wr*rr
        x = CX+R*math.cos(ang); y = CY+R*math.sin(ang)
        s = 20
        pts = []
        for j in range(4):
            aa = ang+math.pi/4+j*math.pi/2+k
            pts.append((x+s*math.cos(aa), y+s*math.sin(aa)))
        d.polygon(pts, fill=BITS[k])
    # 컵 테두리 스티커(컵과 같이 돎)
    sa = ca-math.pi/2
    sx = CX+(CR-17)*math.cos(sa); sy = CY+(CR-17)*math.sin(sa)
    d.ellipse([sx-22, sy-22, sx+22, sy+22], fill=LT)
    # 아이(머리 위 별이 물과 같은 빠르기로 돎)
    strength = min(1.0, ww/0.9) if t > T_STOP else 0.0
    d.rounded_rectangle([KX-KR*0.9, KY+KR*0.85, KX+KR*0.9, KY+KR*2.2], radius=int(KR*0.5), fill=KID_SHIRT)
    face(d, KX, KY, KR, 'dizzy' if strength > 0.25 else 'smile', spin=wa*2)
    halo(im, KX, KY-KR*1.25, KR*0.95, wa*1.6, strength)
    # 라벨 4개
    lab(im, '컵: 멈춤', (CX, 220), LT, t, T_STOP+0.2)
    lab(im, '물: 빙글', (CX, CY+CR+70), LM, t, T_STOP+0.8, 10.0)
    lab(im, '어질어질', (KX, KY-KR*2.15), LY, t, T_STOP+1.4, 9.6)
    lab(im, '괜찮아', (KX, KY-KR*2.15), LG, t, 10.2)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/spin_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('spin', s1, S1, s2, S2, out,
              preview=[(s1, int(2.4*F), S1), (s2, int(6.2*F), S2), (s2, int(9.0*F), S2), (s2, int(13.0*F), S2)])
