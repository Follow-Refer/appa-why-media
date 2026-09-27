"""9/29 편: 빨대 / 모기 / 풍선 — 달 영상 문법(문장 없음, 라벨 4개까지, 원리는 움직임)."""
from v2_videos import *
import random

def lab(im, text, xy, col, t, t0, t1=None):
    a = min(1, max(0, (t-t0)/0.5))
    if t1 is not None: a *= max(0, min(1, (t1-t)/0.5))
    fade_pill(im, text, xy, col, a)

def blend(im, draw_fn):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(layer))
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))
    return ImageDraw.Draw(im)

def dashed(d, a, b, col, w=8, dash=26, k=1.0):
    L = math.dist(a, b)*k; n = int(L//dash)
    for j in range(0, n, 2):
        f0 = j*dash/math.dist(a, b); f1 = min(k, (j+1)*dash/math.dist(a, b))
        d.line([(a[0]+(b[0]-a[0])*f0, a[1]+(b[1]-a[1])*f0), (a[0]+(b[0]-a[0])*f1, a[1]+(b[1]-a[1])*f1)], fill=col, width=w)

# ================= 빨대 =================
WATER = (170, 206, 236); GLASS = (200, 214, 230); STRAW = (236, 120, 130); STRAW_S = (250, 196, 200); TABLE = (222, 200, 172)
GX0, GX1, GY0, GY1, WY = 380, 800, 330, 900, 540
A = (470, 250)                       # 빨대 윗끝 (컵 밖)
P = (700, 860)                       # 물속 실제 끝
def on_line(a, b, y): return (a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]), y)
S_IN = on_line(A, P, WY)             # 물 표면에서 빨대가 들어가는 점
GHOST = (S_IN[0]+230, 760)           # 눈에 보이는 물속 끝 (더 얕고 옆으로)
def glass(d, water=True):
    d.rectangle([0, 900, W, H], fill=TABLE)
    if water: d.rectangle([GX0+10, WY, GX1-10, GY1-10], fill=WATER)
    d.line([GX0, GY0, GX0+10, GY1], fill=GLASS, width=16); d.line([GX1, GY0, GX1-10, GY1], fill=GLASS, width=16)
    d.line([GX0+10, GY1, GX1-10, GY1], fill=GLASS, width=16)
    if water: d.line([GX0+12, WY, GX1-12, WY], fill=(130, 176, 220), width=6)
def straw_seg(d, a, b, col=STRAW, w=34): d.line([a, b], fill=col, width=w); d.ellipse([b[0]-w/2, b[1]-w/2, b[0]+w/2, b[1]+w/2], fill=col)
ST1 = 7*F
def st_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    title(d, '빨대 부러졌어!')
    lift = ease((t-4.2)/0.8)*340; lay = ease((t-5.0)/0.9)
    glass(d)
    if lift <= 0:
        straw_seg(d, S_IN, GHOST); straw_seg(d, A, S_IN)      # 부러져 보이는 모습
    elif lay <= 0:
        a2 = (A[0], A[1]-lift); p2 = (P[0], P[1]-lift)
        if p2[1] > WY:
            f = (p2[1]-WY)/(P[1]-WY); s2 = on_line(a2, p2, WY)
            g2 = (s2[0]+(GHOST[0]-S_IN[0])*f, WY+(GHOST[1]-WY)*f)
            straw_seg(d, s2, g2); straw_seg(d, a2, s2)
        else: straw_seg(d, a2, p2)
    else:  # 식탁 위에 눕혀서 보여 줌: 곧은 빨대
        a2 = (A[0], A[1]-340); p2 = (P[0], P[1]-340); A3, P3 = (170, 985), (770, 985)
        straw_seg(d, (a2[0]+(A3[0]-a2[0])*lay, a2[1]+(A3[1]-a2[1])*lay), (p2[0]+(P3[0]-p2[0])*lay, p2[1]+(P3[1]-p2[1])*lay))
    lab(im, '빨대: 뚝?', (900, 640), LT, t, 1.0, 4.2)
    lab(im, '꺼내면: 멀쩡', (900, 860), LG, t, 5.6)
    return im
