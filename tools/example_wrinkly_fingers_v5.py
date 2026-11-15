"""손이 할머니 손 됐어!(11/16): 상황(저녁 목욕, 아이가 쭈글한 손을 들어 보임) → 답(같은 물 속인데 손끝·발끝만 천천히 쭈글, 팔은 그대로 매끈).
사용: python3 example_wrinkly_fingers_v5.py out.mp4 [preview.png]"""
import sys, math, random
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab, HAIR

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
TILE = (226, 236, 240); TILE_L = (208, 222, 230)
TUB = (250, 250, 252); TUB_D = (222, 226, 236)
WATER_T = (196, 222, 238); WATER_B = (176, 206, 230)
WRINK = (214, 168, 146)
DUCK = (246, 214, 140); BEAK = (240, 170, 120)


def wrinkle_lines(d, x0, x1, ytop, k, n=3, gap=13, width=4):
    """손끝 패드 위 가로 주름. k(0~1)만큼 길이·개수가 늘어남."""
    if k <= 0.02: return
    cx = (x0+x1)/2; half = (x1-x0)/2*0.72
    for j in range(n):
        kk = max(0, min(1, k*n-j))
        if kk <= 0: continue
        y = ytop+18+j*gap; h = half*kk
        d.arc([cx-h, y-8, cx+h, y+8], 200, 340, fill=WRINK, width=width)


def duck(d, x, y, s=1.0, t=0):
    y = y+math.sin(t*2.0)*6
    d.ellipse([x-46*s, y-24*s, x+46*s, y+26*s], fill=DUCK)
    d.ellipse([x+4*s, y-66*s, x+54*s, y-16*s], fill=DUCK)
    d.polygon([(x+50*s, y-44*s), (x+76*s, y-38*s), (x+50*s, y-30*s)], fill=BEAK)
    d.ellipse([x+30*s, y-52*s, x+40*s, y-42*s], fill=INK)


# ---------------- 장면 1: 저녁 목욕 ----------------
S1 = int(4.2*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), TILE); d = ImageDraw.Draw(im)
    for x in range(0, W, 120): d.line([x, 0, x, H], fill=TILE_L, width=3)
    for y in range(0, H, 120): d.line([0, y, W, y], fill=TILE_L, width=3)
    d.text((W/2, 80), '손이 할머니 손 됐어!', font=FBW, fill=TXT, anchor='mm')
    # 아이(어깨까지 물에 잠김)
    d.rounded_rectangle([360, 560, 600, 760], radius=70, fill=SKIN)
    # 들어 올린 팔(짧게, 어깨에서 손까지)
    lift = ease((t-0.3)/1.0)
    hx, hy = 650, 560-110*lift
    d.line([570, 620, hx, hy+40], fill=SKIN, width=52)
    d.ellipse([hx-46, hy-6, hx+46, hy+78], fill=SKIN)              # 손바닥
    k = 0.4+0.6*ease((t-1.0)/1.2)
    for j, (dx, L) in enumerate(((-33, 62), (-11, 74), (11, 72), (33, 60))):
        fx = hx+dx
        d.rounded_rectangle([fx-11, hy-L+10, fx+11, hy+20], radius=11, fill=SKIN)
        for m in range(3):
            if k*3-m > 0: d.line([fx-6, hy-L+22+m*9, fx+6, hy-L+22+m*9], fill=WRINK, width=3)
    face(d, 480, 450, 112, 0, mood='wow' if t > 1.4 else 'smile')
    # 욕조 + 물
    d.rounded_rectangle([90, 660, 990, 1020], radius=70, fill=TUB)
    d.rounded_rectangle([90, 660, 990, 700], radius=20, fill=TUB_D)
    d.rounded_rectangle([130, 640, 950, 690], radius=24, fill=WATER_T)
    duck(d, 820, 640, 0.9, t)
    for bx, by in ((220, 650), (270, 640), (700, 652)):
        d.ellipse([bx-16, by-16, bx+16, by+16], fill=(250, 252, 255))
    lab(im, '쭈글쭈글', (760, 300), LT, t, 1.6)
    return im


