"""appa say: "Let's burp you."(수유 끝나고, 거실 소파). 한 장면 안에서만: 아빠가 소파에 앉아 둘째를
무릎에 세워 앉히고 한 손은 가슴을 받치고 다른 손으로 등을 토닥인다. 옆에 첫째가 앉아 지켜본다.
아빠가 천천히 → 보통 속도로 말하고 토닥토닥, 마지막 토닥일 때 한 번 더. 트림이 나오면(작은 방울)
옆에 선 엄마가 "Good burp!". 아이 목소리는 합성하지 않는다. 마지막 3초 멈춤.
사용: python3 example_say_lets_burp_you_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (242, 236, 228); FLOOR = (214, 204, 190)
SOFA = (196, 208, 232); SOFA_D = (176, 190, 220); WIN = (214, 232, 244)
DAD_SHIRT = (160, 200, 170); PANTS = (150, 170, 210); KID_SHIRT = (246, 214, 140)
MOM_SHIRT = (240, 196, 200); ONESIE = (255, 250, 240); HAIR = (120, 96, 82)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = "Let's burp you.", '트림시켜 줄게'
REPLY = 'Good burp!'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.2, 4.8, 9.4, 12.0
P0, P1 = 6.2, 11.0            # 토닥토닥
BURP = 11.2                   # 트림 나옴
TOTAL = 16.0
DX, KX, MX = 380, 650, 890
BY = 618                      # 둘째 얼굴 y


def room(d):
    d.rectangle([0, 0, W, 960], fill=WALL)
    d.rounded_rectangle([560, 250, 760, 420], radius=16, fill=WIN)          # 창(오른쪽 위, 첫째 뒤)
    d.line([660, 250, 660, 420], fill=WALL, width=8)
    d.rectangle([0, 960, W, H], fill=FLOOR)
    d.rounded_rectangle([110, 560, 790, 820], radius=50, fill=SOFA)        # 등받이
    d.rounded_rectangle([90, 770, 810, 880], radius=30, fill=SOFA_D)       # 앉는 곳
    d.rounded_rectangle([70, 700, 150, 900], radius=30, fill=SOFA_D)       # 팔걸이
    d.rounded_rectangle([750, 700, 830, 900], radius=30, fill=SOFA_D)
    d.rectangle([120, 880, 150, 940], fill=SOFA_D); d.rectangle([750, 880, 780, 940], fill=SOFA_D)


def pat_off(t):
    if P0 <= t <= P1 and t < BURP:
        return -14*abs(math.sin((t-P0)*math.pi*1.6))      # 천천히 토닥(약 0.6초에 한 번)
    return 0


def dad(d, t):
    cx = DX
    for dx in (-36, 36):                                   # 아래 다리
        d.rounded_rectangle([cx+dx-26, 800, cx+dx+26, 975], radius=22, fill=PANTS)
        d.ellipse([cx+dx-32, 960, cx+dx+32, 992], fill=SKIN)
    d.rounded_rectangle([cx-104, 750, cx+104, 820], radius=30, fill=PANTS)   # 무릎(앞에서 본 허벅지)
    d.rounded_rectangle([cx-96, 530, cx+96, 780], radius=60, fill=DAD_SHIRT)
    # 오른팔: 둘째 등 뒤로 짧게(토닥이는 손이 둘째 옆구리 뒤로 살짝 보임)
    po = pat_off(t)
    sx, sy = cx+84, 575; hx, hy = cx+62, 676+po
    d.line([sx, sy, hx, hy], fill=DAD_SHIRT, width=42)
    d.ellipse([sx-21, sy-21, sx+21, sy+21], fill=DAD_SHIRT)
    d.ellipse([hx-24, hy-22, hx+24, hy+22], fill=SKIN)
    # 왼팔: 몸 앞으로 짧게(둘째 가슴 받침, 손은 baby() 뒤에 그림)
    d.line([cx-84, 575, cx-62, 700], fill=DAD_SHIRT, width=42)
    d.ellipse([cx-105, 554, cx-63, 596], fill=DAD_SHIRT)
    face(d, cx, 450, 86, 0, mood='smile')
    for on_, dur in ((T_SLOW, 1.6), (T_NORM, 1.1), (T_AGAIN, 1.1)):
        if on_ <= t <= on_+dur:
            for j in range(3):
                r = 18+j*16+6*math.sin((t-on_)*8-j)
                d.arc([cx-112-r, 430-r, cx-112+r, 430+r], 140, 220, fill=(232, 150, 120), width=6)


def baby(d, t):
    cx = DX
    d.rounded_rectangle([cx-54, 650, cx+54, 770], radius=40, fill=ONESIE, outline=(226, 220, 210), width=3)
    for dx in (-26, 26):                                   # 둘째 발(무릎 위)
        d.ellipse([cx+dx-18, 756, cx+dx+18, 784], fill=ONESIE, outline=(226, 220, 210), width=3)
    burp = BURP <= t <= BURP+1.2
    face(d, cx, BY, 46, 0, mood='wow' if burp else 'smile', baby=True)
    d.ellipse([cx-62, 680, cx-14, 722], fill=SKIN)         # 아빠 왼손(가슴 받침)
    if BURP <= t <= BURP+2.0:                              # 트림 방울
        k = (t-BURP)/2.0
        for j, (ox, oy, r) in enumerate(((64, -4, 12), (92, -32, 17), (126, -62, 22))):
            if k > j*0.15:
                a = 1-max(0, (k-0.6)/0.4)
                c = tuple(int(255-(255-v)*a) for v in (140, 160, 210))
                d.ellipse([cx+ox-r, BY+oy-r-k*20, cx+ox+r, BY+oy+r-k*20], outline=c, width=6)


def kid(d, t):
    cx = KX
    for dx in (-24, 24):
        d.rounded_rectangle([cx+dx-20, 800, cx+dx+20, 905], radius=18, fill=PANTS)
        d.ellipse([cx+dx-24, 892, cx+dx+24, 916], fill=SKIN)
    d.rounded_rectangle([cx-64, 770, cx+64, 820], radius=24, fill=PANTS)
    d.rounded_rectangle([cx-66, 625, cx+66, 790], radius=42, fill=KID_SHIRT)
    for dx in (-1, 1):                                     # 짧은 팔, 무릎 위 손
        x0 = cx+dx*62
        d.rounded_rectangle([x0-18, 645, x0+18, 760], radius=18, fill=KID_SHIRT)
        d.ellipse([x0-17, 748, x0+17, 780], fill=SKIN)
    mood = 'wow' if BURP <= t <= BURP+1.4 else 'smile'
    face(d, cx, 562, 66, 0, mood=mood)


def mom(d, t):
    cx = MX
    d.rounded_rectangle([cx-86, 450, cx+86, 610], radius=40, fill=HAIR)
    for dx in (-28, 28):
        d.rounded_rectangle([cx+dx-22, 790, cx+dx+22, 975], radius=20, fill=PANTS)
        d.ellipse([cx+dx-28, 960, cx+dx+28, 990], fill=SKIN)
    d.rounded_rectangle([cx-80, 590, cx+80, 810], radius=54, fill=MOM_SHIRT)
    for dx in (-1, 1):
        x0 = cx+dx*80
        d.rounded_rectangle([x0-18, 610, x0+18, 730], radius=18, fill=MOM_SHIRT)
        d.ellipse([x0-17, 718, x0+17, 752], fill=SKIN)
    face(d, cx, 505, 76, 0, mood='smile')
    if T_MOM <= t <= T_MOM+0.9:
        for j in range(3):
            r = 18+j*16+6*math.sin((t-T_MOM)*8-j)
            d.arc([cx-96-r, 490-r, cx-96+r, 490+r], 140, 220, fill=(232, 150, 120), width=6)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    room(d)
    d.text((W/2, 70), '수유 끝나고, 거실 소파', font=FTI, fill=TXT, anchor='mm')
    kid(d, t); dad(d, t); baby(d, t); mom(d, t)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 190, a, min(1, max(0, (t-3.4)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        w = dl.textlength(REPLY, font=FSM); cx = min(MX-30, W-w/2-50)
        dl.rounded_rectangle([cx-w/2-30, 364, cx+w/2+30, 418], radius=28, fill=(255, 255, 255, int(230*b)), outline=(240, 196, 200, int(255*b)), width=4)
        dl.text((cx, 391), REPLY, font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts(REPLY, MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('lets_burp_you', scene, TOTAL, clips, out, preview=pv, preview_times=(1.0, 7.0, 11.8, 15.5))
