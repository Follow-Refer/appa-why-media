"""벌써 깜깜해! 해님 벌써 자러 갔어?(11/25): 상황(하원길 다섯 시 반, 어둑한 하늘, 가방 멘 아이)
→ 답(여름 하늘·겨울 하늘을 나란히, 같은 시계로 하루가 흐름: 여름 해님은 높이 길게,
   겨울 해님은 낮게 짧게 가서 먼저 짐. 겨울 쪽만 먼저 깜깜해지고 창문에 불이 켜짐).
사용: python3 example_early_sunset_v5.py out.mp4 [preview.png]"""
import sys, math, random
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import lab, stander, KID_SHIRT

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FCK = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 34, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LY = (226, 186, 110)
DAY_T, DAY_B = (176, 206, 238), (226, 238, 248)
DUSK_T, DUSK_B = (150, 150, 206), (246, 204, 186)
NIGHT_T, NIGHT_B = (70, 78, 128), (120, 120, 170)
SUN = (250, 214, 130); SUN_GLOW = (252, 234, 180)
BLD = [(206, 200, 222), (196, 206, 224), (214, 204, 214)]
BLD_N = [(98, 100, 146), (92, 104, 148), (106, 100, 140)]
WIN_N = (246, 222, 150)
GROUND = (196, 214, 190); GROUND_N = (92, 110, 120)
BAG = (140, 160, 210)


def sky(d, x0, x1, y0, gy, night, dusk):
    for yy in range(y0, gy):
        f = (yy-y0)/(gy-y0)
        top = mix(mix(DAY_T, DUSK_T, dusk), NIGHT_T, night)
        bot = mix(mix(DAY_B, DUSK_B, dusk), NIGHT_B, night)
        d.line([(x0, yy), (x1, yy)], fill=mix(top, bot, f))


def sun(d, cx, cy, r):
    d.ellipse([cx-r*1.5, cy-r*1.5, cx+r*1.5, cy+r*1.5], fill=SUN_GLOW)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SUN)


def town(d, x0, x1, gy, night, lights, seed=3, scale=1.0):
    rnd = random.Random(seed)
    w = x1-x0
    xs = [(0.00, 0.20, 0.70), (0.20, 0.38, 0.62), (0.62, 0.80, 0.74), (0.80, 1.00, 0.66)]
    for j, (a, b, top) in enumerate(xs):
        col = mix(BLD[j % 3], BLD_N[j % 3], night)
        bx0, bx1 = x0+w*a, x0+w*b-10
        ty = gy-(gy-200)*(1-top)*scale
        d.rounded_rectangle([bx0, ty, bx1, gy+20], radius=14, fill=col)
        for wy in range(int(ty+30), gy-24, 50):
            for wx in range(int(bx0+16), int(bx1-26), 36):
                on = rnd.random() < 0.6
                wc = mix(mix(col, (236, 240, 250), 0.35), WIN_N, lights if on else 0)
                d.rounded_rectangle([wx, wy, wx+16, wy+24], radius=4, fill=wc)
    d.rectangle([x0, gy, x1, H], fill=mix(GROUND, GROUND_N, night))


def kid(d, cx, gy, s, mood):
    # 가방(등 뒤, 몸보다 먼저 그려 어깨 뒤로 살짝 보이게)
    stander(d, cx, gy, s, 0, KID_SHIRT, 72, mood=mood)


# ---------------- 장면 1: 하원길 다섯 시 반 ----------------
S1 = int(3.6*F)
GY1 = 860
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    sky(d, 0, W, 0, GY1, 0.55, 0.6)
    town(d, 0, W, GY1, 0.55, 0.9)
    # 가로등
    for lx in (200, 880):
        d.rounded_rectangle([lx-8, 560, lx+8, GY1], radius=6, fill=(150, 146, 170))
        d.ellipse([lx-30, 530, lx+30, 590], fill=(252, 236, 170))
    d.text((W/2, 80), '벌써 깜깜해!', font=FBW, fill=(244, 240, 252), anchor='mm')
    kid(d, 540, 1040, 0.8, 'wow' if t > 1.0 else 'smile')
    return im