# ---------------- 장면 2: 같은 물 속, 어디가 쭈글? ----------------
SURF = 250
FINGERS = [(292, 205), (360, 240), (428, 228), (494, 180)]   # (x중심, 길이)
FW = 58
TOES = [(742, 38), (806, 30), (856, 27), (898, 24), (934, 20)]  # (x, 반지름)


def k_wrinkle(t, t0):
    return ease((t-t0)/4.0)


S2 = int(13.8*F)
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=TILE if yy < SURF else mix(WATER_T, WATER_B, (yy-SURF)/(H-SURF)))
    d.text((W/2, 80), '어디가 쭈글해질까?', font=FBW, fill=TXT, anchor='mm')
    # 물결 표면
    pts = [(x, SURF+math.sin(x/70+t*1.6)*8) for x in range(0, W+20, 20)]
    d.line(pts, fill=(240, 248, 252), width=8)
    # 손 + 팔(손바닥이 보이게, 아래로 화면 밖까지)
    d.rounded_rectangle([300, 760, 490, 1100], radius=80, fill=SKIN)
    d.rounded_rectangle([262, 520, 528, 820], radius=110, fill=SKIN)
    # 엄지(왼쪽 아래로 비스듬히)
    th = Image.new('RGBA', (120, 240), (0, 0, 0, 0)); ImageDraw.Draw(th).rounded_rectangle([20, 10, 100, 230], radius=40, fill=SKIN)
    th = th.rotate(38, expand=True, resample=Image.BICUBIC); im.paste(th, (130, 520), th); d = ImageDraw.Draw(im)
    kh = k_wrinkle(t, 1.6)
    for fx, L in FINGERS:
        top = 540-L
        d.rounded_rectangle([fx-FW/2, top, fx+FW/2, 600], radius=FW/2, fill=SKIN)
        wrinkle_lines(d, fx-FW/2, fx+FW/2, top+6, kh)
    # 손바닥 손금 두 줄(처음부터, 은은하게)
    d.arc([300, 600, 500, 700], 200, 330, fill=(236, 200, 180), width=4)
    d.arc([290, 640, 470, 760], 190, 300, fill=(236, 200, 180), width=4)
    # 발바닥(오른쪽)
    d.ellipse([720, 580, 940, 1000], fill=SKIN)
    d.ellipse([740, 820, 900, 1040], fill=SKIN)
    kf = k_wrinkle(t, 3.2)
    for x, r in TOES:
        cy = 560-r*0.2 if x != 742 else 556
        d.ellipse([x-r, cy-r*1.15, x+r, cy+r*1.15], fill=SKIN)
        wrinkle_lines(d, x-r, x+r, cy-r*1.15+2, kf, n=2 if r < 30 else 3, gap=11, width=3)
    # 물방울(천천히 올라감)
    rnd = random.Random(3)
    for b in range(9):
        bx = rnd.uniform(60, 1020); sp = rnd.uniform(30, 55); ph = rnd.uniform(0, 12)
        by = H-((t*sp+ph*60) % (H-SURF-40))
        if (110 < bx < 560 and by > 280) or (690 < bx < 970 and by > 500): continue
        r = rnd.uniform(8, 14)
        d.ellipse([bx-r, by-r, bx+r, by+r], outline=(236, 246, 252), width=4)
    lab(im, '손끝: 쭈글', (395, 210), LT, t, 4.2)
    lab(im, '발끝: 쭈글', (830, 430), LT, t, 6.0)
    lab(im, '팔: 매끈', (170, 930), LM, t, 7.8)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/wrinkly_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('wrinkly', s1, S1, s2, S2, out,
              preview=[(s1, int(3.0*F), S1), (s2, int(1.0*F), S2), (s2, int(5.0*F), S2), (s2, int(13.0*F), S2)])
