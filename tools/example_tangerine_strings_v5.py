"""귤에 하얀 실 왜 있어?(11/17): 상황(하원길 차 뒷자리, 아이가 깐 귤의 하얀 실을 들어 보임)
→ 답(나무에 달린 귤: 가지에서 꼭지를 지나 하얀 실을 따라 물방울이 알맹이마다 들어가고, 알맹이가 하나씩 통통·진해짐).
사용: python3 example_tangerine_strings_v5.py out.mp4 [preview.png]"""
import sys, math, random
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab, HAIR

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
PEEL_PALE = (250, 222, 170); ORANGE = (246, 170, 96); ORANGE_D = (232, 150, 86)
STRAND = (255, 252, 246); DROP = (130, 182, 230)
SEAT = (190, 196, 214); SEAT_D = (170, 176, 198); CAR_IN = (226, 222, 232)
BRANCH = (176, 146, 122); LEAF = (150, 196, 160); LEAF_D = (126, 176, 140)
KID_SHIRT = (246, 200, 150)


def peeled(d, cx, cy, r, fill_k=None, strands=True, nseg=7):
    """옆에서 본 깐 귤. 세로 결(알맹이 경계) + 알맹이 가운데 하얀 실."""
    rx, ry = r*1.06, r
    fill_k = fill_k or [1]*nseg
    phis = [-math.pi/2+math.pi*k/nseg for k in range(nseg+1)]
    def mer(phi, m=28):
        return [(cx+rx*math.sin(s)*math.sin(phi), cy-ry*math.cos(s)) for s in [math.pi*j/m for j in range(m+1)]]
    for k in range(nseg):
        a, b = mer(phis[k]), mer(phis[k+1])
        col = mix(PEEL_PALE, ORANGE if k % 2 else ORANGE_D, fill_k[k])
        d.polygon(a+b[::-1], fill=col)
    for k in range(1, nseg):
        d.line(mer(phis[k]), fill=mix(PEEL_PALE, (226, 140, 80), 0.5), width=4)
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=(230, 150, 90), width=5)
    paths = []
    if strands:
        for k in range(nseg):
            pm = (phis[k]+phis[k+1])/2
            pts = []
            for j in range(23):
                s = math.pi*(0.02+0.9*j/22)
                w = 0.07*math.sin(j*0.9+k)
                pts.append((cx+rx*math.sin(s)*math.sin(pm+w), cy-ry*math.cos(s)))
            if abs(math.sin(pm)) < 0.97:
                d.line(pts, fill=STRAND, width=max(4, int(r*0.026)), joint='curve')
                # 작은 갈래 둘
                for jj in (8, 14):
                    x0, y0 = pts[jj]; sg = 1 if k % 2 else -1
                    d.line([(x0, y0), (x0+sg*r*0.07, y0+r*0.08)], fill=STRAND, width=max(3, int(r*0.018)))
            paths.append(pts)
    return paths


def along(path, u):
    """폴리라인 위 비율 u(0~1) 지점."""
    L = [math.dist(path[j], path[j+1]) for j in range(len(path)-1)]; tot = sum(L); s = u*tot
    for j, l in enumerate(L):
        if s <= l: f = s/l if l else 0; return (path[j][0]+(path[j+1][0]-path[j][0])*f, path[j][1]+(path[j+1][1]-path[j][1])*f)
        s -= l
    return path[-1]