# ---------------- 장면 2: 여름 하늘 | 겨울 하늘, 같은 시계 ----------------
S2 = int(14.2*F)
GY2 = 820
T0, T1 = 1.4, 9.4          # 시계가 흐르는 구간(초)
H0, H1 = 5.0, 18.5         # 05:00 → 18:30
SUMMER = (5.2, 19.9, 560)  # 해 뜨는 시각, 지는 시각, 하늘 높이(px)
WINTER = (7.7, 17.3, 300)
PANELS = [(0, 534, SUMMER, '여름'), (546, W, WINTER, '겨울')]


def clock_h(t):
    return H0+(H1-H0)*max(0, min(1, (t-T0)/(T1-T0)))


def sun_pos(x0, x1, spec, h):
    rise, sset, ry = spec
    u = (h-rise)/(sset-rise)
    cx = (x0+x1)/2; rx = (x1-x0)/2-75
    th = math.pi*u
    return cx-rx*math.cos(th), GY2+20-ry*math.sin(th), u


def panel_state(spec, h):
    rise, sset, _ = spec
    # 해 뜨기 전/진 뒤는 밤, 앞뒤 0.5시간 노을
    if h < rise: night = min(1, (rise-h)/0.6); dusk = 1-night
    elif h > sset: night = min(1, (h-sset)/0.6); dusk = 1-night
    else:
        night = 0
        dusk = max(0, 1-min(h-rise, sset-h)/0.8)
    return night, dusk


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=BG)
    h = clock_h(t)
    pos = {}
    for (x0, x1, spec, name) in PANELS:
        night, dusk = panel_state(spec, h)
        sky(d, x0, x1, 150, GY2, night, dusk)
        # 하늘 길(옅은 점)
        for q in range(1, 30):
            rise, sset, ry = spec
            px, py, _ = sun_pos(x0, x1, spec, rise+(sset-rise)*q/30)
            d.ellipse([px-4, py-4, px+4, py+4], fill=mix(mix(DAY_B, (255, 255, 255), 0.5), (150, 154, 196), night))
        sx, sy, u = sun_pos(x0, x1, spec, h)
        if -0.05 < u < 1.05: sun(d, sx, sy, 40)
        town(d, x0, x1, GY2, night, night, seed=5 if name == '여름' else 9, scale=0.55)
        pos[name] = (sx, sy, u, night)
        d.text(((x0+x1)/2, 1000), name, font=FBW, fill=mix(TXT, (244, 240, 252), night), anchor='mm')
    d.rectangle([534, 150, 546, H], fill=BG)
    # 시계(가운데 위, 아이도 아는 동그란 시계)
    cx, cy, r = 540, 80, 50
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255), outline=TXT, width=5)
    hh = h % 12; mm = (h % 1)*60
    ah = math.radians(hh*30-90); am = math.radians(mm*6-90)
    d.line([(cx, cy), (cx+28*math.cos(ah), cy+28*math.sin(ah))], fill=TXT, width=7)
    d.line([(cx, cy), (cx+40*math.cos(am), cy+40*math.sin(am))], fill=TXT, width=4)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=TXT)
    # 라벨(같은 말: 높이 길게 / 낮게 짧게 / 벌써 깜깜)
    ss = pos['여름']; ww = pos['겨울']
    lab(im, '높이 길게', (267, 420), LY, t, 4.0, 9.6)
    if ww[2] < 1.0: lab(im, '낮게 짧게', (ww[0], ww[1]-90), LM, t, 4.6, 8.6)
    lab(im, '벌써 깜깜', (813, 420), LM, t, 10.0)
    lab(im, '아직 환해', (267, 420), LY, t, 10.6)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/early_sunset_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('early_sunset', s1, S1, s2, S2, out,
              preview=[(s1, int(2.6*F), S1), (s2, int(3.5*F), S2), (s2, int(6.5*F), S2), (s2, int(13.5*F), S2)])
