"""appa say: "Open wide."(저녁, 양치 시간). 한 장면 안에서만: 욕실 세면대 앞, 첫째는 발판 위에 서 있고
아빠가 옆에서 칫솔을 든다. 아빠가 천천히 → 보통 속도로 말하면 첫째가 입을 크게 벌리고, 아빠가 칫솔질.
다 닦고 입안을 보려 할 때 한 번 더. 문가에서 둘째를 안은 엄마가 "Nice and clean!".
아이 목소리는 합성하지 않는다. 마지막 3초 멈춤.
사용: python3 example_say_open_wide_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (232, 240, 244); TILE = (220, 232, 238); FLOOR = (214, 208, 196)
SINK = (250, 250, 252); SINK_D = (210, 216, 228); MIRROR = (214, 232, 244)
DAD_SHIRT = (160, 190, 170); PANTS = (150, 170, 210); KID_SHIRT = (246, 214, 140)
STOOL = (176, 200, 236); MOM_SHIRT = (240, 196, 200); ONESIE = (214, 232, 244)
BRUSH = (232, 150, 120); BRISTLE = (255, 255, 255); MOUTH = (200, 110, 118)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = 'Open wide.', '입 크게 벌려'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.2, 4.6, 10.4, 12.2
O0, O1 = 3.6, 4.4            # 첫째 입 벌리기(첫 번째)
B0, B1 = 6.2, 9.6            # 칫솔질
C0, C1 = 9.6, 10.1           # 잠깐 다묾
O2, O3 = 10.8, 11.4          # 다시 크게(검사)
TOTAL = 16.0
DX, KX, MX = 290, 560, 875
KHY = 560                    # 첫째 얼굴 중심 y


def room(d):
    d.rectangle([0, 0, W, 960], fill=WALL)
    for y in range(420, 960, 90): d.line([0, y, 640, y], fill=TILE, width=3)
    d.rounded_rectangle([400, 330, 720, 470], radius=20, fill=MIRROR)       # 거울(얼굴 뒤로 살짝)
    d.rectangle([0, 960, W, H], fill=FLOOR)
    # 세면대(첫째 앞, 가슴 아래)
    d.rounded_rectangle([380, 760, 740, 820], radius=24, fill=SINK, outline=SINK_D, width=4)
    d.rounded_rectangle([500, 820, 620, 960], radius=18, fill=SINK_D)
    d.rounded_rectangle([548, 726, 572, 762], radius=8, fill=SINK_D)        # 수도꼭지
    # 문틀(오른쪽, 엄마)
    d.rectangle([740, 300, 1010, 960], fill=(244, 236, 228))
    d.rectangle([740, 300, 756, 960], fill=(226, 214, 200))


def kid_open(t):
    a = ease((t-O0)/(O1-O0))
    if t >= C0: a = 1-ease((t-C0)/(C1-C0))*0.6
    if t >= O2: a = 0.4+0.6*ease((t-O2)/(O3-O2))
    if t >= 13.6: a = 1-ease((t-13.6)/0.5)
    return a


def kid(d, t):
    d.rounded_rectangle([KX-90, 950, KX+90, 1000], radius=14, fill=STOOL)    # 발판
    d.rounded_rectangle([KX-70, 640, KX+70, 800], radius=44, fill=KID_SHIRT)  # 몸(아래는 세면대 뒤)
    o = kid_open(t)
    r = 72
    face(d, KX, KHY, r, 0, mood='smile' if o < 0.15 else 'flat')
    if o >= 0.15:                                    # 입 크게(위 이 한 줄)
        my = KHY+r*0.52
        d.rectangle([KX-r*0.3, my-r*0.08, KX+r*0.3, my+r*0.12], fill=SKIN)  # 원래 입 가리기
        mw = r*(0.14+0.16*o); mh = r*(0.08+0.30*o)
        d.ellipse([KX-mw, my-mh*0.5, KX+mw, my+mh], fill=MOUTH)
        d.chord([KX-mw*0.8, my-mh*0.45, KX+mw*0.8, my+mh*0.35], 180, 360, fill=(255, 255, 255))


def brush_pos(t):
    hx, hy = KX-62, KHY+44                           # 첫째 입 옆
    if B0 <= t <= B1:
        k = min(1, (t-B0)/0.3, (B1-t)/0.3)
        return hx+10*math.sin((t-B0)*2*math.pi*3)*k, hy, True
    return DX+120, 690, False


def dad(d, t):
    cx = DX
    for dx in (-30, 30):
        d.rounded_rectangle([cx+dx-24, 780, cx+dx+24, 990], radius=22, fill=PANTS)
        d.ellipse([cx+dx-30, 972, cx+dx+30, 1000], fill=SKIN)
    d.rounded_rectangle([cx-96, 540, cx+96, 800], radius=62, fill=DAD_SHIRT)
    # 왼팔: 몸 옆에 짧게
    d.rounded_rectangle([cx-118, 560, cx-74, 720], radius=22, fill=DAD_SHIRT)
    d.ellipse([cx-118, 702, cx-74, 746], fill=SKIN)
    # 오른팔: 어깨에서 손(칫솔)까지, 길이 제한
    bx, by, on = brush_pos(t)
    sx, sy = cx+80, 590
    hx, hy = bx-34, by+10
    L = math.hypot(hx-sx, hy-sy)
    if L > 190: hx, hy = sx+(hx-sx)*190/L, sy+(hy-sy)*190/L
    d.line([sx, sy, hx, hy], fill=DAD_SHIRT, width=44)
    d.ellipse([sx-22, sy-22, sx+22, sy+22], fill=DAD_SHIRT)
    # 칫솔(손 → 머리 쪽이 첫째 입)
    d.line([hx, hy, hx+56, hy-12], fill=BRUSH, width=12)
    d.rounded_rectangle([hx+48, hy-26, hx+72, hy-8], radius=4, fill=BRISTLE, outline=SINK_D, width=2)
    d.ellipse([hx-20, hy-20, hx+20, hy+20], fill=SKIN)
    face(d, cx, 450, 86, 0, mood='smile')
    for on_, dur in ((T_SLOW, 1.3), (T_NORM, 0.9), (T_AGAIN, 0.9)):
        if on_ <= t <= on_+dur:
            for j in range(3):
                r = 18+j*16+6*math.sin((t-on_)*8-j)
                d.arc([cx-110-r, 430-r, cx-110+r, 430+r], 140, 220, fill=(232, 150, 120), width=6)


def mom(d, t):
    cx = MX
    d.rounded_rectangle([cx-90, 450, cx+90, 610], radius=40, fill=(120, 96, 82))   # 긴 머리(뒤)
    for dx in (-28, 28):
        d.rounded_rectangle([cx+dx-22, 790, cx+dx+22, 990], radius=20, fill=PANTS)
        d.ellipse([cx+dx-28, 972, cx+dx+28, 1000], fill=SKIN)
    d.rounded_rectangle([cx-86, 590, cx+86, 810], radius=56, fill=MOM_SHIRT)
    # 안긴 둘째(가슴 앞)
    d.rounded_rectangle([cx-70, 660, cx+40, 740], radius=40, fill=ONESIE)
    face(d, cx-70, 668, 40, 0, mood='smile', baby=True)
    for sx in (-1, 1):
        d.ellipse([cx+sx*60-20, 700, cx+sx*60+20, 740], fill=SKIN)
    face(d, cx, 500, 78, 0, mood='smile')
    if T_MOM <= t <= T_MOM+1.0:
        for j in range(3):
            r = 18+j*16+6*math.sin((t-T_MOM)*8-j)
            d.arc([cx-100-r, 480-r, cx-100+r, 480+r], 140, 220, fill=(232, 150, 120), width=6)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    room(d)
    d.text((W/2, 70), '저녁, 양치 시간', font=FTI, fill=TXT, anchor='mm')
    kid(d, t); dad(d, t); mom(d, t)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 190, a, min(1, max(0, (t-3.4)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        txt = 'Nice and clean!'; w = dl.textlength(txt, font=FSM); cx = min(MX-40, W-w/2-50)
        dl.rounded_rectangle([cx-w/2-30, 332, cx+w/2+30, 386], radius=28, fill=(255, 255, 255, int(230*b)), outline=(240, 196, 200, int(255*b)), width=4)
        dl.text((cx, 359), txt, font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts('Nice and clean!', MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('open_wide', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 4.8, 8.0, 12.9))
