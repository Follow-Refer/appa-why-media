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

# ================= 번개 =================
RN1 = (40, 44, 70); RN2 = (70, 72, 100); WALL = (236, 226, 214); FRAME = (200, 180, 160); CLOUD = (120, 122, 150); CLOUD_L = (150, 152, 178)
BOLT = (255, 244, 170)
def bolt(d, x0, y0, x1, y1, seed=1, w=18, col=BOLT):
    random.seed(seed); pts = [(x0, y0)]; n = 7
    for k in range(1, n):
        f = k/n; pts.append((x0+(x1-x0)*f+random.uniform(-60, 60), y0+(y1-y0)*f))
    pts.append((x1, y1)); d.line(pts, fill=col, width=w, joint='curve')
LN1 = 7*F
def ln_s1(i, n):
    t = i/F
    flash = max(0, 1-abs(t-2.2)/0.18) + max(0, 1-abs(t-2.55)/0.12)*0.7
    im = Image.new('RGB', (W, H), mix(WALL, (255, 255, 255), min(1, flash*0.6))); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '밖에 번쩍했어!', font=FBW, fill=TXT, anchor='mm')
    # 창문
    wx0, wy0, wx1, wy1 = 560, 200, 980, 620
    sky = mix(RN1, (230, 230, 255), min(1, flash))
    d.rectangle([wx0, wy0, wx1, wy1], fill=sky)
    for k in range(14):
        x = wx0+20+(k*37+int(t*300)) % (wx1-wx0-40); y = wy0+(k*53+int(t*500)) % (wy1-wy0)
        d.line([x, y, x-8, y+26], fill=mix(sky, (200, 210, 240), 0.6), width=4)
    if flash > 0.2: bolt(d, 820, wy0, 700, wy1-60, seed=4, w=14)
    d.rectangle([wx0, wy0, wx1, wy1], outline=FRAME, width=20); d.line([(wx0+wx1)/2, wy0, (wx0+wx1)/2, wy1], fill=FRAME, width=14)
    # 이불 속 아이: 번쩍 뒤 이불 속으로 쏙
    hide = ease((t-2.4)/0.5)
    d.rounded_rectangle([60, 700, 1020, 1000], radius=60, fill=(200, 190, 220))
    hx, hy = 300, 640+int(120*hide)
    d.ellipse([hx-90, hy-90, hx+90, hy+90], fill=SKIN)
    if hide < 0.5:
        d.ellipse([hx-40, hy-20, hx-20, hy], fill=INK); d.ellipse([hx+20, hy-20, hx+40, hy], fill=INK)
        d.ellipse([hx-14, hy+24, hx+14, hy+50], fill=LIP)
    else:
        d.ellipse([hx-44, hy-28, hx-16, hy], fill=INK); d.ellipse([hx+16, hy-28, hx+44, hy], fill=INK)
    d.rounded_rectangle([60, 690, 1020, 1000], radius=60, fill=BLANKET)
    lab(im, '번쩍!', (770, 170), LT, t, 2.25)
    return im
LN2 = 10*F
def ln_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(RN1, RN2, yy/H))
    d.text((W/2, 80), '구름 속을 보면', font=FBW, fill=(240, 236, 250), anchor='mm')
    d.rectangle([0, 940, W, H], fill=(70, 80, 90))
    for x in range(40, 1080, 180): d.rectangle([x, 880, x+120, 940], fill=(90, 100, 110))
    # 큰 구름
    for cx, cy, r in ((300, 380, 170), (520, 320, 210), (760, 380, 180), (420, 500, 170), (660, 500, 180)):
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=CLOUD)
    d.ellipse([360, 200, 520, 330], fill=CLOUD_L)
    # 얼음 알갱이: 작은 것은 위로, 큰 것은 아래로, 부딪히면 반짝
    charge = min(1, max(0, (t-1.0)/5.0))
    for k in range(10):
        ph = (t*0.45+k*0.1) % 1
        xs = 260+k*52
        if k % 2 == 0:  # 작은 얼음 위로
            y = 580-ph*300; r = 12
            d.ellipse([xs-r, y-r, xs+r, y+r], fill=(230, 240, 255))
        else:           # 큰 얼음 아래로
            y = 280+ph*300; r = 22
            d.ellipse([xs-r, y-r, xs+r, y+r], fill=(200, 214, 240))
        if abs(ph-0.5) < 0.06 and t < 6.8:
            sx = xs-26; sy = 430
            d.line([sx-26, sy, sx+26, sy], fill=YEL, width=9); d.line([sx, sy-26, sx, sy+26], fill=YEL, width=9)
    # 전기가 모여 구름이 번쩍번쩍 빛남
    if charge > 0 and t < 7.0:
        d = blend(im, lambda dd: dd.ellipse([260, 250, 820, 620], fill=(255, 236, 120, int(110*charge*(0.5+0.5*abs(math.sin(t*7)))))))
    # 7초: 번개가 땅으로
    if t >= 7.0:
        u = t-7.0; a = max(0, 1-max(0, u-0.5)/0.8)
        if a > 0:
            d = blend(im, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 230, int(120*a*(1 if u < 0.15 else 0.4)))))
            bolt(d, 560, 560, 600, 880, seed=7, w=int(26*a)+2, col=mix(RN1, BOLT, a))
    lab(im, '얼음: 콩콩', (190, 220), LM, t, 0.6)
    lab(im, '찌릿찌릿 모여', (840, 700), LT, t, 3.2, 7.0)
    lab(im, '번쩍!', (850, 720), LT, t, 6.9)
    return im
