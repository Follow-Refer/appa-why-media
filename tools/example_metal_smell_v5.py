"""철봉 냄새가 내 손에 묻었어!(11/27): 상황(놀이터 철봉에서 내려와 손 냄새 킁킁) →
답(철봉만: 냄새 없음 / 손: 땀·기름 / 손이 철봉을 잡으면 그 자리에서 새 냄새가 생김).
사용: python3 example_metal_smell_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import face, lab, KID_SHIRT

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210)
SKY_T = (206, 220, 240); SKY_B = (238, 234, 244)
GROUND = (214, 200, 176); GRASS = (178, 210, 182)
POST = (150, 176, 214); POST_D = (122, 148, 190)
BAR = (186, 194, 210); BAR_D = (150, 160, 180); BAR_L = (230, 234, 242)
SMELL = (196, 170, 220)
SKIN_D = (236, 204, 176)


def sky(im):
    d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(SKY_T, SKY_B, y/H))
    return d


def overlay(im, fn):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(layer))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def wisps(dl, cx, cy, t, a, n=3, spread=46, rise=150, scale=1.0):
    """부드러운 물결 냄새 줄기 n개, 위로 천천히 올라감."""
    if a <= 0: return
    for k in range(n):
        x0 = cx+(k-(n-1)/2)*spread
        ph = (t*0.6+k*0.33) % 1
        pts = []
        for j in range(14):
            u = j/13
            y = cy-u*rise*scale-ph*30
            x = x0+math.sin(u*2*math.pi*1.2+t*2+k)*14*scale
            pts.append((x, y))
        A = int(220*a*(1-0.5*ph))
        dl.line(pts, fill=SMELL+(A,), width=max(5, int(10*scale)), joint='curve')


# ---------------- 장면 1: 철봉에서 내려와 킁킁 ----------------
S1 = int(3.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = sky(im)
    d.text((W/2, 80), '철봉 냄새가 손에 묻었어!', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=GROUND)
    d.rectangle([0, 840, W, 870], fill=GRASS)
    # 철봉 틀(오른쪽)
    d.rounded_rectangle([640, 300, 676, 870], radius=16, fill=POST)
    d.rounded_rectangle([960, 300, 996, 870], radius=16, fill=POST)
    d.rounded_rectangle([630, 300, 1006, 336], radius=18, fill=BAR, outline=BAR_D, width=4)
    # 아이(왼쪽): 몸 + 다리 + 짧은 팔, 손을 코 앞에
    cx, cy = 380, 430
    d.rounded_rectangle([cx-30, 760, cx-6, 860], radius=12, fill=(130, 150, 190))
    d.rounded_rectangle([cx+6, 760, cx+30, 860], radius=12, fill=(130, 150, 190))
    d.rounded_rectangle([cx-95, 560, cx+95, 780], radius=60, fill=KID_SHIRT)
    d.line([cx-80, 610, cx-120, 720], fill=KID_SHIRT, width=46)          # 왼팔 내림
    d.ellipse([cx-146, 700, cx-96, 750], fill=SKIN)
    up = ease((t-0.2)/1.0)
    hx, hy = cx+150-50*up, 700-190*up                                     # 오른손이 코 앞으로
    d.line([cx+75, 600, hx-10, hy+30], fill=KID_SHIRT, width=46)
    face(d, cx, cy, 120, 0, mood='wow' if t > 1.4 else 'smile')
    d.ellipse([hx-42, hy-36, hx+42, hy+40], fill=SKIN)
    for k in range(4):                                                    # 손가락 끝 살짝
        d.ellipse([hx-38+k*20, hy-50, hx-18+k*20, hy-24], fill=SKIN)
    g = ease((t-1.2)/0.8)
    overlay(im, lambda dl: wisps(dl, hx+10, hy-60, t, g, n=2, spread=36, rise=110, scale=0.8))
    lab(im, '킁킁?', (hx+140, hy-120), LM, t, 1.6)
    return im


# ---------------- 장면 2: 철봉만 / 손만 / 만나면 ----------------
BY = 330          # 철봉 높이(가운데선)
def big_bar(d):
    d.rounded_rectangle([-20, BY-46, W+20, BY+46], radius=46, fill=BAR, outline=BAR_D, width=6)
    d.rounded_rectangle([40, BY-30, W-40, BY-16], radius=7, fill=BAR_L)


def big_hand(d, x, y, curl=0.0):
    """손등이 보이는 오른손(손가락 위쪽). (x,y)=손바닥 위 가장자리 가운데. 짧은 손목까지만."""
    d.rounded_rectangle([x-150, y+150, x+70, y+420], radius=60, fill=(246, 200, 150))   # 소매
    d.rounded_rectangle([x-130, y, x+130, y+220], radius=90, fill=SKIN)                # 손바닥
    for k, (dx, ln) in enumerate(((-90, 150), (-30, 175), (30, 170), (88, 140))):
        L = ln*(1-0.62*curl)
        d.rounded_rectangle([dx+x-26, y-L+40, dx+x+26, y+60], radius=26, fill=SKIN)
        if curl > 0.9: d.ellipse([dx+x-16, y-L+46, dx+x+16, y-L+72], fill=SKIN_D)
    d.rounded_rectangle([x-200, y+70, x-110, y+130], radius=30, fill=SKIN)             # 엄지


def dots(dl, x, y, a):
    """손 위 반짝이는 작은 땀·기름 방울."""
    if a <= 0: return
    for (dx, dy, r) in ((-90, -60, 12), (-30, -100, 10), (30, -80, 13), (88, -40, 11), (-60, 80, 14), (40, 120, 12), (0, 30, 10), (90, 70, 12)):
        X, Y = x+dx, y+dy
        dl.ellipse([X-r, Y-r, X+r, Y+r], fill=(214, 232, 248, int(230*a)), outline=(150, 176, 214, int(255*a)), width=3)
        dl.ellipse([X-r*0.5, Y-r*0.6, X-r*0.05, Y-r*0.15], fill=(255, 255, 255, int(255*a)))


S2 = int(13.8*F)
HX = 540
def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = sky(im)
    big_bar(d)
    # 0~3초: 철봉만, 냄새 없음 (코가 킁킁해도 아무것도 안 올라옴)
    # 3~6초: 손이 아래에서 올라옴(땀·기름 반짝)
    # 6.5~9초: 손이 철봉을 잡음 → 맞닿은 자리에서 냄새 줄기
    come = ease((t-2.8)/1.4)
    grab = ease((t-6.4)/1.6)
    hy = (1150-430*come)*(1-grab) + (BY+10)*grab
    big_hand(d, HX, hy, curl=grab)                      # 손가락이 짧아지며 철봉을 감싸 쥠
    da = ease((t-3.6)/0.6)*(1-ease((t-7.6)/0.6))
    overlay(im, lambda dl: dots(dl, HX, hy+110, da))
    # 접촉 반짝
    sp = max(0, 1-abs(t-8.0)/0.5)
    if sp > 0:
        for k in range(8):
            ang = k*math.pi/4; r0, r1 = 150, 150+50*sp
            d.line([HX+math.cos(ang)*r0, BY+math.sin(ang)*r0*0.6, HX+math.cos(ang)*r1, BY+math.sin(ang)*r1*0.6], fill=YEL, width=8)
    g = ease((t-8.2)/1.6)
    overlay(im, lambda dl: wisps(dl, HX, BY-70, t, g, n=4, spread=70, rise=180, scale=1.1))
    lab(im, '냄새 없어', (HX, 560), LM, t, 0.6, 2.9)
    lab(im, '땀·기름', (820, 820), LM, t, 4.2, 7.4)
    lab(im, '새 냄새 짠!', (230, 150), LT, t, 9.0)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/metal_smell_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('metalsmell', s1, S1, s2, S2, out,
              preview=[(s1, int(3.0*F), S1), (s2, int(2.0*F), S2), (s2, int(5.5*F), S2), (s2, int(12.5*F), S2)])
