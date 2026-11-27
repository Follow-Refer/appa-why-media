"""도토리가 두 개 됐어!(11/28): 상황(하원길, 꼰 손가락으로 도토리 만지며 "두 개?") →
답(편 손가락 바깥 두 쪽 = 늘 도토리 두 개 → 생각 풍선 두 개 /
손가락을 꼬면 그 두 쪽이 가운데서 만나 도토리 하나를 같이 만짐 → 생각 풍선은 그대로 두 개).
사용: python3 example_crossed_fingers_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab, KID_SHIRT

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210)
SKY_T = (206, 220, 240); SKY_B = (238, 234, 244)
WALK = (222, 214, 200); GRASS = (178, 210, 182)
TRUNK = (176, 150, 128); LEAF1 = (246, 200, 140); LEAF2 = (236, 170, 130)
NUT = (196, 150, 108); NUT_D = (170, 124, 86); CAP = (150, 120, 92); CAP_L = (176, 146, 116)
SKIN_D = (236, 204, 176); SLEEVE = (246, 200, 150)
ORG = (232, 150, 120); BLU = (140, 160, 210)


def sky(im):
    d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(SKY_T, SKY_B, y/H))
    return d


def overlay(im, fn):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(layer))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def acorn(d, x, y, r, a=255):
    """도토리: 아래 몸통 + 위 모자 + 꼭지. (x,y)=몸통 가운데."""
    A = lambda c: c+(a,) if a < 255 else c
    d.ellipse([x-r*0.82, y-r*0.75, x+r*0.82, y+r*1.0], fill=A(NUT))
    d.ellipse([x-r*0.15, y+r*0.78, x+r*0.15, y+r*1.08], fill=A(NUT_D))
    d.chord([x-r*0.98, y-r*1.05, x+r*0.98, y+r*0.05], 180, 360, fill=A(CAP))
    d.rounded_rectangle([x-r*0.98, y-r*0.55, x+r*0.98, y-r*0.18], radius=int(r*0.18), fill=A(CAP))
    for k in range(-2, 3):
        d.ellipse([x+k*r*0.36-r*0.12, y-r*0.62, x+k*r*0.36+r*0.12, y-r*0.38], fill=A(CAP_L))
    d.rounded_rectangle([x-r*0.09, y-r*1.32, x+r*0.09, y-r*0.95], radius=int(r*0.08), fill=A(CAP))


def acorn_a(im, x, y, r, a):
    if a <= 0: return
    overlay(im, lambda dl: acorn(dl, x, y, r, int(255*a)))


# ---------------- 장면 1: 하원길, 도토리 만지며 "두 개?" ----------------
S1 = int(3.4*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = sky(im)
    d.text((W/2, 80), '도토리가 두 개 됐어!', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 820, W, H], fill=WALK)
    d.rectangle([0, 800, W, 830], fill=GRASS)
    # 나무(오른쪽)
    d.rounded_rectangle([830, 420, 890, 820], radius=24, fill=TRUNK)
    for (x, y, r, c) in ((860, 360, 150, LEAF1), (770, 420, 100, LEAF2), (950, 430, 100, LEAF2), (860, 250, 100, LEAF2)):
        d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    for x in (760, 940, 990): acorn(d, x, 858, 16)
    # 아이(왼쪽)
    cx, cy = 400, 400
    d.rounded_rectangle([cx-30, 740, cx-6, 830], radius=12, fill=(130, 150, 190))
    d.rounded_rectangle([cx+6, 740, cx+30, 830], radius=12, fill=(130, 150, 190))
    d.rounded_rectangle([cx-95, 530, cx+95, 760], radius=60, fill=KID_SHIRT)
    d.line([cx-80, 580, cx-120, 690], fill=KID_SHIRT, width=46)
    d.ellipse([cx-146, 670, cx-96, 720], fill=SKIN)
    hx, hy = cx+170, 600                                                  # 앞으로 내민 오른손
    d.line([cx+75, 580, hx-30, hy+10], fill=KID_SHIRT, width=46)
    face(d, cx, cy, 120, 0, mood='wow' if t > 1.2 else 'smile')
    d.ellipse([hx-42, hy-30, hx+42, hy+44], fill=SKIN)
    # 꼰 두 손가락(작게) + 그 사이 도토리
    for (x0, x1) in ((hx-18, hx+16), (hx+18, hx-16)):
        d.line([x0, hy-6, x1, hy-80], fill=SKIN_D, width=30)
        d.line([x0, hy-6, x1, hy-80], fill=SKIN, width=22)
        d.ellipse([x1-15, hy-95, x1+15, hy-65], fill=SKIN, outline=SKIN_D, width=4)
    acorn(d, hx, hy-112, 26)
    # 두 개로 느껴지는 듯 살짝 겹쳐 보이는 도토리
    g = ease((t-1.0)/0.8)*(0.5+0.25*math.sin(t*5))
    acorn_a(im, hx+56, hy-118, 26, g)
    lab(im, '두 개?', (hx+180, hy-210), LM, t, 1.4)
    return im


# ---------------- 장면 2: 편 손가락 / 꼰 손가락 ----------------
FW, FL = 116, 440            # 손가락 굵기·길이
BX1, BX2, BY = 470, 610, 790  # 검지·중지 뿌리
def finger_img(edge_side, edge_col, edge_a):
    """위로 선 손가락 하나(RGBA). edge_side -1=왼쪽 옆면, +1=오른쪽 옆면에 색 줄."""
    im = Image.new('RGBA', (FW+40, FL+40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, 20+FW, 20+FL+30], radius=FW//2, fill=SKIN+(255,))
    d.ellipse([20+FW*0.28, 34, 20+FW*0.72, 34+FW*0.38], fill=SKIN_D+(255,))     # 손톱
    if edge_a > 0:
        x = 20+12 if edge_side < 0 else 20+FW-12
        d.line([x, 20+FW*0.55, x, 20+FL*0.36], fill=edge_col+(int(255*edge_a),), width=18)
    return im


def paste_finger(im, fimg, bx, ang):
    """뿌리(bx,BY)를 축으로 ang도(+는 시계방향) 기울여 붙이기."""
    w, h = fimg.size
    big = Image.new('RGBA', (h*2, h*2), (0, 0, 0, 0))
    big.paste(fimg, (h-w//2, 0))
    rot = big.rotate(-ang, resample=Image.BICUBIC, center=(h, h))
    im.paste(rot, (int(bx-h), int(BY-h)), rot)


def tip(bx, ang, back=60):
    a = math.radians(ang); L = FL-back
    return bx+L*math.sin(a), BY-L*math.cos(a)


def hand(im, cross, edge_a):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([330, 980, 790, 1120], radius=60, fill=SLEEVE)
    d.rounded_rectangle([370, 740, 770, 1010], radius=110, fill=SKIN)               # 손등
    d.rounded_rectangle([250, 820, 400, 900], radius=40, fill=SKIN)                 # 엄지
    for k, x in enumerate((680, 740)):                                              # 접은 약지·새끼
        d.ellipse([x-50, 730-k*6, x+50, 830-k*6], fill=SKIN_D)
    a1 = 30*cross; a2 = -30*cross
    paste_finger(im, finger_img(-1, ORG, edge_a), BX1, a1)                          # 검지(아래)
    paste_finger(im, finger_img(+1, BLU, edge_a), BX2, a2)                          # 중지(위로 겹침)
    return a1, a2


def bubble(im, a, ghost_k):
    """생각 풍선 + 도토리 두 개."""
    if a <= 0: return
    def f(dl):
        A = int(235*a)
        for (x, y, r) in ((236, 196, 14), (272, 168, 20)):
            dl.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, A), outline=(200, 196, 214, A), width=4)
        dl.ellipse([310, 50, 750, 250], fill=(255, 255, 255, A), outline=(200, 196, 214, A), width=5)
        acorn(dl, 455, 155, 44, int(255*a))
        acorn(dl, 605, 155, 44, int(255*a))
    overlay(im, f)


def spark(d, x, y, s, col):
    if s <= 0: return
    for k in range(6):
        ang = k*math.pi/3; r0, r1 = 50, 50+34*s
        d.line([x+math.cos(ang)*r0, y+math.sin(ang)*r0, x+math.cos(ang)*r1, y+math.sin(ang)*r1], fill=col, width=7)


S2 = int(16.0*F)
R = 48
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = sky(im)
    # 눈 감은 아이 얼굴(왼쪽 위) — 생각 풍선의 주인
    fx, fy, fr = 130, 170, 78
    face(d, fx, fy, fr, 0, mood='smile')
    for sx in (fx-fr*0.38, fx+fr*0.38):
        ey = fy+fr*0.08
        d.ellipse([sx-fr*0.16, ey-fr*0.16, sx+fr*0.16, ey+fr*0.16], fill=SKIN)
        d.arc([sx-fr*0.16, ey-fr*0.12, sx+fr*0.16, ey+fr*0.12], 20, 160, fill=INK, width=5)
    cross = ease((t-7.2)/3.0)
    edge_a = ease((t-0.3)/0.8)
    hand(im, cross, edge_a)
    d = ImageDraw.Draw(im)
    # 1부: 편 손가락 바깥 두 쪽에 도토리 두 개
    ty = 470
    lx0, rx0 = BX1-FW/2-R*0.85, BX2+FW/2+R*0.85
    come = ease((t-0.4)/3.0); go = ease((t-6.6)/0.8)
    la = 1-go
    acorn_a(im, lx0-420*(1-come), ty, R, la if t < 7.4 else 0)
    acorn_a(im, rx0+420*(1-come), ty, R, la if t < 7.4 else 0)
    s = max(0, 1-abs(t-3.6)/0.45)
    spark(d, lx0-10, ty, s, ORG); spark(d, rx0+10, ty, s, BLU)
    # 2부: 꼰 손가락 끝 사이 틈에 도토리 하나
    (ix, iy), (mx, my) = tip(BX1, 30, 70), tip(BX2, -30, 70)
    cxm = (ix+mx)/2; cym = (iy+my)/2+6
    drop = ease((t-10.4)/1.4)
    if t > 10.2:
        acorn_a(im, cxm, cym-520*(1-drop), R, min(1, (t-10.2)/0.4))
    s = max(0, 1-abs(t-11.9)/0.45)
    spark(d, cxm-60, cym, s, BLU); spark(d, cxm+60, cym, s, ORG)
    # 생각 풍선: 두 번 다 도토리 두 개
    ba = ease((t-3.9)/0.6)*(1-ease((t-6.6)/0.6)) + ease((t-12.3)/0.6)
    bubble(im, min(1, ba), 0)
    lab(im, '두 개', (BX1+(BX2-BX1)/2, 620), LM, t, 4.0, 6.6)
    lab(im, '하나', (860, cym+10), LT, t, 12.0)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/crossed_fingers_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('crossedfingers', s1, S1, s2, S2, out,
              preview=[(s1, int(3.0*F), S1), (s2, int(5.5*F), S2), (s2, int(9.0*F), S2), (s2, int(15.0*F), S2)])