# ---------------- 장면 1: 하원길 차 뒷자리 ----------------
S1 = int(3.8*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), CAR_IN); d = ImageDraw.Draw(im)
    # 창문 + 지나가는 나무
    d.rounded_rectangle([90, 150, 990, 520], radius=60, fill=(214, 228, 242))
    for k in range(6):
        x = (k*240-t*260) % 1200-100
        if 110 < x < 970:
            d.rectangle([x-10, 380, x+10, 500], fill=BRANCH)
            d.ellipse([x-60, 290, x+60, 410], fill=LEAF)
    d.rectangle([90, 500, 990, 520], fill=CAR_IN)
    d.rounded_rectangle([90, 150, 990, 520], radius=60, outline=(200, 196, 212), width=14)
    d.text((W/2, 80), '귤에 하얀 실 왜 있어?', font=FBW, fill=TXT, anchor='mm')
    # 카시트 + 아이
    d.rounded_rectangle([250, 300, 710, 1100], radius=120, fill=SEAT)
    d.rounded_rectangle([290, 640, 670, 1100], radius=100, fill=KID_SHIRT)
    face(d, 480, 500, 120, 0, mood='wow' if t > 1.2 else 'smile')
    # 손에 든 깐 귤(아이 가슴 앞, 짧은 손)
    lift = ease((t-0.2)/1.0); gx, gy = 560, 860-50*lift
    peeled(d, gx, gy, 105)
    for sx in (-1, 1):
        d.ellipse([gx+sx*100-32, gy+20, gx+sx*100+32, gy+84], fill=SKIN)
    lab(im, '하얀 실?', (830, 700), LT, t, 1.5)
    return im


# ---------------- 장면 2: 나무에 달린 귤, 물길 ----------------
CX, CY, R = 540, 660, 255
NSEG = 7
BR = [(-20, 250), (300, 232), (540, 228), (820, 214), (1100, 200)]   # 가지
STEM = [(540, 228), (540, CY-R)]


def seg_k(t, k):
    return ease((t-(5.0+0.55*k))/3.0)


S2 = int(14.0*F)
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((214, 230, 244), (240, 236, 246), yy/H))
    d.text((W/2, 80), '하얀 실은 뭐였을까?', font=FBW, fill=TXT, anchor='mm')
    # 가지 + 잎
    d.line(BR, fill=BRANCH, width=30, joint='curve')
    for lx, ly, sg in ((180, 240, -1), (380, 230, 1), (720, 220, -1), (900, 208, 1)):
        d.ellipse([lx-70, ly-34+sg*40, lx+70, ly+34+sg*40], fill=LEAF if sg > 0 else LEAF_D)
    d.line(STEM, fill=BRANCH, width=16)
    fk = [seg_k(t, k) for k in range(NSEG)]
    paths = peeled(d, CX, CY, R, fk, nseg=NSEG)
    # 꼭지(초록 별)
    d.polygon([(CX+math.cos(a)*(44 if j % 2 == 0 else 20), CY-R+4+math.sin(a)*(26 if j % 2 == 0 else 12))
               for j, a in enumerate([math.pi*2*q/10 for q in range(10)])], fill=LEAF_D)
    # 물방울: 가지 → 꼭지 → 하얀 실 → 알맹이
    route0 = BR[:3]+[(540, CY-R+6)]
    rnd = random.Random(5)
    vis = [k for k, p in enumerate(paths) if abs(p[11][0]-CX) < R*0.95]
    for j in range(26):
        t0 = 1.4+j*0.42; u = (t-t0)/3.6
        if u < 0 or u > 1 or t > 12.0: continue
        k = vis[j % len(vis)]
        if u < 0.5: p = along(route0, u/0.5)
        else: p = along(paths[k], (u-0.5)/0.5*0.85)
        r = 16
        d.ellipse([p[0]-r, p[1]-r*1.2, p[0]+r, p[1]+r], fill=DROP)
    lab(im, '나무', (170, 330), LG, t, 1.2)
    lab(im, '꼭지', (740, 360), LT, t, 3.0)
    lab(im, '물길', (900, 620), LM, t, 4.8)
    lab(im, '통통', (CX, 990), LT, t, 8.6)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/tangerine_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('tangerine', s1, S1, s2, S2, out,
              preview=[(s1, int(3.0*F), S1), (s2, int(3.5*F), S2), (s2, int(7.0*F), S2), (s2, int(13.5*F), S2)])
