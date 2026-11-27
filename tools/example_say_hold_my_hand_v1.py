"""appa say: "Hold my hand."(산책 가는 길, 주차장 옆). 한 장면 안에서만: 아빠가 길가에 서서 손을 내밀며 말하고,
주차된 차를 보던 첫째가 아빠 옆으로 걸어와 손을 잡는다. 오른쪽엔 엄마가 둘째가 탄 유모차를 밀고 서 있다.
소리: 아빠 목소리로 천천히 → 보통 속도 → (손을 잡으면) 한 번 더. 아이 목소리는 합성하지 않는다. 마지막 3초 멈춤.
사용: python3 example_say_hold_my_hand_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); SKY = (222, 232, 244); BLD = (232, 226, 236); WIN = (214, 232, 244)
ROAD = (214, 210, 220); WALK = (236, 228, 214); LINE = (250, 248, 252)
CAR = (196, 208, 232); CAR_D = (170, 186, 218); TIRE = (120, 116, 132)
DAD_SHIRT = (160, 200, 170); KID_SHIRT = (246, 214, 140); MOM_SHIRT = (240, 196, 200)
PANTS = (150, 170, 210); HAIR = (120, 96, 82); STROLLER = (214, 196, 232); STROLLER_D = (190, 170, 214)
TREE = (170, 206, 176); TRUNK = (196, 170, 150)

EN, KO = 'Hold my hand.', '손 잡자'
T_SLOW, T_NORM, T_AGAIN = 2.2, 4.8, 9.2
W0, W1 = 6.6, 8.8            # 첫째가 걸어오는 시간
TOTAL = 14.5
DX = 300                     # 아빠
K0, K1 = 650, 565            # 첫째 x: 처음 → 아빠 옆
MX = 1000                    # 엄마
GY = 1000                    # 발 높이


def backdrop(d):
    d.rectangle([0, 0, W, 700], fill=SKY)
    d.rounded_rectangle([600, 300, 1040, 720], radius=20, fill=BLD)        # 아파트(뒤)
    for r in range(3):
        for c in range(4):
            x = 640+c*100; y = 330+r*110
            d.rounded_rectangle([x, y, x+60, y+60], radius=8, fill=WIN)
    d.rectangle([60, 520, 84, 720], fill=TRUNK); d.ellipse([0, 400, 150, 560], fill=TREE)   # 나무(왼쪽 뒤)
    d.rectangle([0, 700, W, 860], fill=ROAD)                               # 주차장 바닥
    for x in (80, 420, 760):
        d.line([x, 720, x, 850], fill=LINE, width=8)
    # 주차된 차(가운데 뒤, 서 있음)
    d.rounded_rectangle([430, 640, 760, 790], radius=40, fill=CAR)
    d.rounded_rectangle([490, 580, 700, 680], radius=34, fill=CAR)
    d.rounded_rectangle([515, 600, 590, 660], radius=12, fill=WIN); d.rounded_rectangle([605, 600, 680, 660], radius=12, fill=WIN)
    for x in (500, 690):
        d.ellipse([x-38, 760, x+38, 836], fill=TIRE)
    d.rectangle([0, 860, W, H], fill=WALK)                                 # 인도
    d.line([0, 860, W, 860], fill=CAR_D, width=6)


def arm(d, sx, sy, hx, hy, col):
    d.line([sx, sy, hx, hy], fill=col, width=40)
    d.ellipse([sx-20, sy-20, sx+20, sy+20], fill=col)
    d.ellipse([hx-23, hy-22, hx+23, hy+22], fill=SKIN)


def dad(d, t):
    cx = DX
    for dx in (-36, 36):
        d.rounded_rectangle([cx+dx-28, 740, cx+dx+28, GY], radius=26, fill=PANTS)
        d.ellipse([cx+dx-32, GY-20, cx+dx+32, GY+12], fill=SKIN)
    d.rounded_rectangle([cx-100, 500, cx+100, 760], radius=70, fill=DAD_SHIRT)
    arm(d, cx-90, 530, cx-118, 700, DAD_SHIRT)                              # 왼팔: 몸 옆
    k = ease((t-T_SLOW)/0.8)                                                # 오른손: 살짝 앞으로 내밀기
    arm(d, cx+90, 530, cx+118+32*k, 700+60*k, DAD_SHIRT)
    face(d, cx, 410, 96, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.5), (T_NORM, 1.1), (T_AGAIN, 1.1)):
        if on <= t <= on+dur:
            for j in range(3):
                r = 18+j*16+6*math.sin((t-on)*8-j)
                d.arc([cx-126-r, 410-r, cx-126+r, 410+r], 140, 220, fill=(232, 150, 120), width=6)


def kid(d, t):
    p = ease((t-W0)/(W1-W0)); cx = K0+(K1-K0)*p
    walking = W0 < t < W1
    bob = -6*abs(math.sin((t-W0)*math.pi*2.2)) if walking else 0
    s = 0.95; hip = GY-130*s; sh = hip-170*s+bob
    for j, dx in enumerate((-28, 28)):
        lift = (8*math.sin((t-W0)*math.pi*2.2+j*math.pi)) if walking else 0
        d.rounded_rectangle([cx+dx-21, hip-10, cx+dx+21, GY-max(0, lift)], radius=19, fill=PANTS)
        d.ellipse([cx+dx-27, GY-18-max(0, lift), cx+dx+27, GY+8-max(0, lift)], fill=SKIN)
    d.rounded_rectangle([cx-68, sh, cx+68, hip+17], radius=44, fill=KID_SHIRT)
    arm(d, cx+68, sh+26, cx+80, sh+136, KID_SHIRT)                          # 오른팔: 몸 옆
    if t >= W1:                                                             # 왼손: 아빠 손 잡음
        hx, hy = DX+150, 760
        d.line([cx-62, sh+26, hx+22, hy], fill=KID_SHIRT, width=36)
        d.ellipse([cx-80, sh+8, cx-44, sh+44], fill=KID_SHIRT)
        d.ellipse([hx+2, hy-20, hx+44, hy+20], fill=SKIN)
    else:
        arm(d, cx-68, sh+26, cx-80, sh+136, KID_SHIRT)
    look = 'wow' if t < 2.0 else 'smile'
    face(d, cx, sh-66+8, 74, 0, mood=look)


def mom(d, t):
    cx = MX
    d.rounded_rectangle([cx-80, 470, cx+80, 620], radius=40, fill=HAIR)
    for dx in (-26, 26):
        d.rounded_rectangle([cx+dx-21, 780, cx+dx+21, GY], radius=19, fill=PANTS)
        d.ellipse([cx+dx-27, GY-18, cx+dx+27, GY+10], fill=SKIN)
    d.rounded_rectangle([cx-76, 600, cx+76, 810], radius=52, fill=MOM_SHIRT)
    face(d, cx, 520, 74, 0, mood='smile')
    # 유모차(엄마 앞, 왼쪽): 바구니 + 차양 + 바퀴, 손잡이는 엄마 손으로
    d.line([cx-60, 690, cx-130, 760], fill=STROLLER_D, width=12)
    d.ellipse([cx-82, 672, cx-46, 708], fill=SKIN)
    d.rounded_rectangle([cx-270, 770, cx-110, 900], radius=46, fill=STROLLER)
    d.pieslice([cx-270, 704, cx-150, 830], 180, 300, fill=STROLLER_D)
    face(d, cx-185, 800, 32, 0, mood='smile', baby=True)
    for x in (cx-245, cx-135):
        d.ellipse([x-30, 930, x+30, 990], outline=TIRE, width=10)
    d.line([cx-245, 900, cx-245, 932], fill=STROLLER_D, width=8); d.line([cx-135, 900, cx-135, 932], fill=STROLLER_D, width=8)


def scene(t):
    im = Image.new('RGB', (W, H), SKY); d = ImageDraw.Draw(im)
    backdrop(d)
    d.text((W/2, 70), '산책 가는 길, 주차장 옆', font=FTI, fill=TXT, anchor='mm')
    mom(d, t); dad(d, t); kid(d, t)
    if t >= W1:                                                             # 잡은 손 위 작은 반짝임
        b = min(1, (t-W1)/0.5)
        c = tuple(int(255-(255-v)*b) for v in (246, 190, 120))
        x, y = DX+150, 700
        d.line([x, y-18, x, y+18], fill=c, width=6); d.line([x-18, y, x+18, y], fill=c, width=6)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 190, a, min(1, max(0, (t-3.4)/0.6)))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('hold_my_hand', scene, TOTAL, clips, out, preview=pv, preview_times=(1.0, 5.5, 7.7, 13.5))