ST2 = 10*F
EYE = (150, 330)
def st_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    title(d, '옆에서 보면')
    glass(d)
    # 아이 옆얼굴 + 눈
    d.ellipse([EYE[0]-150, EYE[1]-120, EYE[0]+60, EYE[1]+120], fill=SKIN); d.ellipse([EYE[0]+10, EYE[1]-16, EYE[0]+36, EYE[1]+10], fill=INK)
    # 실제 빨대: 물 위는 진하게, 물속은 연하게(진짜 자리)
    straw_seg(d, S_IN, P, col=STRAW_S); straw_seg(d, A, S_IN)
    # 빛: 물속 끝 P → 수면 Q → 눈
    Q = (560, WY)
    k1 = ease((t-0.8)/1.3); k2 = ease((t-2.1)/1.3)
    if k1 > 0: d.line([P, (P[0]+(Q[0]-P[0])*k1, P[1]+(Q[1]-P[1])*k1)], fill=YEL, width=12)
    if k2 > 0:
        e = (EYE[0]+40, EYE[1]); d.line([Q, (Q[0]+(e[0]-Q[0])*k2, Q[1]+(e[1]-Q[1])*k2)], fill=YEL, width=12)
    # 눈이 믿는 곧은 선: 눈 → Q 방향 그대로 물속으로 연장 (점선)
    k3 = ease((t-4.2)/1.2)
    if k3 > 0:
        e = (EYE[0]+40, EYE[1]); dx, dy = Q[0]-e[0], Q[1]-e[1]; s = (GHOST[1]-Q[1])/dy
        G = (Q[0]+dx*s, GHOST[1]); dashed(d, Q, G, (190, 170, 110), w=8, k=k3)
        # 눈에 보이는 가짜 끝: G 쪽으로 빨대가 '있는 것처럼'
        k4 = ease((t-5.4)/1.0)
        if k4 > 0:
            g = (S_IN[0]+(G[0]-S_IN[0])*k4, S_IN[1]+(G[1]-S_IN[1])*k4)
            d = blend(im, lambda dd: straw_seg(dd, S_IN, g, col=STRAW+(int(200*k4),)))
    lab(im, '빛: 꺾여', (Q[0]-40, WY-110), LM, t, 2.4)
    lab(im, '눈이 속았다!', (860, 980), LT, t, 6.4)
    return im

# ================= 모기 =================
NT1 = (54, 60, 96); NT2 = (84, 86, 124); BED = (200, 190, 220); BLANKET = (150, 170, 214); PILLOW = (236, 232, 244); MOS = (60, 58, 70)
def mosquito(d, x, y, s=1.0, flap=0):
    d.line([x-26*s, y+10*s, x-46*s, y+34*s], fill=MOS, width=int(4*s)); d.line([x+6*s, y+12*s, x+14*s, y+38*s], fill=MOS, width=int(4*s)); d.line([x+22*s, y+10*s, x+42*s, y+34*s], fill=MOS, width=int(4*s))
    d.ellipse([x-34*s, y-8*s, x+20*s, y+14*s], fill=MOS); d.ellipse([x+14*s, y-12*s, x+34*s, y+8*s], fill=MOS)
    d.line([x+32*s, y, x+58*s, y+14*s], fill=MOS, width=int(3*s))
    wy = -30*s if flap % 2 == 0 else -18*s
    d.ellipse([x-24*s, y+wy-8*s, x+8*s, y+wy+14*s], fill=(220, 226, 240)); d.ellipse([x-6*s, y+wy-4*s, x+22*s, y+wy+16*s], fill=(206, 214, 234))
def night_bg(d, title_txt):
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(NT1, NT2, y/H))
    d.text((W/2, 80), title_txt, font=FBW, fill=(240, 236, 250), anchor='mm')
def sleeper(d, hx, hy, r, closed=True):
    d.ellipse([hx-r, hy-r, hx+r, hy+r], fill=SKIN)
    for ex in (hx-r*0.38, hx+r*0.38): d.arc([ex-r*0.18, hy-r*0.18, ex+r*0.18, hy+r*0.06], 20, 160, fill=INK, width=max(4, int(r*0.07)))
NM1 = 7*F
def mq_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    night_bg(d, '모기는 왜 나만 물어?')
    d.rounded_rectangle([90, 520, 990, 900], radius=40, fill=BED)
    d.rounded_rectangle([130, 470, 440, 600], radius=40, fill=PILLOW); d.rounded_rectangle([580, 470, 900, 600], radius=40, fill=PILLOW)
    sleeper(d, 280, 520, 100); sleeper(d, 740, 540, 78)          # 아빠(왼쪽) · 아이(오른쪽)
    d.rounded_rectangle([110, 600, 970, 880], radius=40, fill=BLANKET)
    arm = [(760, 640), (930, 700)]; d.line(arm, fill=SKIN, width=46); d.ellipse([905, 676, 955, 726], fill=SKIN)   # 이불 밖 아이 팔
    # 모기: 왼쪽 위에서 지그재그로 날아와 아이 팔에 앉음
    k = ease((t-0.4)/4.0); x = 60+(880-60)*k + 40*math.sin(t*5)*(1-k); y = 260+(660-260)*k + 50*math.sin(t*7)*(1-k)
    mosquito(d, x, y, 1.3, flap=i if k < 1 else 0)
    if t > 5.0:
        a = min(1, (t-5.0)/0.8)
        d = blend(im, lambda dd: [dd.ellipse([cx-24, cy-18, cx+24, cy+18], fill=(240, 150, 160, int(230*a))) for cx, cy in ((860, 672), (820, 660))])
    lab(im, '모기: 윙~', (300, 300), LT, t, 0.8)
    return im
