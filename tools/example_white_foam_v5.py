"""분홍 비누가 하얀 거품 됐어!(11/26): 상황(저녁 목욕, 분홍 비누 문지르니 하얀 거품) →
답(투명한 방울 하나 / 잔뜩 모이면 하양, 투명한 얼음 / 잔뜩 모인 눈은 하양을 나란히).
사용: python3 example_white_foam_v5.py out.mp4 [preview.png]"""
import sys, math, random
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210)
TILE = (226, 236, 240); TILE_L = (208, 222, 230)
TUB = (250, 250, 252); TUB_D = (222, 226, 236)
WATER_T = (196, 222, 238)
PINK = (244, 186, 200); PINK_D = (228, 160, 180)
EDGE = (150, 168, 200)
TILE2 = (184, 202, 224); TILE2_L = (168, 188, 214)


def tiles(d, col=TILE_L):
    for x in range(0, W, 120): d.line([x, 0, x, H], fill=col, width=3)
    for y in range(0, H, 120): d.line([0, y, W, y], fill=col, width=3)


def overlay(im, fn):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(layer))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def foam_blob(d, cx, cy, s, a=255):
    """하얀 거품 덩어리(작은 원 여러 개)."""
    rnd = random.Random(5)
    for k in range(14):
        ang = rnd.uniform(0, 2*math.pi); rr = rnd.uniform(0, 1)*s*0.7
        x = cx+math.cos(ang)*rr; y = cy+math.sin(ang)*rr*0.6; r = s*rnd.uniform(0.32, 0.5)
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, a), outline=(220, 228, 240, a), width=3)


# ---------------- 장면 1: 저녁 목욕 ----------------
S1 = int(4.2*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), TILE); d = ImageDraw.Draw(im); tiles(d)
    d.text((W/2, 80), '분홍 비누가 하얀 거품 됐어!', font=FBW, fill=TXT, anchor='mm')
    # 아이 몸(어깨까지 물에 잠김)
    d.rounded_rectangle([380, 560, 620, 760], radius=70, fill=SKIN)
    # 왼손: 분홍 비누(몸 가까이, 짧은 팔)
    d.line([420, 640, 330, 600], fill=SKIN, width=50)
    d.ellipse([290, 560, 370, 640], fill=SKIN)
    d.rounded_rectangle([250, 520, 380, 590], radius=26, fill=PINK, outline=PINK_D, width=4)
    # 오른손: 들어 올린 손 위 거품
    lift = ease((t-0.3)/1.0)
    hx, hy = 680, 600-90*lift
    d.line([590, 640, hx, hy+30], fill=SKIN, width=50)
    d.ellipse([hx-48, hy-10, hx+48, hy+60], fill=SKIN)
    g = ease((t-0.6)/1.6)
    if g > 0: overlay(im, lambda dl: foam_blob(dl, hx, hy-30-30*g, 40+60*g))
    d = ImageDraw.Draw(im)
    face(d, 500, 450, 112, 0, mood='wow' if t > 1.6 else 'smile')
    # 욕조 + 물
    d.rounded_rectangle([90, 660, 990, 1020], radius=70, fill=TUB)
    d.rounded_rectangle([90, 660, 990, 700], radius=20, fill=TUB_D)
    d.rounded_rectangle([130, 640, 950, 690], radius=24, fill=WATER_T)
    return im


# ---------------- 장면 2: 하나는 투명, 모이면 하양 ----------------
BX, BY, BR = 270, 330, 110            # 방울 하나
PX, PBASE = 760, 440                  # 거품 더미
IX, IY, IS = 270, 770, 170            # 얼음
SX, SBASE = 760, 890                  # 눈 더미


def mound(seed, n, cx, base, wid, hei, rmin, rmax):
    rnd = random.Random(seed); pts = []
    while len(pts) < n:
        x = rnd.uniform(-1, 1); y = rnd.uniform(0, 1)
        if y > (1-x*x)**0.8: continue
        r = rnd.uniform(rmin, rmax)
        pts.append((cx+x*wid, base-y*hei-r*0.3, r))
    pts.sort(key=lambda p: -p[1])     # 아래부터 쌓이게
    return pts

PILE = mound(11, 80, PX, PBASE, 210, 230, 22, 40)
SNOW = mound(23, 220, SX, SBASE, 220, 200, 11, 18)


def bubble(dl, x, y, r, a_fill, a_edge, rainbow=False):
    dl.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, a_fill), outline=EDGE+(a_edge,), width=max(2, int(r*0.05)))
    dl.arc([x-r*0.7, y-r*0.7, x+r*0.2, y+r*0.2], 190, 250, fill=(255, 255, 255, min(255, a_edge+60)), width=max(3, int(r*0.09)))
    if rainbow:
        for k, c in enumerate(((246, 190, 200), (246, 224, 160), (180, 220, 200), (180, 196, 236))):
            rr = r-6-k*5
            dl.arc([x-rr, y-rr, x+rr, y+rr], 20, 80, fill=c+(150,), width=5)


def flake(dl, x, y, r, a):
    dl.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, a), outline=(228, 234, 244, a), width=2)


S2 = int(13.5*F)
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), TILE2); d = ImageDraw.Draw(im); tiles(d, TILE2_L)
    # 위: 방울 하나(뒤 타일 줄이 그대로 비침)
    a0 = ease(t/0.8)
    def top(dl):
        bubble(dl, BX, BY, BR, int(34*a0), int(230*a0), rainbow=True)
        k = (t-1.6)/3.4
        cnt = int(len(PILE)*ease(k)) if k > 0 else 0
        for j, (x, y, r) in enumerate(PILE[:cnt]):
            pop = min(1, (len(PILE)*ease(k)-j)/3)
            bubble(dl, x, y, r*(0.6+0.4*pop), int(205*pop), int(200*pop))
    overlay(im, top)
    # 아래: 얼음 하나 / 눈 더미
    ai = ease((t-6.0)/0.8)
    def bottom(dl):
        if ai > 0:
            s = IS/2
            dl.rounded_rectangle([IX-s, IY-s, IX+s, IY+s], radius=26, fill=(214, 232, 248, int(70*ai)), outline=EDGE+(int(230*ai),), width=6)
            dl.line([IX-s+28, IY-s+40, IX-s+28, IY+s-60], fill=(255, 255, 255, int(220*ai)), width=8)
            dl.line([IX-s+40, IY-s+28, IX+s-70, IY-s+28], fill=(255, 255, 255, int(220*ai)), width=8)
        k = (t-7.0)/3.4
        if k > 0:
            m = (len(SNOW)+5)*ease(k)
            for j, (x, y, r) in enumerate(SNOW):
                p = m-j
                if p <= 0: break
                fall = max(0, 1-p/4)            # 막 내려오는 결정
                flake(dl, x, y-fall*160, r, int(255*min(1, p/2)))
    overlay(im, bottom)
    lab(im, '하나: 투명', (BX, 525), LM, t, 1.0)
    lab(im, '모이면: 하양', (PX, 560), LT, t, 5.0)
    lab(im, '얼음: 투명', (IX, 975), LM, t, 6.6)
    lab(im, '눈: 하양', (SX, 975), LT, t, 10.4)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/white_foam_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('whitefoam', s1, S1, s2, S2, out,
              preview=[(s1, int(3.2*F), S1), (s2, int(3.0*F), S2), (s2, int(8.5*F), S2), (s2, int(13.0*F), S2)])
