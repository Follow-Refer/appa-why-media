"""appa say: "Be gentle."(거실 매트, 아기 옆). 한 장면 안에서만: 첫째가 매트에 누운 둘째 팔 쪽으로 손을 뻗고,
아빠가 말하면 손을 천천히 내려 살살 쓰다듬고, 둘째가 웃는다.
소리: 아빠 목소리로 천천히 → 보통 속도 → (쓰다듬기가 끝나면) 한 번 더.
사용: python3 example_say_be_gentle_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (238, 234, 244); FLOOR = (220, 208, 192)
MAT = (214, 232, 244); MAT_D = (196, 218, 236); ONESIE = (246, 214, 140); ONESIE_D = (232, 196, 120)
DAD_SHIRT = (160, 190, 170); KID_SHIRT = (232, 190, 196); PANTS = (150, 170, 210)

EN, KO = 'Be gentle.', '살살 해'
T_SLOW, T_NORM, T_AGAIN = 2.4, 5.6, 11.0
T_DOWN, T_STROKE, T_END = 6.8, 7.8, 10.8   # 손 내려놓기, 쓰다듬기 시작, 끝
TOTAL = 15.2


def lerp(a, b, k): return a+(b-a)*k


def hand_pos(t):
    """첫째 손: 무릎 위(780,800) → 아기 팔 위로 뻗음(700,745) → 팔 위에 내려 살살 쓰다듬기."""
    r = ease((t-0.6)/1.6)
    x = lerp(784, 660, r); y = lerp(810, 742, r)
    dn = ease((t-T_DOWN)/1.0)
    y = lerp(y, 774, dn)
    if T_STROKE <= t <= T_END:
        p = (t-T_STROKE)/(T_END-T_STROKE)
        x += -30*math.sin(p*2*math.pi*1.5)*math.sin(p*math.pi)   # 천천히 1.5번 왕복
    return x, y


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.text((W/2, 70), '거실 매트, 아기 옆에서', font=FTI, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=FLOOR)
    # 매트
    d.rounded_rectangle([360, 840, 1000, 960], radius=30, fill=MAT)
    for x in range(420, 1000, 90): d.line([x, 852, x, 948], fill=MAT_D, width=4)
    # 아빠(왼쪽, 서 있음)
    d.rounded_rectangle([150, 740, 206, 990], radius=26, fill=PANTS)
    d.rounded_rectangle([226, 740, 282, 990], radius=26, fill=PANTS)
    d.ellipse([140, 970, 216, 1004], fill=SKIN); d.ellipse([216, 970, 292, 1004], fill=SKIN)
    d.rounded_rectangle([120, 520, 312, 770], radius=70, fill=DAD_SHIRT)
    for xa in (108, 324):
        d.rounded_rectangle([xa-24, 540, xa+24, 690], radius=24, fill=DAD_SHIRT)
        d.ellipse([xa-22, 676, xa+22, 720], fill=SKIN)
    face(d, 216, 432, 90, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.3), (T_NORM, 1.0), (T_AGAIN, 1.0)):
        speak_mark(d, 330, 432, t, on, on+dur)
    # 둘째(매트 위에 누움, 머리 왼쪽): 몸 → 다리 → 팔 → 얼굴
    d.rounded_rectangle([500, 790, 690, 880], radius=44, fill=ONESIE)
    d.rounded_rectangle([680, 800, 750, 834], radius=17, fill=ONESIE_D)
    d.rounded_rectangle([680, 838, 750, 872], radius=17, fill=ONESIE_D)
    d.ellipse([740, 798, 772, 836], fill=SKIN); d.ellipse([740, 836, 772, 874], fill=SKIN)
    d.rounded_rectangle([560, 790, 660, 820], radius=15, fill=ONESIE_D)      # 위쪽 팔(배 위)
    d.ellipse([548, 788, 580, 822], fill=SKIN)
    smile = t > 9.4
    face(d, 448, 832, 62, 0, mood='smile' if smile else 'flat', baby=True)
    # 첫째(오른쪽, 매트 끝에 무릎 꿇고 앉음)
    d.rounded_rectangle([820, 860, 990, 930], radius=34, fill=PANTS)         # 접은 다리
    d.rounded_rectangle([812, 650, 972, 880], radius=60, fill=KID_SHIRT)
    hx, hy = hand_pos(t)
    sx, sy = 826, 700                                                          # 어깨
    d.line([sx, sy, hx+14, hy-6], fill=KID_SHIRT, width=42)
    d.ellipse([sx-21, sy-21, sx+21, sy+21], fill=KID_SHIRT)
    d.ellipse([hx-24, hy-20, hx+24, hy+20], fill=SKIN)
    d.rounded_rectangle([962, 700, 1002, 830], radius=20, fill=KID_SHIRT)      # 반대 팔(몸 옆)
    d.ellipse([962, 816, 1002, 852], fill=SKIN)
    face(d, 892, 572, 80, 0, mood='wow' if smile and t < 11.8 else 'smile')
    # 둘째 웃을 때 작은 반짝임
    if smile:
        a = min(1, (t-9.4)/0.6)
        for (px, py) in ((370, 772), (520, 760)):
            r = 12*a
            d.line([px-r, py, px+r, py], fill=(232, 150, 120), width=5)
            d.line([px, py-r, px, py+r], fill=(232, 150, 120), width=5)
    # 영어 카드(위쪽, 얼굴과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.4)/0.6)))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('be_gentle', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.0, 8.6, 12.4))
