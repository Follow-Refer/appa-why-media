"""달이 왜 낮에 나왔어?(11/18): 상황(하원길 오후, 파란 하늘에 하얀 반달, 아이가 올려다봄)
→ 답(같은 동네 하늘, 시간이 흐름: 해님이 서쪽으로 지는 동안 달도 뒤따라 하늘을 건넘.
   낮에도 달은 하늘에 있었고, 깜깜해지면 더 밝게 보이고 별도 나타남).
사용: python3 example_daytime_moon_v5.py out.mp4 [preview.png]"""
import sys, math, random
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *
from example_yawn_catch_v5 import lab, stander, KID_SHIRT

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LY = (226, 186, 110)
DAY_T, DAY_B = (176, 206, 238), (226, 238, 248)
DUSK_T, DUSK_B = (150, 150, 206), (246, 204, 186)
NIGHT_T, NIGHT_B = (70, 78, 128), (120, 120, 170)
SUN = (250, 214, 130); SUN_GLOW = (252, 234, 180)
BLD = [(206, 200, 222), (196, 206, 224), (214, 204, 214)]
BLD_N = [(98, 100, 146), (92, 104, 148), (106, 100, 140)]
WIN_N = (246, 222, 150)
GROUND = (196, 214, 190); GROUND_N = (92, 110, 120)
GY = 860   # 땅(지평선)


def sky(d, night, dusk):
    for yy in range(GY):
        f = yy/GY
        top = mix(mix(DAY_T, DUSK_T, dusk), NIGHT_T, night)
        bot = mix(mix(DAY_B, DUSK_B, dusk), NIGHT_B, night)
        d.line([(0, yy), (W, yy)], fill=mix(top, bot, f))


def moon(d, cx, cy, r, night, bg):
    """상현 무렵 반달(오른쪽이 밝음). 낮엔 하얗고 옅게, 밤엔 노랗고 밝게."""
    lit = mix((250, 250, 252), (252, 240, 190), night)
    dark = mix(bg, (150, 156, 196), 0.18)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=dark)
    # 오른쪽 반 + 조금 더(차오르는 중)
    d.pieslice([cx-r, cy-r, cx+r, cy+r], -90, 90, fill=lit)
    k = 0.18
    d.ellipse([cx-r*k, cy-r, cx+r*k, cy+r], fill=lit)


def sun(d, cx, cy, r):
    d.ellipse([cx-r*1.5, cy-r*1.5, cx+r*1.5, cy+r*1.5], fill=SUN_GLOW)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SUN)


def town(d, night, lights=0.0):
    rnd = random.Random(3)
    xs = [(-20, 150, 620), (150, 300, 560), (300, 430, 680), (650, 790, 600), (790, 930, 660), (930, 1100, 580)]
    for j, (x0, x1, top) in enumerate(xs):
        col = mix(BLD[j % 3], BLD_N[j % 3], night)
        d.rounded_rectangle([x0, top, x1-12, GY+20], radius=18, fill=col)
        for wy in range(top+40, GY-30, 62):
            for wx in range(x0+24, x1-40, 46):
                on = rnd.random() < 0.55
                wc = mix(mix(col, (236, 240, 250), 0.35), WIN_N, lights if on else 0)
                d.rounded_rectangle([wx, wy, wx+22, wy+30], radius=5, fill=wc)
    d.rectangle([0, GY, W, H], fill=mix(GROUND, GROUND_N, night))


def arc_pt(th, cx=540, cy=GY+40, rx=560, ry=700):
    """θ=0: 왼쪽(동쪽) 지평선, θ=π/2: 남쪽 하늘 꼭대기, θ=π: 오른쪽(서쪽) 지평선."""
    return cx-rx*math.cos(th), cy-ry*math.sin(th)