NM2 = 10*F
def mq_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    night_bg(d, '모기가 찾아가는 길')
    hx, hy = 800, 560
    # 따뜻함(주황빛 테두리) 6초부터
    wa = ease((t-5.4)/1.0)
    if wa > 0:
        d = blend(im, lambda dd: [dd.ellipse([hx-150-g, hy-150-g, hx+150+g, hy+330+g], outline=(250, 170, 110, int(90*wa*(1-g/90))), width=16) for g in range(0, 90, 18)])
    # 아이 옆얼굴(왼쪽 보고 누움) + 팔
    d.ellipse([hx-130, hy-130, hx+130, hy+130], fill=SKIN); d.arc([hx-80, hy-30, hx-40, hy+6], 20, 160, fill=INK, width=6)
    d.ellipse([hx-128, hy+30, hx-104, hy+56], fill=LIP)
    d.rounded_rectangle([hx-100, hy+140, hx+120, hy+320], radius=60, fill=(180, 200, 230)); d.line([(hx-60, hy+220), (hx-230, hy+280)], fill=SKIN, width=44)
    # 숨 구름: 입에서 왼쪽으로 흘러가는 길 (계속 나옴)
    puffs = []
    for j in range(16):
        born = j*0.7
        if t > born:
            age = t-born; px = hx-150-age*120; py = hy+44-age*16+18*math.sin(age*2+j)
            if px > -80: puffs.append((px, py, 26+age*9, max(0.15, 0.7-age*0.07)))
    d = blend(im, lambda dd: [dd.ellipse([x-r, y-r*0.7, x+r, y+r*0.7], fill=(230, 236, 250, int(255*a))) for x, y, r, a in puffs])
    # 모기: 2초부터 왼쪽 끝에서 숨 길을 따라 들어옴 → 7.5초 팔에 앉음
    k = ease((t-2.0)/5.5); x = 40+(hx-210-40)*k; y = hy-60+60*k*k+30*math.sin(t*6)*(1-k)+ (230*ease((t-6.4)/1.1))
    if t > 1.6: mosquito(d, x, y, 1.2, flap=i if t < 7.5 else 0)
    lab(im, '숨: 후~', (hx-330, hy-150), LM, t, 0.8)
    lab(im, '따뜻해', (hx+40, hy-230), LT, t, 5.8)
    lab(im, '살 냄새', (hx-400, hy+380), LG, t, 7.2)
    return im
def mq_sounds(total, sr):
    y = np.zeros(int(sr*total)); tt = np.arange(len(y))/sr
    buzz = 0.05*np.sin(2*np.pi*(520+30*np.sin(2*np.pi*3*tt))*tt)
    m = np.zeros(len(y)); a, b = int(sr*0.4), int(sr*4.6); m[a:b] = 1
    base = NM1/F-1.0; a2, b2 = int(sr*(base+2.0)), int(sr*(base+7.5)); m[a2:min(b2, len(y))] = 1
    from numpy import convolve
    m = convolve(m, np.ones(2000)/2000, mode='same')
    return buzz*m

# ================= 풍선 =================
BAL = (236, 110, 120); BAL_H = (250, 190, 196); PARK = (186, 214, 160); DAY1 = (190, 222, 246); DAY2 = (236, 244, 250)
def balloon(d, x, y, r, string_to=None):
    if string_to: d.line([(x, y+r*1.15), string_to], fill=(120, 116, 130), width=4)
    d.ellipse([x-r, y-r*1.15, x+r, y+r*1.15], fill=BAL); d.polygon([(x-10, y+r*1.15+12), (x+10, y+r*1.15+12), (x, y+r*1.15-4)], fill=BAL)
    d.ellipse([x-r*0.55, y-r*0.8, x-r*0.2, y-r*0.35], fill=BAL_H)
BL1 = 7*F
def bl_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(DAY1, DAY2, yy/H))
    d.rectangle([0, 820, W, H], fill=PARK); d.text((W/2, 80), '풍선 날아갔어!', font=FBW, fill=TXT, anchor='mm')
    cx, gy = 460, 820; kid(d, cx, gy)
    hand = (cx+120, gy-200); d.line([(cx+60, gy-170), hand], fill=SKIN, width=28)
    kk = ease((t-1.8)/5.0); rise = kk*250
    bx, by = cx+170+60*math.sin(t*1.3)*ease((t-1.8)/2)+300*kk, 360-rise; r = 80*(1-0.55*kk)
    balloon(d, bx, by, r, string_to=hand if t < 1.8 else (bx-10, by+r*1.15+120*(1-0.5*kk)))
    # 아이 시선: 풍선 따라 위로 (눈동자 위로 이동)
    lab(im, '풍선: 둥둥', (800, 700), LT, t, 2.4)
    return im
