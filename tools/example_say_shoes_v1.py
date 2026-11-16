"""appa say 예시: "Shoes on!"(현관, 나가기 전). 한 장면 안에서만: 아빠가 문 앞에서 말하고, 첫째가 신발을 신는다.
소리: 아빠 목소리로 천천히 → 보통 속도 → (신발 다 신으면) 한 번 더.
사용: python3 example_say_shoes_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (240, 234, 226); FLOOR = (214, 200, 182); TILE = (226, 214, 198)
DOOR = (196, 214, 236); DOOR_D = (170, 192, 222); DAD_SHIRT = (160, 190, 170); KID_SHIRT = (246, 200, 150)
PANTS = (150, 170, 210); SHOE = (232, 150, 120); SHOE_D = (214, 128, 100)

EN, KO = 'Shoes on!', '신발 신자'
T_SLOW, T_NORM, T_AGAIN = 2.6, 6.4, 10.6
TOTAL = 15.0


def shoe(d, x, y, s=1.0):
    d.rounded_rectangle([x-46*s, y-24*s, x+46*s, y+20*s], radius=int(20*s), fill=SHOE)
    d.rounded_rectangle([x-46*s, y+8*s, x+46*s, y+22*s], radius=int(7*s), fill=SHOE_D)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.text((W/2, 70), '현관, 나가기 전', font=FTI, fill=TXT, anchor='mm')
    # 문 + 바닥
    d.rounded_rectangle([720, 330, 980, 880], radius=24, fill=DOOR)
    d.ellipse([925, 600, 955, 630], fill=DOOR_D)
    d.rectangle([0, 880, W, H], fill=FLOOR)
    for x in range(0, W, 140): d.line([x, 880, x, H], fill=TILE, width=4)
    # 아빠(왼쪽, 서 있음): 다리·몸·짧은 팔
    d.rounded_rectangle([170, 720, 230, 1010], radius=26, fill=PANTS)
    d.rounded_rectangle([250, 720, 310, 1010], radius=26, fill=PANTS)
    d.rounded_rectangle([140, 500, 340, 760], radius=70, fill=DAD_SHIRT)
    for x0 in (128, 352):
        d.rounded_rectangle([x0-26, 520, x0+26, 680], radius=26, fill=DAD_SHIRT)
        d.ellipse([x0-24, 665, x0+24, 713], fill=SKIN)
    face(d, 240, 410, 96, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.4), (T_NORM, 1.0), (T_AGAIN, 1.0)):
        speak_mark(d, 362, 410, t, on, on+dur)
    # 첫째(가운데 오른쪽, 바닥에 앉아 신발 신기)
    k = ease((t-8.2)/2.0)                       # 신발이 발로 가는 정도
    d.rounded_rectangle([470, 720, 650, 930], radius=60, fill=KID_SHIRT)
    for fx in (500, 600):                          # 앞으로 뻗은 다리(짧게)
        d.rounded_rectangle([fx-26, 890, fx+26, 990], radius=24, fill=PANTS)
        d.ellipse([fx-30, 975, fx+30, 1020], fill=SKIN)
    face(d, 560, 640, 84, 0, mood='wow' if 7.8 < t < 10.4 else 'smile')
    # 신발: 옆에 놓였다가 발로
    for j, fx in enumerate((500, 600)):
        sx = 730+80*j+(fx-730-80*j)*k; sy = 1030+(1004-1030)*k
        shoe(d, sx, sy, 0.8)
    # 영어 카드(위쪽, 사람과 안 겹치게)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.6)/0.6)))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0))]
    build('shoes', scene, TOTAL, clips, out, preview=pv, preview_times=(1.5, 3.0, 9.2, None))
