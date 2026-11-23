"""appa say: "Let's bundle up."(추운 아침, 현관 앞). 한 장면 안에서만: 아빠는 외투를 입고 서서 말하고,
첫째는 외투를 걸친 채 혼자 지퍼를 아래에서 위로 올린다. 엄마는 겉싸개로 싼 둘째를 안고 있다.
창밖엔 찬 바람(나뭇잎이 휙). 지퍼가 다 올라가면 아빠가 한 번 더, 엄마가 "All bundled up."
소리: 아빠 목소리로 천천히 → 보통 속도 → (지퍼 다 올린 뒤) 한 번 더 → 엄마 대답.
사용: python3 example_say_bundle_up_v1.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from say import *
from example_yawn_catch_v5 import face

SKIN = (250, 226, 200); WALL = (238, 232, 240); FLOOR = (214, 204, 186); MAT = (200, 214, 196)
SKY = (206, 222, 240); FRAME = (250, 250, 252); LEAF = (232, 176, 120)
DAD_COAT = (160, 190, 170); DAD_COAT_D = (140, 172, 152); PANTS = (150, 170, 210)
KID_COAT = (176, 200, 236); KID_COAT_D = (150, 178, 222); KID_SHIRT = (246, 214, 140)
MOM_SHIRT = (240, 196, 200); MOM_HAIR = (110, 86, 76); BUNTING = (220, 200, 232); BUNTING_D = (200, 180, 220)
ZIP = (232, 150, 120); WAVE = (232, 150, 120)
FSM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 40, index=1)

EN, KO = "Let's bundle up.", '따뜻하게 꽁꽁 입자'
T_SLOW, T_NORM, T_AGAIN, T_MOM = 2.4, 4.9, 9.6, 11.3
Z0, Z1 = 6.8, 9.2            # 첫째가 지퍼를 올리는 시간
TOTAL = 15.4
KX = 560                     # 첫째 몸 가운데
Z_BOT, Z_TOP = 880, 712      # 지퍼 고리가 움직이는 높이


def zip_y(t):
    return Z_BOT+(Z_TOP-Z_BOT)*ease((t-Z0)/(Z1-Z0))


def window(d, t):
    d.rounded_rectangle([420, 390, 700, 560], radius=18, fill=FRAME)
    d.rectangle([438, 408, 682, 542], fill=SKY)
    d.line([560, 408, 560, 542], fill=FRAME, width=10)
    # 찬 바람 줄과 날리는 나뭇잎
    for i in range(3):
        ph = (t*0.5+i*0.33) % 1
        x = 438+ph*260; y = 430+i*40+8*math.sin(t*2+i)
        if 492 < x < 676:
            d.arc([x-50, y-12, x+10, y+12], 200, 340, fill=(250, 250, 255), width=5)
    for i in range(2):
        ph = (t*0.35+i*0.5) % 1
        x = 438+ph*244; y = 455+i*45+14*math.sin(t*3+i*2)
        if 446 < x < 674:
            d.ellipse([x-12, y-7, x+12, y+7], fill=LEAF)


def dad(d, t):
    cx = 190
    for dx in (-34, 34):
        d.rounded_rectangle([cx+dx-26, 760, cx+dx+26, 980], radius=24, fill=PANTS)
        d.ellipse([cx+dx-36, 962, cx+dx+36, 996], fill=SKIN)
    d.rounded_rectangle([cx-100, 560, cx+100, 800], radius=64, fill=DAD_COAT)
    d.line([cx, 600, cx, 790], fill=DAD_COAT_D, width=6)
    for y in (640, 700, 760):
        d.ellipse([cx+10, y-8, cx+26, y+8], fill=DAD_COAT_D)
    for dx in (-1, 1):                       # 팔은 몸 옆에 짧게
        x0 = cx+dx*108
        d.rounded_rectangle([x0-24, 580, x0+24, 740], radius=24, fill=DAD_COAT)
        d.ellipse([x0-20, 726, x0+20, 764], fill=SKIN)
    d.rounded_rectangle([cx-60, 540, cx+60, 590], radius=24, fill=(246, 214, 140))   # 목도리
    face(d, cx, 470, 86, 0, mood='smile')
    for on, dur in ((T_SLOW, 1.7), (T_NORM, 1.3), (T_AGAIN, 1.3)):
        speak_mark(d, cx+120, 450, t, on, on+dur)


def kid(d, t):
    zy = zip_y(t)
    for dx in (-26, 26):
        d.rounded_rectangle([KX+dx-22, 880, KX+dx+22, 1000], radius=20, fill=PANTS)
        d.ellipse([KX+dx-30, 986, KX+dx+30, 1012], fill=SKIN)
    # 안쪽 티셔츠(외투가 열린 틈으로 보임)
    d.rounded_rectangle([KX-74, 690, KX+74, 900], radius=46, fill=KID_SHIRT)
    # 외투 두 쪽: 지퍼 고리 아래는 닫히고 위는 V로 벌어짐
    open_w = 34
    L = [(KX-84, 700), (KX-6, 700), (KX-6, zy), (KX-6, 908), (KX-84, 908)]
    R = [(KX+6, 700), (KX+84, 700), (KX+84, 908), (KX+6, 908), (KX+6, zy)]
    d.rounded_rectangle([KX-90, 690, KX+90, 910], radius=48, fill=KID_COAT)
    gap_top = max(0, zy-700)
    if gap_top > 4:
        d.polygon([(KX-open_w, 696), (KX+open_w, 696), (KX, zy)], fill=KID_SHIRT)
    for y in (760, 820, 880):                # 패딩 줄
        d.line([KX-82, y, KX-8, y], fill=KID_COAT_D, width=4)
        d.line([KX+8, y, KX+82, y], fill=KID_COAT_D, width=4)
    d.line([KX, max(zy, 700), KX, 906], fill=KID_COAT_D, width=5)    # 닫힌 지퍼 줄
    d.rounded_rectangle([KX-9, zy-4, KX+9, zy+26], radius=5, fill=ZIP)  # 지퍼 고리
    # 팔: 왼팔은 지퍼 고리를 잡고(짧게), 오른팔은 몸 옆
    d.rounded_rectangle([KX+86, 712, KX+120, 840], radius=17, fill=KID_COAT)
    d.ellipse([KX+86, 828, KX+120, 860], fill=SKIN)
    sx, sy = KX-80, 722
    hx, hy = KX-16, zy+18
    d.line([sx, sy, hx, hy], fill=KID_COAT, width=34)
    d.ellipse([sx-17, sy-17, sx+17, sy+17], fill=KID_COAT)
    d.ellipse([hx-18, hy-16, hx+18, hy+16], fill=SKIN)
    face(d, KX, 626, 70, 0, mood='wow' if Z1 <= t < Z1+1.2 else 'smile')


def mom(d, t):
    cx = 890
    for dx in (-30, 30):
        d.rounded_rectangle([cx+dx-24, 780, cx+dx+24, 980], radius=22, fill=PANTS)
        d.ellipse([cx+dx-32, 964, cx+dx+32, 996], fill=SKIN)
    d.rounded_rectangle([cx-74, 500, cx+74, 650], radius=50, fill=MOM_HAIR)      # 어깨까지 오는 머리
    d.rounded_rectangle([cx-90, 590, cx+90, 810], radius=60, fill=MOM_SHIRT)
    face(d, cx, 520, 72, 0, mood='smile', hair=MOM_HAIR)
    # 겉싸개에 싼 둘째(가슴 앞에 가로로, 머리는 왼쪽)
    d.rounded_rectangle([cx-110, 650, cx+70, 740], radius=45, fill=BUNTING)
    d.line([cx-40, 662, cx-40, 728], fill=BUNTING_D, width=5)
    d.ellipse([cx-150, 640, cx-50, 740], fill=BUNTING)                           # 모자 달린 겉싸개
    face(d, cx-100, 694, 36, 0, mood='flat' if t < T_MOM else 'smile', baby=True)
    # 엄마 팔: 아기 아래로 받침(짧게)
    d.rounded_rectangle([cx-110, 722, cx+96, 760], radius=19, fill=MOM_SHIRT)
    d.ellipse([cx-128, 720, cx-92, 760], fill=SKIN)
    d.rounded_rectangle([cx+82, 610, cx+120, 750], radius=19, fill=MOM_SHIRT)
    if T_MOM <= t <= T_MOM+1.1:
        speak_mark(d, cx-96, 500, t, T_MOM, T_MOM+1.1)


def scene(t):
    im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.text((W/2, 70), '추운 아침, 나가기 전', font=FTI, fill=TXT, anchor='mm')
    window(d, t)
    d.rectangle([0, 930, W, H], fill=FLOOR)
    d.rounded_rectangle([60, 960, 1020, 1030], radius=30, fill=MAT)
    dad(d, t); kid(d, t); mom(d, t)
    a = min(1, max(0, (t-T_SLOW+0.4)/0.5))
    card(im, EN, KO, 200, a, min(1, max(0, (t-4.1)/0.6)))
    if t >= T_MOM:
        b = min(1, (t-T_MOM)/0.4)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        txt = 'All bundled up.'; w = dl.textlength(txt, font=FSM); cx = 880
        cx = min(cx, W-w/2-50)
        dl.rounded_rectangle([cx-w/2-30, 378, cx+w/2+30, 432], radius=28, fill=(255, 255, 255, int(230*b)), outline=(240, 196, 200, int(255*b)), width=4)
        dl.text((cx, 405), txt, font=FSM, fill=TXT+(int(255*b),), anchor='mm')
        im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else None
    clips = [(T_SLOW, tts(EN, DAD, 0.8)), (T_NORM, tts(EN, DAD, 1.0)), (T_AGAIN, tts(EN, DAD, 1.0)),
             (T_MOM, tts('All bundled up.', MOM, 1.0))]
    for t0, c in clips: print('clip', t0, round(len(c)/SR, 2))
    build('bundle_up', scene, TOTAL, clips, out, preview=pv, preview_times=(1.2, 5.6, 8.0, 12.5))
