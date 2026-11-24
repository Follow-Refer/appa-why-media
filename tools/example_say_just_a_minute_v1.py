"""appa say: "Just a minute."(저녁, 분유 타는 중). 한 장면 안에서만: 아빠는 부엌 조리대 앞에서 젖병을 흔들고,
바운서의 둘째는 칭얼, 첫째는 그림을 들고 "이거 봐!" 한다. 아빠가 천천히 → 보통 속도로 말하면
첫째가 그림을 내려 안고 기다린다(행동이 끝날 때 한 번 더). 젖병이 다 되면 아빠가 "Thanks for waiting."
아이 목소리는 합성하지 않는다. 마지막 3초 멈춤.
사용: python3 example_say_just_a_minute_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (238, 232, 240); FLOOR = (214, 204, 186)
COUNTER = (226, 214, 200); COUNTER_TOP = (246, 240, 232); CAB = (214, 228, 236)
DAD_SHIRT = (160, 190, 170); PANTS = (150, 170, 210)
KID_SHIRT = (246, 214, 140); PAPER = (255, 255, 255)
BOUNCER = (214, 232, 244); BOUNCER_D = (180, 204, 226); ONESIE = (240, 196, 200)
MILK = (252, 248, 236); BOTTLE = (232, 236, 246); CAP = (176, 200, 236)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = 'Just a minute.', '잠깐만 기다려 줘'
T_SLOW, T_NORM, T_AGAIN, T_THX = 2.4, 4.8, 8.8, 11.0
SH0, SH1 = 1.0, 10.4          # 젖병 흔드는 시간
P0, P1 = 6.6, 8.4             # 첫째가 그림을 내려 안는 시간
TOTAL = 15.6
DX = 300                      # 아빠 몸 가운데
KX = 850                      # 첫째 몸 가운데


def kitchen(d):
    d.rectangle([0, 0, W, 930], fill=WALL)
    d.rounded_rectangle([40, 700, 600, 940], radius=18, fill=COUNTER)
    d.rectangle([40, 690, 600, 716], fill=COUNTER_TOP)
    for x in (60, 330):
        d.rounded_rectangle([x, 740, x+250, 920], radius=14, fill=CAB)
        d.ellipse([x+115, 820, x+135, 840], fill=COUNTER)
    d.rectangle([0, 930, W, H], fill=FLOOR)


def bottle_pos(t):
    if SH0 <= t <= SH1:
        k = min(1, (t-SH0)/0.4, (SH1-t)/0.4)
        return DX, 670+22*math.sin((t-SH0)*2*math.pi*2.2)*k
    return DX, 670


def dad(d, t):
    cx = DX
    d.rounded_rectangle([cx-96, 560, cx+96, 790], radius=62, fill=DAD_SHIRT)   # 몸(다리는 조리대 뒤)
    bx, by = bottle_pos(t)
    # 팔: 어깨에서 가슴 앞 젖병까지 짧게
    for sx in (cx-84, cx+84):
        d.line([sx, 600, bx+(sx-cx)*0.32, by+30], fill=DAD_SHIRT, width=44)
        d.ellipse([sx-22, 578, sx+22, 622], fill=DAD_SHIRT)
    # 젖병
    d.rounded_rectangle([bx-30, by-56, bx+30, by+70], radius=18, fill=BOTTLE, outline=BOTTLE_D, width=4)
    d.rounded_rectangle([bx-26, by-8, bx+26, by+66], radius=14, fill=MILK)
    d.rounded_rectangle([bx-34, by-74, bx+34, by-50], radius=10, fill=CAP)
    d.ellipse([bx-14, by-100, bx+14, by-68], fill=(246, 214, 140))
    for sx in (-1, 1):
        hx = bx+sx*30
        d.ellipse([hx-22, by+6, hx+22, by+50], fill=SKIN)
    face(d, cx, 470, 86, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.6), (T_NORM, 1.1), (T_AGAIN, 1.1), (T_THX, 1.2)):
        speak_mark(d, cx+118, 450, t, on, on+dur)
    if SH1 <= t <= SH1+1.6:                  # 다 됐다는 작은 반짝임
        a = 1-(t-SH1)/1.6
        for ang in range(0, 360, 60):
            r0, r1 = 50, 50+22*a
            x0 = bx+r0*math.cos(math.radians(ang)); y0 = by-90+r0*math.sin(math.radians(ang))
            x1 = bx+r1*math.cos(math.radians(ang)); y1 = by-90+r1*math.sin(math.radians(ang))
            d.line([x0, y0, x1, y1], fill=(246, 200, 110), width=5)


BOTTLE_D = (200, 208, 226)


def baby(d, t):
    cx, cy = 540, 900
    d.ellipse([cx-120, 960, cx+120, 1000], fill=BOUNCER_D)                      # 받침
    d.polygon([(cx-130, 880), (cx+110, 820), (cx+130, 960), (cx-110, 980)], fill=BOUNCER)
    d.rounded_rectangle([cx-60, 870, cx+90, 950], radius=40, fill=ONESIE)
    fuss = t < SH1
    wob = 3*math.sin(t*9) if fuss else 0
    face(d, cx-70+wob, 880, 44, 0, mood='flat' if fuss else 'smile', baby=True)
    if fuss:                                                                     # 칭얼 물결(작게)
        for j in range(2):
            ph = (t*1.4+j*0.5) % 1
            r = 58+ph*26
            col = tuple(int(c*(1-ph)+w*ph) for c, w in zip((200, 180, 220), WALL))
            d.arc([cx-70-r, 880-r, cx-70+r, 880+r], 200, 250, fill=col, width=5)


def pk(t):
    return ease((t-P0)/(P1-P0))


def kid(d, t):
    gy = 1000
    for dx in (-26, 26):
        d.rounded_rectangle([KX+dx-22, 860, KX+dx+22, gy], radius=20, fill=PANTS)
        d.ellipse([KX+dx-30, gy-14, KX+dx+30, gy+12], fill=SKIN)
    d.rounded_rectangle([KX-70, 700, KX+70, 880], radius=44, fill=KID_SHIRT)
    k = pk(t)
    px = KX+112-112*k; py = 610+(800-610)*k        # 그림: 머리 옆(한 손) → 가슴 앞(두 손)
    d.rounded_rectangle([px-62, py-52, px+62, py+52], radius=8, fill=PAPER, outline=(220, 214, 226), width=3)
    d.ellipse([px+14, py-40, px+46, py-8], fill=(246, 214, 140))
    d.polygon([(px-44, py+6), (px-14, py-24), (px+16, py+6)], fill=(232, 150, 120))
    d.rectangle([px-38, py+6, px+10, py+40], fill=(160, 200, 170))
    # 오른팔: 종이 오른쪽 아래를 잡음 / 왼팔: 몸 옆 → 종이 왼쪽 아래
    rx, ry = px+40, py+44
    lx = (KX-84)*(1-k)+(px-40)*k; ly = 830*(1-k)+(py+44)*k
    for sx, hx, hy in ((KX+60, rx, ry), (KX-60, lx, ly)):
        d.line([sx, 724, hx, hy], fill=KID_SHIRT, width=30)
        d.ellipse([hx-16, hy-15, hx+16, hy+15], fill=SKIN)
    face(d, KX, 630, 68, 0, mood='wow' if t < P0 else 'smile')


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    kitchen(d)
    d.text((W/2, 70), '저녁, 분유 타는 중', font=FTI, fill=TXT, anchor='mm')
    dad(d, t); baby(d, t); kid(d, t)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-3.9)/0.6)))
    if t >= T_THX:
        b = min(1, (t-T_THX)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        txt = 'Thanks for waiting.'; w = dl.textlength(txt, font=FSM); cx = 690
        cx = min(cx, W-w/2-50)
        dl.rounded_rectangle([cx-w/2-30, 404, cx+w/2+30, 458], radius=28, fill=(255, 255, 255, int(230*b)), outline=(160, 190, 170, int(255*b)), width=4)
        dl.text((cx, 431), txt, font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_THX, tts('Thanks for waiting.', DAD, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('just_a_minute', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.4, 9.2, 12.8))
