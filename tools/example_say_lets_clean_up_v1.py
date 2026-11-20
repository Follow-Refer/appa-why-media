"""appa say: "Let's clean up."(거실, 저녁 먹기 전). 한 장면 안에서만: 아빠가 말하면 바닥에 앉은 첫째가
블록 세 개를 하나씩 장난감 상자에 넣고, 옆 바운서의 둘째가 그걸 본다. 다 넣으면 엄마가 "Great job!".
소리: 아빠 목소리로 천천히 → 보통 속도 → (다 치운 뒤) 한 번 더 → 엄마 대답.
사용: python3 example_say_lets_clean_up_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (240, 236, 246); FLOOR = (222, 210, 194); RUG = (214, 232, 244)
DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 214, 140); PANTS = (150, 170, 210)
BOX = (232, 170, 150); BOX_D = (214, 150, 132); BOUNCER = (200, 214, 236); BOUNCER_D = (176, 194, 224)
ONESIE = (220, 200, 232); MOM_SHIRT = (240, 196, 200); MOM_HAIR = (110, 86, 76)
BLOCKS = [((470, 990), (246, 200, 120)), ((560, 1004), (160, 200, 170)), ((650, 992), (140, 160, 210))]
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = "Let's clean up.", '이제 치우자'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.4, 5.0, 10.8, 12.4
T_PUT = (6.6, 7.8, 9.0)       # 블록마다 집기 시작
DUR = 1.1
TOTAL = 16.0
BOXIN = (790, 850)            # 상자 입구 가운데
REST = (650, 860)             # 손 쉬는 자리(무릎 앞)
SH = (610, 760)               # 첫째 오른쪽 어깨


def lerp(a, b, k): return a+(b-a)*k


def block_pos(i, t):
    (x0, y0), _ = BLOCKS[i]; t0 = T_PUT[i]
    if t < t0+0.25: return (x0, y0), 'floor'
    k = ease((t-t0-0.25)/(DUR-0.25))
    if k >= 1: return None, 'in'
    x = lerp(x0, BOXIN[0], k); y = lerp(y0, BOXIN[1]-30, k)-90*math.sin(k*math.pi)
    return (x, y), 'hand'


def hand(t):
    for i, t0 in enumerate(T_PUT):
        if t0 <= t < t0+DUR+0.2:
            (x0, y0), _ = BLOCKS[i]
            if t < t0+0.25:                       # 블록 쪽으로 손을 내림
                k = ease((t-t0)/0.25); return lerp(REST[0], x0, k), lerp(REST[1], y0-30, k)
            p, st = block_pos(i, t)
            if st == 'hand': return p[0], p[1]-30
            k = ease((t-t0-DUR)/0.2); return lerp(BOXIN[0], REST[0], k), lerp(BOXIN[1]-60, REST[1], k)
    return REST


def block(d, x, y, col):
    d.rounded_rectangle([x-30, y-30, x+30, y+30], radius=10, fill=col)
    d.rounded_rectangle([x-18, y-18, x+18, y+18], radius=6, outline=(255, 255, 255), width=4)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.text((W/2, 70), '거실, 저녁 먹기 전', font=FTI, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=FLOOR)
    d.rounded_rectangle([380, 930, 1000, 1060], radius=40, fill=RUG)
    # ── 엄마: 오른쪽 뒤에 서 있음(바운서 뒤)
    d.rounded_rectangle([900, 560, 1060, 900], radius=60, fill=MOM_SHIRT)
    face(d, 980, 476, 70, 0, mood='smile', hair=MOM_HAIR)
    if T_MOM <= t <= T_MOM+0.9:
        for j in range(3):
            r = 16+j*14+6*math.sin((t-T_MOM)*8-j)
            d.arc([902-r, 476-r, 902+r, 476+r], 140, 220, fill=(232, 150, 120), width=6)
    # ── 둘째: 바운서(오른쪽 아래)
    d.chord([860, 760, 1060, 1000], 150, 390, fill=BOUNCER)
    d.rounded_rectangle([870, 960, 1050, 990], radius=14, fill=BOUNCER_D)
    d.rounded_rectangle([920, 840, 1010, 950], radius=36, fill=ONESIE)
    look = any(T_PUT[0] <= t < T_PUT[-1]+DUR+0.6 for _ in [0])
    face(d, 960, 800, 50, 0, mood='wow' if look else ('smile' if t > T_PUT[-1] else 'flat'), baby=True)
    # ── 장난감 상자
    d.rounded_rectangle([700, 850, 880, 990], radius=18, fill=BOX)
    d.rounded_rectangle([690, 836, 890, 866], radius=12, fill=BOX_D)
    n_in = sum(1 for i in range(3) if block_pos(i, t)[1] == 'in')
    for j in range(n_in):                               # 상자 위로 살짝 보이는 블록
        d.rounded_rectangle([724+j*52, 812, 770+j*52, 846], radius=8, fill=BLOCKS[j][1])
    d.rounded_rectangle([690, 836, 890, 866], radius=12, fill=BOX_D)
    # ── 첫째: 바닥에 앉음(가운데)
    d.rounded_rectangle([480, 900, 680, 960], radius=28, fill=PANTS)       # 접은 다리
    d.rounded_rectangle([490, 720, 640, 930], radius=56, fill=KID_SHIRT)
    d.rounded_rectangle([470, 760, 510, 880], radius=20, fill=KID_SHIRT)   # 왼팔(몸 옆)
    d.ellipse([470, 866, 510, 902], fill=SKIN)
    # 바닥 블록(손에 든 건 나중에)
    held = None
    for i in range(3):
        p, st = block_pos(i, t)
        if st == 'floor': block(d, *p, BLOCKS[i][1])
        elif st == 'hand': held = (p, BLOCKS[i][1])
    hx, hy = hand(t)
    d.line([SH, (hx, hy)], fill=KID_SHIRT, width=40)
    d.ellipse([SH[0]-20, SH[1]-20, SH[0]+20, SH[1]+20], fill=KID_SHIRT)
    if held: block(d, *held[0], held[1])
    d.ellipse([hx-22, hy-20, hx+22, hy+20], fill=SKIN)
    face(d, 566, 640, 80, 0, mood='smile')
    # 블록이 들어갈 때 작은 반짝임
    for i, t0 in enumerate(T_PUT):
        te = t0+DUR
        if te <= t < te+0.6:
            a = (t-te)/0.6; r = 14+10*a
            for ang in range(0, 360, 90):
                c, s = math.cos(math.radians(ang+45)), math.sin(math.radians(ang+45))
                d.line([BOXIN[0]+c*r*2, 800+s*r, BOXIN[0]+c*(r*2+12), 800+s*(r+12)], fill=(232, 150, 120), width=5)
    # ── 아빠: 왼쪽에 서 있음
    d.rounded_rectangle([110, 740, 166, 990], radius=26, fill=PANTS)
    d.rounded_rectangle([186, 740, 242, 990], radius=26, fill=PANTS)
    d.ellipse([100, 970, 176, 1004], fill=SKIN); d.ellipse([176, 970, 252, 1004], fill=SKIN)
    d.rounded_rectangle([80, 520, 272, 770], radius=70, fill=DAD_SHIRT)
    for xa in (68, 284):
        d.rounded_rectangle([xa-24, 540, xa+24, 690], radius=24, fill=DAD_SHIRT)
        d.ellipse([xa-22, 676, xa+22, 720], fill=SKIN)
    face(d, 176, 432, 90, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.5), (T_NORM, 1.1), (T_AGAIN, 1.1)):
        speak_mark(d, 290, 432, t, on, on+dur)
    # 영어 카드(위쪽, 얼굴과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.2)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        w = dl.textlength('Great job!', font=FSM); cx = 1060-w/2-36
        dl.rounded_rectangle([cx-w/2-30, 326, cx+w/2+30, 386], radius=30, fill=(255, 255, 255, int(220*b)))
        dl.text((cx, 356), 'Great job!', font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts('Great job!', MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('lets_clean_up', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.6, 8.3, 13.0))
