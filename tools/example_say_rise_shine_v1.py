"""appa say: "Rise and shine!"(아침, 아이 방). 한 장면 안에서만: 아빠가 창가에서 말하고, 커튼이 열리고, 첫째가 침대에서 일어나 앉는다.
소리: 아빠 목소리로 천천히 → 보통 속도 → (첫째가 일어나 앉으면) 한 번 더.
사용: python3 example_say_rise_shine_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face, INK

SKIN = (250, 226, 200); WALL = (236, 232, 244); FLOOR = (214, 204, 186)
SKY = (214, 232, 244); SUN = (246, 214, 140); CURTAIN = (232, 190, 196); CURTAIN_D = (214, 168, 176)
FRAME = (255, 255, 255); BED = (226, 206, 190); PILLOW = (255, 252, 246)
BLANKET = (196, 214, 236); BLANKET_D = (170, 192, 222)
DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 200, 150); PANTS = (150, 170, 210)

EN, KO = 'Rise and shine!', '일어나, 아침이야'
T_SLOW, T_NORM, T_AGAIN = 2.4, 6.0, 11.9
T_OPEN, T_SIT = 7.6, 9.6          # 커튼 열림 시작, 일어나 앉기 시작
TOTAL = 16.2


def mix(a, b, k): return tuple(int(a[i]+(b[i]-a[i])*k) for i in range(3))


def sleepy_eyes(d, cx, cy, r):
    """감은 눈: 얼굴 위 눈 자리를 덮고 아래로 휜 선."""
    ex = r*0.38; ey = cy+r*0.08; er = r*0.10
    for sx in (cx-ex, cx+ex):
        d.ellipse([sx-er*1.3, ey-er*1.4, sx+er*1.3, ey+er*1.4], fill=SKIN)
        d.arc([sx-er*1.6, ey-er*1.2, sx+er*1.6, ey+er*1.2], 20, 160, fill=INK, width=max(3, int(r*0.07)))


def scene(t):
    o = ease((t-T_OPEN)/2.0)                         # 커튼 열림 0→1
    s = ease((t-T_SIT)/1.8)                          # 일어나 앉기 0→1
    im = Image.new('RGB', (W, H), mix((214, 210, 228), WALL, o)); d = ImageDraw.Draw(im)
    d.text((W/2, 70), '아침, 아이 방', font=FTI, fill=TXT, anchor='mm')
    d.rectangle([0, 960, W, H], fill=FLOOR)
    # 창문(가운데): 하늘 + 해
    x0, y0, x1, y1 = 400, 450, 680, 720
    d.rounded_rectangle([x0-14, y0-14, x1+14, y1+14], radius=18, fill=FRAME)
    d.rectangle([x0, y0, x1, y1], fill=mix((176, 186, 214), SKY, o))
    sy = 640-70*o
    d.ellipse([540-46, sy-46, 540+46, sy+46], fill=mix((214, 200, 170), SUN, o))
    d.line([540, y0, 540, y1], fill=FRAME, width=10)
    # 커튼: 닫힘(가운데에서 만남) → 양옆으로
    half = (x1-x0)/2+20
    wcur = half-(half-50)*o
    for side in (-1, 1):
        if side < 0: cx0, cx1 = x0-30, x0-30+wcur
        else: cx0, cx1 = x1+30-wcur, x1+30
        d.rounded_rectangle([cx0, y0-30, cx1, y1+40], radius=16, fill=CURTAIN)
        for k in range(1, 3):
            lx = cx0+(cx1-cx0)*k/3
            d.line([lx, y0-10, lx, y1+30], fill=CURTAIN_D, width=5)
    d.rectangle([x0-50, y0-44, x1+50, y0-30], fill=(200, 190, 210))   # 커튼봉
    # 아빠(왼쪽, 창 옆에 서 있음): 팔은 몸 옆에 짧게
    d.rounded_rectangle([150, 740, 206, 990], radius=26, fill=PANTS)
    d.rounded_rectangle([226, 740, 282, 990], radius=26, fill=PANTS)
    d.ellipse([140, 970, 216, 1004], fill=SKIN); d.ellipse([216, 970, 292, 1004], fill=SKIN)
    d.rounded_rectangle([120, 520, 312, 770], radius=70, fill=DAD_SHIRT)
    for xa in (108, 324):
        d.rounded_rectangle([xa-24, 540, xa+24, 690], radius=24, fill=DAD_SHIRT)
        d.ellipse([xa-22, 676, xa+22, 720], fill=SKIN)
    face(d, 216, 432, 90, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.9), (T_NORM, 1.3), (T_AGAIN, 1.3)):
        speak_mark(d, 330, 432, t, on, on+dur)
    # 침대(오른쪽 아래)
    d.rounded_rectangle([600, 800, 1060, 960], radius=30, fill=BED)
    d.rounded_rectangle([1000, 700, 1060, 960], radius=24, fill=BED)       # 머리판
    d.rounded_rectangle([600, 940, 630, 1000], radius=10, fill=BED)
    d.rounded_rectangle([1020, 940, 1050, 1000], radius=10, fill=BED)
    d.rounded_rectangle([870, 770, 990, 830], radius=28, fill=PILLOW)
    # 첫째: 누움(머리 베개 위) → 일어나 앉음
    hx = 930-20*s; hy = 760-150*s; r = 68
    if s > 0.02:   # 앉으면서 보이는 몸통
        top = hy+r*0.7
        d.rounded_rectangle([hx-70, top, hx+70, 880], radius=50, fill=KID_SHIRT)
    face(d, hx, hy, r, 0, mood='wow' if 10.6 < t < 12.4 else 'smile')
    if s < 0.35: sleepy_eyes(d, hx, hy, r)
    # 이불(몸을 덮음)
    btop = 810+30*s
    d.rounded_rectangle([630, btop, 990, 930], radius=40, fill=BLANKET)
    d.line([660, btop+40, 960, btop+40], fill=BLANKET_D, width=6)
    # 영어 카드(위쪽, 얼굴과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.6)/0.6)))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('rise_shine', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.0, 9.0, 12.2))