BL2 = 11*F
def bl_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    h = ease(t/7.0)                 # 0 → 1 (고도)
    top = mix((150, 196, 236), (28, 34, 80), h); bot = mix(DAY2, (90, 120, 190), h)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(top, bot, yy/H))
    # 지나가는 것들: 아파트 → 구름 → 비행기 높이 구름 (아래로 흘러감)
    off = h*2600
    for bx, bw, bh in ((80, 200, 560), (320, 180, 420), (760, 240, 620)):
        yb = H+off*1.0; d.rectangle([bx, yb-bh, bx+bw, yb], fill=(214, 206, 222))
        for r in range(3):
            for c in range(2): d.rectangle([bx+30+c*80, yb-bh+40+r*120, bx+80+c*80, yb-bh+100+r*120], fill=(250, 246, 220))
    for cx, cy, s in ((200, -300, 1.0), (820, -700, 1.3), (380, -1200, 1.1), (760, -1700, 0.9)):
        y0 = cy+off*0.9; col = (255, 255, 255)
        for dx, dy, r in ((0, 0, 70), (70, 10, 90), (150, 0, 70), (75, -40, 70)): d.ellipse([cx+dx*s-r*s, y0+dy*s-r*s, cx+dx*s+r*s, y0+dy*s+r*s], fill=col)
    if h > 0.6:
        d = blend(im, lambda dd: [dd.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255, int(255*(h-0.6)/0.4))) for x, y in ((120, 200), (300, 140), (940, 260), (700, 120), (520, 300), (860, 420), (80, 480))])
    bx, by = 540, 560
    pop = 7.6
    if t < pop:
        r = 70+100*ease((t-0.5)/7.0)
        balloon(d, bx, by, r)
        d.line([(bx, by+r*1.15+12), (bx-20+10*math.sin(t*3), by+r*1.15+200)], fill=(120, 116, 130), width=4)
    else:
        u = t-pop; a = 1 if u < 0.35 else max(0, 1-(u-0.35)/0.6)
        if a > 0:
            pts = []
            for k in range(16):
                ang = k*math.pi/8; rr = 200 if k % 2 == 0 else 90
                pts.append((bx+rr*(1+u)*math.cos(ang), by+rr*(1+u)*math.sin(ang)))
            d = blend(im, lambda dd: dd.polygon(pts, fill=(255, 236, 120, int(255*a))))
        random.seed(3)
        for k in range(9):
            vx = random.uniform(-260, 260); vy0 = random.uniform(-200, 40)
            x = bx+vx*u; y = by+vy0*u+260*u*u
            ang = u*4+k; s = 26
            d.polygon([(x+s*math.cos(ang), y+s*math.sin(ang)), (x+s*math.cos(ang+2.3), y+s*math.sin(ang+2.3)), (x+s*0.6*math.cos(ang+4.2), y+s*0.6*math.sin(ang+4.2))], fill=BAL)
    lab(im, '위로 갈수록: 커져', (540, 960), LM, t, 1.5, pop)
    lab(im, '펑!', (540, 240), LT, t, pop+0.1)
    return im
def bl_sounds(total, sr):
    y = np.zeros(int(sr*total)); base = BL1/F-1.0; t0 = base+7.6
    n = int(sr*0.25); rng = np.random.default_rng(1); pop = rng.normal(0, 0.5, n)*np.exp(-np.arange(n)/(sr*0.03))
    a = int(sr*t0); y[a:a+n] += pop[:len(y)-a]
    return y

if __name__ == '__main__':
    which, out = sys.argv[1], sys.argv[2]
    if which == 'straw':
        build('straw', st_s1, ST1, st_s2, ST2, out, preview=[(st_s1, int(2.5*F), ST1), (st_s1, int(6.5*F), ST1), (st_s2, int(3.5*F), ST2), (st_s2, int(9*F), ST2)])
    elif which == 'mosquito':
        build('mosquito', mq_s1, NM1, mq_s2, NM2, out, sounds=mq_sounds, preview=[(mq_s1, int(2*F), NM1), (mq_s1, int(6.5*F), NM1), (mq_s2, int(4*F), NM2), (mq_s2, int(9*F), NM2)])
    elif which == 'balloon':
        build('balloon', bl_s1, BL1, bl_s2, BL2, out, sounds=bl_sounds, preview=[(bl_s1, int(1*F), BL1), (bl_s1, int(5*F), BL1), (bl_s2, int(5*F), BL2), (bl_s2, int(8*F), BL2)])