# ---------------- 장면 1: 하원길 오후 ----------------
S1 = int(3.6*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    sky(d, 0, 0)
    sun(d, 930, 300, 52)
    moon(d, 300, 360, 62, 0, mix(DAY_T, DAY_B, 360/GY))
    town(d, 0)
    d.text((W/2, 80), '달이 왜 낮에 나왔어?', font=FBW, fill=TXT, anchor='mm')
    # 아이(오른쪽 아래, 몸은 짧게) + 달 옆 반짝임
    stander(d, 640, 1040, 0.8, 0, KID_SHIRT, 72, mood='wow' if t > 1.0 else 'smile')
    tw = 0.5+0.5*math.sin(t*5)
    if t > 1.0:
        for (sx, sy) in ((390, 300), (220, 430)):
            rr = 10+6*tw
            d.line([(sx-rr, sy), (sx+rr, sy)], fill=(255, 255, 255), width=5)
            d.line([(sx, sy-rr), (sx, sy+rr)], fill=(255, 255, 255), width=5)
    lab(im, '낮에 달?', (300, 500), LT, t, 1.3)
    return im


# ---------------- 장면 2: 시간이 흐르는 같은 하늘 ----------------
S2 = int(14.0*F)
T0, T1 = 1.6, 9.6               # 움직이는 구간
SUN0, MOON0, DTH = 0.66*math.pi, 0.20*math.pi, 0.48*math.pi
rnd = random.Random(11)
STARS = [(rnd.randint(40, 1040), rnd.randint(150, 600), rnd.random()) for _ in range(26)]


def prog(t): return ease((t-T0)/(T1-T0))


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    p = prog(t)
    th_s = SUN0+DTH*p; th_m = MOON0+DTH*p
    sx, sy = arc_pt(th_s); mx, my = arc_pt(th_m)
    dusk = max(0, min(1, (th_s-0.86*math.pi)/(0.1*math.pi))) * (1-max(0, min(1, (th_s-1.0*math.pi)/(0.12*math.pi))))
    night = max(0, min(1, (th_s-0.98*math.pi)/(0.14*math.pi)))
    sky(d, night, dusk)
    # 하늘 길(아주 옅은 점선)
    for q in range(1, 40):
        x, y = arc_pt(math.pi*q/40)
        if y < GY-20:
            d.ellipse([x-4, y-4, x+4, y+4], fill=mix(mix(DAY_B, (255, 255, 255), 0.5), (150, 154, 196), night))
    # 별(밤에 나타남)
    if night > 0:
        for (x, y, ph) in STARS:
            a = night*(0.6+0.4*math.sin(t*3+ph*6))
            c = mix(mix(NIGHT_T, NIGHT_B, y/GY), (255, 248, 220), a)
            r = 4+3*ph
            d.polygon([(x, y-r*2), (x+r*0.6, y-r*0.6), (x+r*2, y), (x+r*0.6, y+r*0.6),
                       (x, y+r*2), (x-r*0.6, y+r*0.6), (x-r*2, y), (x-r*0.6, y-r*0.6)], fill=c)
    if sy < GY+60: sun(d, sx, sy, 52)
    moon(d, mx, my, 62, night, mix(mix(mix(DAY_T, DUSK_T, dusk), NIGHT_T, night), mix(mix(DAY_B, DUSK_B, dusk), NIGHT_B, night), my/GY))
    town(d, night, lights=night)
    stander(d, 640, 1040, 0.8, 0, KID_SHIRT, 72, mood='smile')
    d.text((W/2, 80), '달은 어디 있었을까?', font=FBW, fill=mix(TXT, (244, 240, 252), night), anchor='mm')
    # 라벨: 해님·달은 따라다님
    lab(im, '해님', (sx, sy+110), LY, t, 0.4, 6.6)
    lab(im, '달', (mx, my+110), LM, t, 0.9)
    lab(im, '낮에도 놀러 와', (540, 300), LT, t, 2.6, 7.2)
    lab(im, '별도 있었어', (300, 210), LY, t, 10.2)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/daytime_moon_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('daytime_moon', s1, S1, s2, S2, out,
              preview=[(s1, int(2.6*F), S1), (s2, int(4.0*F), S2), (s2, int(8.4*F), S2), (s2, int(13.5*F), S2)])
