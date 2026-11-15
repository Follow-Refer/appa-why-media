"""거울 속 나는 왼손 들었어!(11/16): 상황(욕실 거울 앞, 아이가 오른손을 듦) → 답(거울 속 손은 같은 쪽, 마주 선 아빠 손은 반대쪽).
사용: python3 example_mirror_hand_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab, HAIR

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FHD = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 46, index=1)
LT = (232, 150, 120); LM = (140, 160, 210)
TILE = (226, 236, 240); TILE_L = (208, 222, 230)
GLASS = (214, 232, 244); GLASS_L = (232, 242, 250); FRAME = (250, 250, 252); FRAME_D = (210, 214, 228)
KID_SHIRT = (246, 200, 150); DAD_SHIRT = (160, 190, 170)
TOWEL = (246, 214, 140); TOWEL_D = (226, 186, 110); BAR = (190, 186, 200)
GLOW = (250, 236, 170)


def raised_arm(d, sx, sy, k, side, s, shirt):
    """어깨(sx,sy)에서 짧은 팔. k=0 내림, 1 올림. side=+1 화면 오른쪽."""
    L = 120*s
    ang = math.radians(80 - 140*k) if side > 0 else math.radians(100 + 140*k)
    hx = sx + math.cos(ang)*L
    hy = sy + math.sin(ang)*L
    d.line([sx, sy, hx, hy], fill=shirt, width=int(40*s))
    d.ellipse([hx-24*s, hy-24*s, hx+24*s, hy+24*s], fill=SKIN)
    return hx, hy


def kid_back(d, cx, by, s, k):
    """뒷모습 아이. 오른손(화면 오른쪽)을 k만큼 듦. 손 위치 반환."""
    bw, bh = 200*s, 230*s
    d.rounded_rectangle([cx-bw/2, by-bh, cx+bw/2, by+40*s], radius=80*s, fill=KID_SHIRT)
    hx, hy = raised_arm(d, cx+bw/2-22*s, by-bh+50*s, k, +1, s, KID_SHIRT)
    raised_arm(d, cx-bw/2+22*s, by-bh+50*s, 0, -1, s, KID_SHIRT)
    r = 92*s; hc = by-bh-r+20*s
    d.ellipse([cx-r, hc-r, cx+r, hc+r], fill=HAIR)
    d.ellipse([cx-r-10*s, hc-8*s, cx-r+16*s, hc+28*s], fill=SKIN)   # 귀
    d.ellipse([cx+r-16*s, hc-8*s, cx+r+10*s, hc+28*s], fill=SKIN)
    return hx, hy


def front_person(d, cx, by, s, k, hand_side, shirt, mood='smile'):
    """마주 보는 사람(거울 속 아이·아빠). hand_side 쪽 손을 k만큼 듦."""
    bw, bh = 200*s, 230*s
    d.rounded_rectangle([cx-bw/2, by-bh, cx+bw/2, by+40*s], radius=80*s, fill=shirt)
    hx, hy = raised_arm(d, cx+hand_side*(bw/2-22*s), by-bh+50*s, k, hand_side, s, shirt)
    raised_arm(d, cx-hand_side*(bw/2-22*s), by-bh+50*s, 0, -hand_side, s, shirt)
    face(d, cx, by-bh-92*s+20*s, 92*s, 0, mood=mood)
    return hx, hy


def towel(d, x, y, s):
    d.rounded_rectangle([x-70*s, y-8*s, x+70*s, y+8*s], radius=8*s, fill=BAR)
    d.rounded_rectangle([x-56*s, y, x+56*s, y+150*s], radius=14*s, fill=TOWEL)
    d.line([x-56*s, y+120*s, x+56*s, y+120*s], fill=TOWEL_D, width=int(8*s))


def bathroom(im):
    d = ImageDraw.Draw(im)
    for x in range(0, W, 120): d.line([x, 0, x, H], fill=TILE_L, width=3)
    for y in range(0, H, 120): d.line([0, y, W, y], fill=TILE_L, width=3)
    return d


def mirror(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0-18, y0-18, x1+18, y1+18], radius=40, fill=FRAME, outline=FRAME_D, width=4)
    d.rounded_rectangle(box, radius=28, fill=GLASS)
    d.line([x0+40, y0+120, x0+120, y0+40], fill=GLASS_L, width=14)


# ---------------- 장면 1: 욕실 거울 앞 ----------------
S1 = int(4.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), TILE); d = bathroom(im)
    d.text((W/2, 80), '거울 속 나는 왼손 들었어!', font=FBW, fill=TXT, anchor='mm')
    MB = (220, 150, 860, 690); mirror(d, MB)
    towel(d, 975, 300, 0.9)                    # 진짜 수건(오른쪽 벽)
    k = ease((t-0.4)/1.2)
    # 거울 속: 아이 얼굴, 화면 오른쪽 손 듦(같은 쪽) — 수건도 거울 속 오른쪽 끝에 살짝
    mirror_clip = Image.new('L', (W, H), 0); ImageDraw.Draw(mirror_clip).rounded_rectangle(MB, radius=28, fill=255)
    layer = Image.new('RGB', (W, H), GLASS); dl = ImageDraw.Draw(layer)
    dl.line([MB[0]+40, MB[1]+120, MB[0]+120, MB[1]+40], fill=GLASS_L, width=14)
    towel(dl, 815, 260, 0.6)
    mhx, mhy = front_person(dl, 540+0.95*(78)+0.95*60-91, 650, 0.66, k, +1, KID_SHIRT, mood='wow' if t > 2.0 else 'smile')
    im.paste(layer, (0, 0), mirror_clip); d = ImageDraw.Draw(im)
    kid_back(d, 540, 1110, 0.95, k)
    lab(im, '왼손?', (mhx-10, mhy-90), LT, t, 2.0)
    return im


# ---------------- 장면 2: 거울 vs 마주 선 아빠 ----------------
S2 = int(12.6*F)
PX = (270, 810)          # 두 칸 가운데
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), TILE); d = bathroom(im)
    d.text((W/2, 80), '손은 어느 쪽에 있을까?', font=FBW, fill=TXT, anchor='mm')
    k = ease((t-1.0)/3.0)
    g = ease((t-4.2)/1.2)
    # 왼쪽 칸: 거울
    MB = (40, 200, 500, 700); mirror(d, MB)
    d.line([540, 180, 540, 1040], fill=TILE_L, width=6)
    # 오른쪽 칸: 아빠(벽 앞)
    d.rounded_rectangle([580, 200, 1040, 700], radius=28, fill=(236, 230, 242))
    d.text((PX[0], 150), '거울', font=FHD, fill=TXT, anchor='mm')
    d.text((PX[1], 150), '아빠', font=FHD, fill=TXT, anchor='mm')
    # 아이 손 위치(미리 계산해서 빛줄기를 뒤에 깐다)
    for cx, mode in ((PX[0], 'mirror'), (PX[1], 'dad')):
        kx = cx+80-17.6+math.cos(math.radians(-60))*96
        if g > 0:
            a = int(255*g*0.85)
            band = Image.new('RGBA', (W, H), (0, 0, 0, 0)); db = ImageDraw.Draw(band)
            db.rounded_rectangle([kx-34, 300, kx+34, 860], radius=34, fill=GLOW+(a,))
            im.paste(Image.alpha_composite(im.convert('RGBA'), band).convert('RGB')); d = ImageDraw.Draw(im)
    mclip = Image.new('L', (W, H), 0); ImageDraw.Draw(mclip).rounded_rectangle(MB, radius=28, fill=255)
    layer = im.copy(); dl = ImageDraw.Draw(layer)
    front_person(dl, PX[0]+24.8, 680, 0.62, k, +1, KID_SHIRT)
    im.paste(layer, (0, 0), mclip); d = ImageDraw.Draw(im)
    pclip = Image.new('L', (W, H), 0); ImageDraw.Draw(pclip).rounded_rectangle([580, 200, 1040, 700], radius=28, fill=255)
    layer = im.copy(); dl = ImageDraw.Draw(layer)
    front_person(dl, PX[1], 690, 0.78, k, -1, DAD_SHIRT)
    im.paste(layer, (0, 0), pclip); d = ImageDraw.Draw(im)
    kid_back(d, PX[0], 1070, 0.8, k)
    kid_back(d, PX[1], 1070, 0.8, k)
    lab(im, '같은 쪽', (PX[0], 250), LM, t, 4.8)
    lab(im, '반대쪽', (PX[1], 250), LT, t, 6.2)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/mirror_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('mirror', s1, S1, s2, S2, out,
              preview=[(s1, int(3.5*F), S1), (s2, int(2.5*F), S2), (s2, int(5.5*F), S2), (s2, int(12.0*F), S2)])