def ln_sounds(total, sr):
    y = np.zeros(int(sr*total)); rng = np.random.default_rng(2)
    y += rng.normal(0, 0.015, len(y))       # 빗소리
    for t0, amp in ((2.3, 0.35), (LN1/F-1.0+7.1, 0.5)):
        n = int(sr*1.6); a = int(sr*t0)
        if a >= len(y): continue
        tt = np.arange(n)/sr
        rum = rng.normal(0, 1, n); rum = np.convolve(rum, np.ones(300)/300, mode='same')*8
        y[a:a+n] += (amp*rum*np.exp(-tt/0.6))[:len(y)-a]
    return y
if __name__ == '__main__' and sys.argv[1] == 'lightning':
    build('lightning', ln_s1, LN1, ln_s2, LN2, sys.argv[2], sounds=ln_sounds, preview=[(ln_s1, int(1*F), LN1), (ln_s1, int(2.2*F), LN1), (ln_s2, int(4.5*F), LN2), (ln_s2, int(7.1*F), LN2)])

# ================= 비행기구름 =================
SK1 = (120, 176, 232); SK2 = (206, 230, 248); PLANE = (245, 245, 250); PLANE_D = (190, 196, 214)
def plane(d, x, y, s=1.0):
    d.rounded_rectangle([x-120*s, y-18*s, x+120*s, y+18*s], radius=int(18*s), fill=PLANE)
    d.polygon([(x-10*s, y), (x-70*s, y-90*s), (x-40*s, y-90*s), (x+40*s, y)], fill=PLANE_D)
    d.polygon([(x-10*s, y), (x-70*s, y+70*s), (x-40*s, y+70*s), (x+40*s, y)], fill=PLANE_D)
    d.polygon([(x-110*s, y), (x-140*s, y-50*s), (x-118*s, y-50*s), (x-90*s, y)], fill=PLANE_D)
    for k in range(4): d.ellipse([x+(20+k*22)*s, y-8*s, x+(32+k*22)*s, y+4*s], fill=(150, 170, 210))
def sky_bg(d, top=SK1, bot=SK2):
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(top, bot, yy/H))
CT_1 = 7*F
def cn_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.rectangle([0, 860, W, H], fill=PARK); d.text((W/2, 80), '하늘에 누가 줄 그었어!', font=FBW, fill=TXT, anchor='mm')
    px = -100+ease(t/6.5)*1250; py = 330-0.08*px
    # 줄: 비행기 뒤쪽, 조금 떨어진 곳부터 하얗게
    x0 = -100
    if px-160 > x0:
        d = blend(im, lambda dd: dd.line([(x0, 330-0.08*x0), (px-170, py+8)], fill=(255, 255, 255, 235), width=26))
    plane(d, px, py, 0.55)
    kid(d, 330, 860, s=0.85)
    hx, hy = 330+60, 860-290*0.85+80; d.line([(hx, hy), (hx+130, hy-150)], fill=SKIN, width=24)
    lab(im, '하얀 줄!', (760, 560), LT, t, 2.5)
    return im
CT_2 = 10*F
def cn_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (70, 120, 200), (150, 196, 240))
    d.text((W/2, 80), '비행기 엔진 뒤를 보면', font=FBW, fill=(245, 245, 250), anchor='mm')
    # 큰 엔진 (오른쪽), 입김이 왼쪽으로
    ex, ey = 860, 470
    d.rounded_rectangle([ex-150, ey-80, ex+150, ey+80], radius=70, fill=(220, 224, 236)); d.ellipse([ex-170, ey-80, ex-110, ey+80], fill=(120, 124, 140))
    d.polygon([(ex-60, ey-80), (ex+40, ey-230), (ex+120, ey-230), (ex+80, ey-80)], fill=PLANE_D)
    # 입김 알갱이: 나오면 주황(따뜻) → 왼쪽으로 가며 흰 얼음 반짝이
    parts = []
    for k in range(60):
        born = k*0.13
        if t > born:
            age = t-born; x = ex-180-age*190; y = ey+math.sin(k*1.7)*30*(1+age*0.4)
            if x > -40:
                cool = min(1, age/1.6); parts.append((x, y, cool, k))
    for x, y, cool, k in parts:
        col = mix((255, 196, 150), (255, 255, 255), cool); r = 16+6*cool
        d.ellipse([x-r, y-r, x+r, y+r], fill=col)
        if cool > 0.95 and k % 3 == 0:
            d.line([x-r-6, y, x+r+6, y], fill=(210, 230, 255), width=3); d.line([x, y-r-6, x, y+r+6], fill=(210, 230, 255), width=3)
    # 온도계: 아주 추워
    tx, ty = 150, 760
    d.rounded_rectangle([tx-18, ty-200, tx+18, ty+20], radius=18, fill=(245, 245, 250)); d.ellipse([tx-34, ty, tx+34, ty+68], fill=(120, 170, 240))
    d.rectangle([tx-8, ty-40, tx+8, ty+20], fill=(120, 170, 240))
    lab(im, '엔진 입김: 후~', (ex-120, ey+170), LT, t, 0.6)
    lab(im, '너무 추워: 꽁꽁', (330, 800), LM, t, 3.0)
    lab(im, '하얀 줄 = 구름', (430, 300), LG, t, 6.0)
    return im
