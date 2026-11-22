"""appa say: "Bath time!"(저녁, 욕실). 한 장면 안에서만: 욕조에 물이 받아져 있고, 아빠가 둘째를 안고 서서 말한다.
엄마는 욕조 뒤에 앉아 물에 손을 넣어 온도를 보고, 첫째가 고무 오리를 욕조에 넣으면 '첨벙'.
오리가 물에 뜨면 아빠가 한 번 더, 엄마가 "Nice and warm."
소리: 아빠 목소리로 천천히 → 보통 속도 → (오리가 뜬 뒤) 한 번 더 → 엄마 대답.
사용: python3 example_say_bath_time_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (226, 238, 244); TILE = (210, 226, 236); FLOOR = (214, 220, 230)
TUB = (250, 250, 252); TUB_D = (222, 226, 236); WATER = (180, 214, 238); WATER_L = (206, 230, 246)
DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 214, 140); PANTS = (150, 170, 210)
MOM_SHIRT = (240, 196, 200); MOM_HAIR = (110, 86, 76); ONESIE = (220, 200, 232)
DUCK = (250, 214, 90); BEAK = (240, 150, 90); INKC = (80, 76, 90)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = 'Bath time!', '목욕할 시간이야'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.4, 4.9, 9.4, 11.1
T_THROW, T_LAND = 6.9, 7.9
TOTAL = 15.4
HAND0 = (930, 800)            # 첫째 손(오리 들고 있음)
LAND = (720, 836)             # 오리가 뜨는 자리


def lerp(a, b, k): return a+(b-a)*k


def duck(d, x, y, s=1.0):
    d.ellipse([x-38*s, y-22*s, x+38*s, y+22*s], fill=DUCK)
    d.ellipse([x-34*s, y-58*s, x+2*s, y-22*s], fill=DUCK)
    d.polygon([(x-34*s, y-44*s), (x-52*s, y-38*s), (x-34*s, y-32*s)], fill=BEAK)
    d.ellipse([x-22*s, y-48*s, x-14*s, y-40*s], fill=INKC)


def duck_pos(t):
    if t < T_THROW: return HAND0[0], HAND0[1]-30, 'hand'
    k = ease((t-T_THROW)/(T_LAND-T_THROW))
    if k < 1:
        return lerp(HAND0[0], LAND[0], k), lerp(HAND0[1]-30, LAND[1], k)-120*math.sin(k*math.pi), 'air'
    return LAND[0], LAND[1]+4*math.sin((t-T_LAND)*3), 'float'


def kid_hand(t):
    if t < T_THROW: return HAND0
    k = ease((t-T_THROW)/0.5)            # 놓고 나면 손이 앞으로 살짝 나갔다 돌아옴
    b = ease((t-T_THROW-0.6)/0.6)
    x = lerp(HAND0[0], 870, k); y = lerp(HAND0[1], 770, k)
    return lerp(x, HAND0[0], b), lerp(y, HAND0[1]+20, b)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    for y in range(120, 900, 90): d.line([0, y, W, y], fill=TILE, width=3)
    for x in range(0, W, 90): d.line([x, 120, x, 900], fill=TILE, width=3)
    d.rectangle([0, 0, W, 116], fill=WALL)
    d.text((W/2, 70), '저녁, 욕조에 물 받은 뒤', font=FTI, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=FLOOR)
    # ── 엄마: 욕조 뒤에 앉음(욕조가 아랫몸을 가림)
    d.rounded_rectangle([574, 540, 718, 680], radius=50, fill=MOM_HAIR)           # 어깨까지 오는 머리
    d.rounded_rectangle([576, 640, 716, 860], radius=56, fill=MOM_SHIRT)
    face(d, 646, 566, 68, 0, mood='smile', hair=MOM_HAIR)
    # ── 욕조
    d.rounded_rectangle([370, 790, 880, 990], radius=60, fill=TUB)
    d.rounded_rectangle([392, 812, 858, 880], radius=30, fill=WATER)
    # 엄마 손(물에 담금): 어깨 → 물 표면
    d.line([(592, 690), (548, 838)], fill=MOM_SHIRT, width=36)
    d.ellipse([574, 672, 610, 708], fill=MOM_SHIRT)
    d.ellipse([528, 826, 568, 858], fill=SKIN)
    d.rounded_rectangle([392, 846, 858, 880], radius=16, fill=WATER)        # 손목 아래는 물속
    for j in range(2):                                                       # 손 둘레 잔물결
        r = 30+j*18+6*math.sin(t*3+j)
        d.arc([548-r, 846-r*0.3, 548+r, 846+r*0.3], 0, 180, fill=WATER_L, width=4)
    d.rounded_rectangle([370, 880, 880, 990], radius=50, fill=TUB)
    d.line([400, 884, 850, 884], fill=TUB_D, width=6)
    for x in (430, 820): d.rounded_rectangle([x-20, 980, x+20, 1010], radius=10, fill=TUB_D)
    # 김(물 위로 살짝)
    for i, x in enumerate((440, 800)):
        ph = (t*0.6+i*0.33) % 1
        y0 = 800-ph*90
        col = tuple(int(c+(255-c)*ph) for c in (200, 214, 226))
        d.arc([x-14, y0-30, x+14, y0], 90, 270, fill=col, width=5)
        d.arc([x-14, y0-60, x+14, y0-30], 270, 90, fill=col, width=5)
    # ── 오리
    dx, dy, st = duck_pos(t)
    if st == 'float':
        duck(d, dx, dy-6)
        d.rounded_rectangle([dx-48, dy+6, dx+48, dy+30], radius=12, fill=WATER)   # 아랫부분 물에 잠김
    # 첨벙 물방울
    if T_LAND <= t < T_LAND+0.9:
        a = (t-T_LAND)/0.9
        for ang in (-60, -30, 0, 30, 60):
            c, s = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
            r = 30+80*a; px = LAND[0]+c*r; py = LAND[1]+s*r*0.9+120*a*a
            d.ellipse([px-8, py-10, px+8, py+10], fill=WATER)
        for j in range(2):
            r = 40+60*a+j*20
            d.arc([LAND[0]-r, LAND[1]+10-r*0.25, LAND[0]+r, LAND[1]+10+r*0.25], 0, 180, fill=WATER_L, width=4)
    # ── 첫째: 오른쪽에 서 있음
    d.rounded_rectangle([912, 850, 958, 1000], radius=22, fill=PANTS)
    d.rounded_rectangle([972, 850, 1018, 1000], radius=22, fill=PANTS)
    d.ellipse([904, 986, 964, 1012], fill=SKIN); d.ellipse([966, 986, 1026, 1012], fill=SKIN)
    d.rounded_rectangle([900, 660, 1030, 870], radius=54, fill=KID_SHIRT)
    d.rounded_rectangle([1024, 690, 1060, 810], radius=18, fill=KID_SHIRT)     # 반대 팔(몸 옆)
    d.ellipse([1024, 796, 1060, 830], fill=SKIN)
    hx, hy = kid_hand(t); sx, sy = 920, 700
    d.line([sx, sy, hx, hy], fill=KID_SHIRT, width=38)
    d.ellipse([sx-19, sy-19, sx+19, sy+19], fill=KID_SHIRT)
    if st == 'hand': duck(d, dx, dy, 0.85)
    d.ellipse([hx-20, hy-18, hx+20, hy+18], fill=SKIN)
    if st == 'air': duck(d, dx, dy, 0.9)
    face(d, 965, 584, 74, 0, mood='wow' if T_LAND <= t < T_LAND+1.4 else 'smile')
    # ── 아빠: 왼쪽에 서서 둘째를 안음
    d.rounded_rectangle([110, 750, 166, 990], radius=26, fill=PANTS)
    d.rounded_rectangle([186, 750, 242, 990], radius=26, fill=PANTS)
    d.ellipse([100, 970, 176, 1004], fill=SKIN); d.ellipse([176, 970, 252, 1004], fill=SKIN)
    d.rounded_rectangle([80, 520, 272, 780], radius=70, fill=DAD_SHIRT)
    # 둘째(가슴 앞에 가로로 안김, 머리는 오른쪽 = 욕조 쪽)
    d.rounded_rectangle([120, 610, 290, 690], radius=40, fill=ONESIE)
    face(d, 306, 626, 46, 0, mood='wow' if t > T_LAND else 'flat', baby=True)
    # 아빠 팔: 아기 몸 아래로 받침
    d.rounded_rectangle([96, 672, 300, 712], radius=20, fill=DAD_SHIRT)
    d.ellipse([290, 668, 330, 712], fill=SKIN)
    d.rounded_rectangle([60, 540, 106, 690], radius=23, fill=DAD_SHIRT)
    face(d, 176, 436, 88, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.2), (T_NORM, 0.9), (T_AGAIN, 0.9)):
        speak_mark(d, 290, 420, t, on, on+dur)
    if T_MOM <= t <= T_MOM+1.0:
        for j in range(3):
            r = 16+j*14+6*math.sin((t-T_MOM)*8-j)
            d.arc([724-r, 566-r, 724+r, 566+r], -40, 40, fill=(232, 150, 120), width=6)
    # 영어 카드(위쪽, 얼굴과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.1)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        txt = 'Nice and warm.'; w = dl.textlength(txt, font=FSM); cx = 700
        dl.rounded_rectangle([cx-w/2-30, 410, cx+w/2+30, 470], radius=30, fill=(255, 255, 255, int(225*b)))
        dl.text((cx, 440), txt, font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts('Nice and warm.', MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('bath_time', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.4, 7.5, 12.0))
