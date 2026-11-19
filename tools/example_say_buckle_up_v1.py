"""appa say: "Buckle up."(차 뒷자리, 출발 전). 한 장면 안에서만: 문 앞의 아빠가 말하면 부스터 시트의 첫째가
어깨 위 벨트를 당겨 허리 옆 버클에 '딸깍' 채운다. 옆에는 뒤를 보는 카시트에 이미 끈을 맨 둘째.
소리: 아빠 목소리로 천천히 → 보통 속도 → (딸깍 뒤) 한 번 더 → 앞자리 엄마 "Off we go!".
사용: python3 example_say_buckle_up_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); INSIDE = (236, 230, 240); WINDOW = (206, 228, 244); FRAME = (200, 194, 210)
SEAT = (190, 196, 220); SEAT_D = (170, 178, 206); BOOST = (240, 196, 170)
BELT = (110, 116, 140); BUCKLE = (240, 120, 110); METAL = (200, 204, 214)
DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 214, 140); PANTS = (150, 170, 210)
CARRIER = (232, 190, 196); CARRIER_D = (214, 168, 178); ONESIE = (200, 226, 206); MOM_HAIR = (110, 86, 76)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = 'Buckle up.', '안전벨트 매자'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.4, 5.0, 10.0, 11.7
T_PULL, T_CLICK = 6.6, 9.0
TOTAL = 16.0

A = (668, 560)        # 어깨 쪽 벨트 고정점(좌석 옆 기둥)
LAP = (690, 808)      # 오른쪽 허리 아래 고정점
B = (478, 806)        # 왼쪽 허리 옆 버클 받침


def lerp(a, b, k): return a+(b-a)*k


def tongue(t):
    """벨트 고리(첫째 손): 오른쪽 어깨 옆에 걸려 있다가 → 가슴을 비스듬히 가로질러 → 왼쪽 허리 버클로."""
    r = ease((t-T_PULL)/(T_CLICK-T_PULL))
    if r < 0.35:     # 먼저 앞으로 당겨 빼기
        k = r/0.35; return lerp(676, 640, k), lerp(700, 640, k)
    k = (r-0.35)/0.65
    x = lerp(640, B[0], k); y = lerp(640, B[1]-6, k) - 30*math.sin(k*math.pi)
    return x, y


def scene(t):
    im = Image.new('RGB', (W, H), INSIDE); d = ImageDraw.Draw(im)
    # 창문(뒤쪽 배경)
    d.rounded_rectangle([380, 400, 1060, 560], radius=40, fill=WINDOW)
    d.text((W/2, 70), '차 뒷자리, 출발 전', font=FTI, fill=TXT, anchor='mm')
    # 열린 문틀(왼쪽)
    d.rectangle([330, 380, 352, 1080], fill=FRAME)
    d.rectangle([0, 1000, 340, H], fill=(214, 204, 186))
    # 뒷좌석 바닥 쿠션
    d.rounded_rectangle([352, 880, 1080, 960], radius=24, fill=SEAT_D)
    # ── 첫째 자리: 등받이 + 부스터
    d.rounded_rectangle([420, 580, 720, 900], radius=50, fill=SEAT)
    d.rounded_rectangle([440, 812, 700, 890], radius=26, fill=BOOST)
    d.rectangle([680, 540, 700, 600], fill=METAL)     # 어깨 고정점
    # 첫째 몸
    d.rounded_rectangle([500, 820, 680, 870], radius=24, fill=PANTS)   # 무릎(옆에서 본 허벅지 앞쪽)
    d.rounded_rectangle([486, 620, 650, 830], radius=60, fill=KID_SHIRT)
    face(d, 568, 540, 78, 0, mood='wow' if T_CLICK <= t < T_CLICK+1.0 else 'smile')
    # 버클 받침
    d.rounded_rectangle([B[0]-18, B[1]-10, B[0]+18, B[1]+40], radius=8, fill=BUCKLE)
    # 벨트: 어깨 고정점 → 고리(손) → 허리 고정점
    tx, ty = (B[0], B[1]-6) if t >= T_CLICK else tongue(t)
    d.line([A, (tx, ty)], fill=BELT, width=20)
    d.line([(tx, ty), LAP], fill=BELT, width=20)
    d.rounded_rectangle([tx-14, ty-12, tx+14, ty+16], radius=6, fill=METAL)
    # 첫째 팔: 왼팔은 무릎 위, 오른팔이 고리를 잡음(채운 뒤엔 무릎으로)
    d.line([(510, 660), (520, 800)], fill=KID_SHIRT, width=40); d.ellipse([500, 790, 540, 830], fill=SKIN)
    if t < T_CLICK+0.4:
        hx, hy = tx+8, ty+18
    else:
        k = ease((t-T_CLICK-0.4)/0.6); hx, hy = lerp(B[0]+8, 600, k), lerp(B[1]+12, 800, k)
    sx, sy = 626, 650
    d.line([(sx, sy), (hx, hy)], fill=KID_SHIRT, width=40)
    d.ellipse([sx-20, sy-20, sx+20, sy+20], fill=KID_SHIRT)
    d.ellipse([hx-22, hy-20, hx+22, hy+20], fill=SKIN)
    # 딸깍
    if T_CLICK <= t < T_CLICK+1.4:
        a = min(1, (t-T_CLICK)/0.2)
        for ang in range(0, 360, 60):
            r0, r1 = 34, 34+18*a
            c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([B[0]-60+c*r0, B[1]+10+s*r0, B[0]-60+c*r1, B[1]+10+s*r1], fill=BUCKLE, width=5)
        d.text((B[0]-60, B[1]+10), '딸깍', font=FSM, fill=BUCKLE, anchor='mm')
    # ── 둘째: 뒤를 보는 카시트(얼굴은 왼쪽, 첫째 쪽), 끈은 이미 맴
    d.chord([740, 640, 940, 900], 70, 290, fill=CARRIER)
    d.rounded_rectangle([760, 860, 930, 890], radius=12, fill=CARRIER_D)
    d.rounded_rectangle([790, 740, 880, 840], radius=36, fill=ONESIE)
    face(d, 830, 700, 46, 0, mood='smile' if t > T_MOM else 'flat', baby=True)
    d.line([(806, 748), (836, 820)], fill=BELT, width=10); d.line([(866, 748), (836, 820)], fill=BELT, width=10)
    d.ellipse([826, 810, 846, 830], fill=BUCKLE)
    # ── 엄마: 앞자리에서 뒤돌아봄(오른쪽 끝)
    face(d, 1000, 610, 54, 0, mood='smile', hair=MOM_HAIR)
    d.rounded_rectangle([950, 668, 1060, 900], radius=30, fill=SEAT_D)    # 앞좌석 등받이
    if T_MOM <= t <= T_MOM+0.9:
        for j in range(3):
            r = 16+j*14+6*math.sin((t-T_MOM)*8-j)
            d.arc([944-r, 600-r, 944+r, 600+r], 140, 220, fill=(232, 150, 120), width=6)
    # ── 아빠: 열린 문 밖에 서 있음(왼쪽)
    d.rounded_rectangle([130, 760, 186, 1010], radius=26, fill=PANTS)
    d.rounded_rectangle([206, 760, 262, 1010], radius=26, fill=PANTS)
    d.rounded_rectangle([100, 560, 292, 790], radius=70, fill=DAD_SHIRT)
    d.rounded_rectangle([64, 580, 112, 730], radius=24, fill=DAD_SHIRT); d.ellipse([66, 716, 110, 760], fill=SKIN)
    d.line([(280, 600), (350, 680)], fill=DAD_SHIRT, width=46)            # 문틀을 잡은 팔
    d.ellipse([330, 660, 374, 704], fill=SKIN)
    face(d, 196, 474, 86, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.3), (T_NORM, 1.0), (T_AGAIN, 1.0)):
        speak_mark(d, 304, 470, t, on, on+dur)
    # 영어 카드(위쪽, 얼굴과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.2)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        w = dl.textlength('Off we go!', font=FSM)
        dl.rounded_rectangle([900-w/2-30, 486, 900+w/2+30, 546], radius=30, fill=(255, 255, 255, int(220*b)))
        dl.text((900, 516), 'Off we go!', font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts('Off we go!', MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('buckle_up', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.6, 8.2, 12.4))