if __name__ == '__main__' and sys.argv[1] == 'contrail':
    build('contrail', cn_s1, CT_1, cn_s2, CT_2, sys.argv[2], preview=[(cn_s1, int(2*F), CT_1), (cn_s1, int(6*F), CT_1), (cn_s2, int(3*F), CT_2), (cn_s2, int(8*F), CT_2)])

# ================= 하늘 파랑 =================
SLIDE = (236, 150, 120)
COLS = [(240, 110, 110), (250, 180, 90), (250, 226, 110), (130, 200, 130), (110, 160, 240)]
BS_1 = 6*F
def bs_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (110, 170, 236), (200, 226, 248))
    d.rectangle([0, 880, W, H], fill=PARK); d.text((W/2, 80), '하늘은 왜 파래?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([180, 640, 440, 670], fill=SLIDE); d.line([(200, 670), (200, 880)], fill=(160, 160, 180), width=16); d.line([(420, 670), (420, 880)], fill=(160, 160, 180), width=16)
    d.polygon([(440, 640), (440, 670), (820, 880), (760, 880)], fill=SLIDE)
    kid(d, 310, 640, s=0.8)
    # 크레파스 든 손? → 물음표 붓: 하늘에 붓칠하는 손이 없음을 보여 주는 대신 라벨
    lab(im, '누가 색칠했어?', (720, 360), LT, t, 1.5)
    return im
BS_2 = 11*F
def bs_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    fill = ease((t-3.5)/4.0)
    sky_bg(d, mix((60, 64, 90), (110, 170, 236), fill), mix((90, 94, 120), (200, 226, 248), fill))
    d.text((W/2, 80), '햇빛 속을 보면', font=FBW, fill=(245, 245, 250), anchor='mm')
    d.rectangle([0, 900, W, H], fill=PARK)
    sx, sy = 120, 220; d.ellipse([sx-80, sy-80, sx+80, sy+80], fill=SUN)
    # 공기 알갱이
    random.seed(11); air = [(random.uniform(250, 1050), random.uniform(250, 860)) for _ in range(40)]
    for ax, ay in air: d.ellipse([ax-6, ay-6, ax+6, ay+6], fill=(210, 214, 230))
    # 색 공 줄기: 해에서 오른쪽 아래로 흘러감. 파랑은 공기 알갱이 만나면 사방으로 튐
    for k in range(120):
        born = k*0.075; age = t-born
        if age <= 0: continue
        c = k % 5; col = COLS[c]
        x = sx+60+age*260; y = sy+40+age*190
        if c == 4 and age > 1.3:  # 파랑: 튕겨서 사방으로
            random.seed(k); ang = random.uniform(0, 2*math.pi); u = min(age-1.3, random.uniform(1.2, 2.6)); hop = 1.3*random.uniform(0.3, 1.4)
            bx = sx+60+hop*260+math.cos(ang)*u*260+8*math.sin(t*3+k); by = sy+40+hop*190+math.sin(ang)*u*260+8*math.cos(t*3+k)
            if 0 < bx < W and 150 < by < 900: d.ellipse([bx-13, by-13, bx+13, by+13], fill=col)
        elif y < 900 and x < W:
            d.ellipse([x-13, y-13, x+13, y+13], fill=col)
    kid(d, 900, 900, s=0.6)
    lab(im, '햇빛: 여러 색', (400, 200), LT, t, 0.6)
    lab(im, '파랑만 통통 튀어', (620, 470), LM, t, 2.4)
    lab(im, '하늘 가득 파랑', (560, 820), LG, t, 6.5)
    return im
if __name__ == '__main__' and sys.argv[1] == 'bluesky':
    build('bluesky', bs_s1, BS_1, bs_s2, BS_2, sys.argv[2], preview=[(bs_s1, int(3*F), BS_1), (bs_s2, int(2*F), BS_2), (bs_s2, int(5*F), BS_2), (bs_s2, int(9*F), BS_2)])
