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

# ================= 공통 =================
def bubble(im, text, xy, a=1.0, size=1.0):
    if a <= 0: return
    f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', int(56*size), index=1)
    def dr(dd):
        w = dd.textlength(text, font=f); x, y = xy
        dd.rounded_rectangle([x-w/2-30*size, y-50*size, x+w/2+30*size, y+50*size], radius=int(40*size), fill=(255, 255, 255, int(255*a)))
        dd.text((x, y), text, font=f, fill=TXT+(int(255*a),), anchor='mm')
    blend(im, dr)
def dog(d, cx, gy, s=1.0, tongue=1.0, t=0):
    B = (214, 170, 120); Bd = (180, 136, 90)
    d.ellipse([cx-170*s, gy-190*s, cx+90*s, gy-40*s], fill=B)
    for lx in (-130, -60, 20, 60): d.rounded_rectangle([cx+lx*s, gy-80*s, cx+(lx+34)*s, gy], radius=int(14*s), fill=B)
    d.line([cx-160*s, gy-150*s, cx-230*s, gy-220*s+10*math.sin(t*12)*s], fill=B, width=int(26*s))
    hx, hy = cx+110*s, gy-230*s
    d.ellipse([hx-90*s, hy-80*s, hx+90*s, hy+80*s], fill=B)
    d.ellipse([hx-110*s, hy-60*s, hx-50*s, hy+60*s], fill=Bd); d.ellipse([hx+50*s, hy-60*s, hx+110*s, hy+60*s], fill=Bd)
    d.ellipse([hx-40*s, hy-30*s, hx-20*s, hy-10*s], fill=INK); d.ellipse([hx+20*s, hy-30*s, hx+40*s, hy-10*s], fill=INK)
    d.ellipse([hx-18*s, hy+6*s, hx+18*s, hy+30*s], fill=(80, 70, 80))
    if tongue > 0:
        L = 50+40*tongue*(0.8+0.2*math.sin(t*14))
        d.rounded_rectangle([hx-20*s, hy+36*s, hx+20*s, hy+(36+L)*s], radius=int(20*s), fill=(240, 130, 140))

# ================= 1. 차 뒤로 =================
ROAD = (150, 150, 160); CAR = (240, 200, 110); BUS = (120, 190, 150)
CB1 = 7*F
def cb_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (60, 60, 76)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 200, 990, 800], radius=60, fill=(200, 220, 240))
    bx = 1100 - ease((t-1.2)/5.0)*1500  # 버스가 창밖에서 왼쪽(앞)으로
    d.rectangle([bx-40, 240, bx+1400, 780], fill=BUS)
    for k in range(9): d.rounded_rectangle([bx+20+k*160, 290, bx+140+k*160, 470], radius=16, fill=(210, 236, 246))
    for wx in (bx+200, bx+1100): d.ellipse([wx-70, 700, wx+70, 840], fill=(60, 60, 70))
    d.rectangle([0, 0, W, 200], fill=(60, 60, 76)); d.rectangle([0, 800, W, H], fill=(60, 60, 76))
    d.rounded_rectangle([90, 200, 990, 800], radius=60, outline=(90, 90, 110), width=26)
    d.ellipse([700, 700, 1000, 1000], fill=SKIN); d.ellipse([740, 780, 780, 820], fill=INK)
    d.text((W/2, 110), '우리 차 뒤로 가!', font=FBW, fill=(245, 245, 250), anchor='mm')
    lab(im, '우리 차: 뒤로?!', (360, 880), LT, t, 2.2)
    return im
CB2 = 10*F
def top_car(d, x, y, col, L=240, Wd=120):
    d.rounded_rectangle([x-Wd/2, y-L/2, x+Wd/2, y+L/2], radius=30, fill=col)
    d.rounded_rectangle([x-Wd/2+14, y-L/2+30, x+Wd/2-14, y-L/2+80], radius=10, fill=(210, 236, 246))
def cb_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (190, 214, 170)); d = ImageDraw.Draw(im)
    d.rectangle([260, 0, 820, H], fill=ROAD); d.line([(540, 0), (540, H)], fill=(250, 250, 250), width=8)
    for y in range(0, H, 90): d.line([(540, y), (540, y+50)], fill=ROAD, width=10)
    d.text((W/2, 80), '위에서 보면', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([260, 170, 820, 186], fill=(250, 250, 250))  # 정지선
    top_car(d, 420, 520, CAR)
    by = 620 - ease((t-1.5)/4.5)*700
    top_car(d, 660, by, BUS, L=520, Wd=150)
    wig = 0 if t < 6.5 else 0
    lab(im, '우리 차: 그대로', (190, 520), LT, t, 1.0)
    lab(im, '버스: 앞으로', (890, 420), LM, t, 2.4)
    lab(im, '눈이 속았다!', (540, 960), LG, t, 6.4)
    return im
if __name__ == '__main__' and sys.argv[1] == 'car':
    build('car', cb_s1, CB1, cb_s2, CB2, sys.argv[2], preview=[(cb_s1, int(1*F), CB1), (cb_s1, int(4*F), CB1), (cb_s2, int(3*F), CB2), (cb_s2, int(8*F), CB2)])

# ================= 2. 구름 =================
def cloud(d, cx, cy, s=1.0, col=(255, 255, 255)):
    for dx, dy, r in ((0, 0, 110), (120, -40, 140), (260, 0, 110), (130, 50, 120), (-90, 30, 80), (350, 40, 80)):
        d.ellipse([cx+(dx-r)*s, cy+(dy-r)*s, cx+(dx+r)*s, cy+(dy+r)*s], fill=col)
CL1 = 7*F
def cl_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.rectangle([0, 820, W, H], fill=PARK); d.text((W/2, 80), '구름은 왜 안 떨어져?', font=FBW, fill=TXT, anchor='mm')
    cloud(d, 300+20*t, 330+6*math.sin(t*1.5), 1.1)
    # 누운 아이 (옆모습)
    d.ellipse([140, 760, 260, 880], fill=SKIN); d.rounded_rectangle([250, 780, 520, 860], radius=40, fill=(180, 200, 230))
    d.line([(520, 800), (660, 800)], fill=SKIN, width=28); d.line([(520, 840), (660, 840)], fill=SKIN, width=28)
    d.ellipse([190, 790, 206, 806], fill=INK)
    lab(im, '물이 둥둥?', (820, 600), LT, t, 1.8)
    return im
CL2 = 10*F
def cl_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (150, 180, 214), (214, 226, 240))
    d.text((W/2, 80), '구름 속을 보면', font=FBW, fill=TXT, anchor='mm')
    random.seed(5); drops = [(random.uniform(80, 1000), random.uniform(200, 760), random.uniform(0, 6)) for _ in range(90)]
    merge = ease((t-5.0)/1.5)
    tx, ty = 560, 520
    for k, (x, y, ph) in enumerate(drops):
        x += 10*math.sin(t*2+ph); y += 8*math.cos(t*1.7+ph)
        if k < 14:
            x = x+(tx-x)*merge; y = y+(ty-y)*merge
            if merge >= 1: continue
        d.ellipse([x-7, y-7, x+7, y+7], fill=(120, 170, 230))
    # 위로 부는 바람
    for k in range(5):
        x0 = 150+k*190; ph = (t*0.6+k*0.2) % 1; y0 = 900-ph*500
        pts = [(x0+18*math.sin((y0-yy)/40), yy) for yy in range(int(y0), int(y0)-160, -8)]
        d.line(pts, fill=(250, 250, 255), width=8)
    if merge >= 1:
        u = t-6.5; y = ty+max(0, u-0.4)**2*380
        d.polygon([(tx, y-60), (tx-36, y+10), (tx+36, y+10)], fill=(90, 140, 220)); d.ellipse([tx-38, y-14, tx+38, y+54], fill=(90, 140, 220))
    lab(im, '물방울: 아주 작아', (300, 200), LM, t, 0.6)
    lab(im, '바람: 위로 후~', (760, 900), LT, t, 2.5)
    lab(im, '뭉치면: 비', (820, 560), LG, t, 6.6)
    return im
if __name__ == '__main__' and sys.argv[1] == 'cloud':
    build('cloud', cl_s1, CL1, cl_s2, CL2, sys.argv[2], preview=[(cl_s1, int(3*F), CL1), (cl_s2, int(2*F), CL2), (cl_s2, int(5.8*F), CL2), (cl_s2, int(8*F), CL2)])

# ================= 3. 머리카락 =================
HAIR = (110, 84, 70)
HC1 = 7*F
def hc_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '잘라도 안 아파?', font=FBW, fill=TXT, anchor='mm')
    cx, cy = 540, 520
    cut = t > 3.0
    # 머리카락 (옆머리 길게)
    for k in range(9):
        x = cx-220+k*55; L = 380 if not cut or k < 6 else 260
        d.line([(x, cy-150), (x-10, cy-150+L)], fill=HAIR, width=34)
    d.ellipse([cx-200, cy-230, cx+200, cy+200], fill=SKIN)
    d.chord([cx-215, cy-250, cx+215, cy+60], 180, 360, fill=HAIR)
    smile = 1 if t > 3.3 else 0
    d.ellipse([cx-80, cy-20, cx-50, cy+10], fill=INK); d.ellipse([cx+50, cy-20, cx+80, cy+10], fill=INK)
    d.arc([cx-50, cy+40, cx+50, cy+100], 20, 160, fill=LIP, width=8)
    # 가위
    sx = 930 - ease((t-1.0)/1.8)*140; op = abs(math.sin(t*8)) if t < 3.0 else 0.1
    for sgn in (1, -1):
        d.line([(sx, 700), (sx+140, 700+sgn*op*50)], fill=(170, 176, 190), width=16)
        d.ellipse([sx+140-30, 700+sgn*op*50-26+sgn*30, sx+140+30, 700+sgn*op*50+26+sgn*30], outline=(236, 110, 110), width=10)
    if cut:
        u = t-3.0
        for k in range(3):
            x = cx+110+k*55; y = cy+110+u*300
            if y < 980: d.line([(x-10, y), (x-16, y+110)], fill=HAIR, width=30)
    lab(im, '싹둑: 안 아파', (300, 900), LG, t, 3.5)
    return im
HC2 = 10*F
def hc_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '머리카락 한 올을 보면', font=FBW, fill=TXT, anchor='mm')
    sk = 640
    pull = ease((t-6.2)/0.6)*40*(1 if t < 8.5 else 0)
    d.rectangle([0, sk, W, H], fill=(246, 214, 190))
    # 뿌리: 살아 있어 (분홍 알뿌리 + 감긴 줄)
    rx, ry = 540, sk+170-pull
    glow = 0.6+0.4*abs(math.sin(t*3))
    d.ellipse([rx-60, ry-60, rx+60, ry+60], fill=mix((246, 214, 190), (240, 150, 160), glow))
    for k in range(3):
        yy = ry-40+k*30; d.arc([rx-90, yy-24, rx+90, yy+24], 0, 180, fill=(236, 110, 120), width=6)
    cut_y = 330 if t > 3.2 else 160
    d.line([(rx, ry-50), (rx, cut_y)], fill=HAIR, width=30)
    if 3.2 < t < 5.0:
        u = t-3.2; d.line([(rx+40+u*60, 160+u*260), (rx+40+u*60, 330+u*260)], fill=HAIR, width=30)
    # 가위
    if 2.0 < t < 3.6:
        op = abs(math.sin(t*9)); sy = 330
        for sgn in (1, -1): d.line([(rx+180, sy), (rx+10, sy+sgn*op*40)], fill=(170, 176, 190), width=14)
    # 당기는 손가락
    if 5.6 < t < 8.8:
        d.ellipse([rx-50, cut_y-60-pull, rx-4, cut_y+20-pull], fill=SKIN); d.ellipse([rx+4, cut_y-60-pull, rx+50, cut_y+20-pull], fill=SKIN)
    lab(im, '끝: 안 느껴', (820, 260), LG, t, 3.4)
    lab(im, '뿌리: 살아 있어', (260, 900), LM, t, 1.0)
    if t > 6.4: bubble(im, '아야!', (820, 520), min(1, (t-6.4)/0.3)*(1 if t < 8.8 else max(0, (9.3-t)/0.5)))
    return im
if __name__ == '__main__' and sys.argv[1] == 'hair':
    build('hair', hc_s1, HC1, hc_s2, HC2, sys.argv[2], preview=[(hc_s1, int(2*F), HC1), (hc_s1, int(5*F), HC1), (hc_s2, int(3.6*F), HC2), (hc_s2, int(7*F), HC2)])

# ================= 4. 배꼽 =================
BB1 = 6*F
def bb_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (214, 236, 246)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '배꼽은 왜 있어?', font=FBW, fill=TXT, anchor='mm')
    d.rounded_rectangle([80, 700, 1000, 1000], radius=80, fill=(250, 250, 255))
    for k in range(12): d.ellipse([140+k*70, 660+10*math.sin(k+t*2), 220+k*70, 740+10*math.sin(k+t*2)], fill=(255, 255, 255))
    cx = 540
    d.ellipse([cx-100, 240, cx+100, 440], fill=SKIN)
    d.ellipse([cx-44, 310, cx-24, 330], fill=INK); d.ellipse([cx+24, 310, cx+44, 330], fill=INK); d.ellipse([cx-16, 370, cx+16, 400], fill=LIP)
    d.rounded_rectangle([cx-120, 440, cx+120, 720], radius=80, fill=SKIN)
    d.ellipse([cx-12, 590, cx+12, 614], fill=(220, 170, 150))
    k = ease((t-0.8)/1.0); d.line([(cx+110, 500), (cx+110-80*k, 500+80*k)], fill=SKIN, width=34)
    lab(im, '여기 뭐야?', (820, 560), LT, t, 1.6)
    return im
BB2 = 11*F
def bb_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    born = ease((t-5.0)/1.0)
    d.text((W/2, 80), '엄마 배 속에 있을 때' if t < 5.5 else '태어나면', font=FBW, fill=TXT, anchor='mm')
    # 엄마 배 (큰 원)
    a = 1-born
    if a > 0:
        d = blend(im, lambda dd: dd.ellipse([180, 220, 900, 900], fill=(250, 214, 200, int(255*a))))
    bx, by = 460+born*80, 560
    d.ellipse([bx-130, by-30, bx+130, by+140], fill=SKIN)                       # 몸
    d.line([(bx+90, by+120), (bx+170, by+60)], fill=SKIN, width=40); d.ellipse([bx+150, by+40, bx+195, by+85], fill=SKIN)   # 다리
    d.line([(bx-60, by+40), (bx+10, by-10)], fill=(240, 212, 186), width=30)       # 팔
    d.ellipse([bx-190, by-170, bx-10, by+10], fill=SKIN)                         # 머리
    d.arc([bx-150, by-110, bx-110, by-80], 20, 160, fill=INK, width=6); d.arc([bx-90, by-110, bx-50, by-80], 20, 160, fill=INK, width=6)
    d.ellipse([bx-180, by-60, bx-150, by-36], fill=(250, 200, 200))
    nav = (bx+60, by+60)
    cut = t > 7.2
    end = (780, 560) if born < 1 else (900, 700)
    if not cut:
        d.line([nav, end], fill=(236, 160, 170), width=22)
        if t < 5.0:
            for k in range(5):
                f = ((t*0.8+k/5) % 1); x = end[0]+(nav[0]-end[0])*f; y = end[1]+(nav[1]-end[1])*f
                d.ellipse([x-12, y-12, x+12, y+12], fill=(255, 226, 120))
    else:
        u = t-7.2; stub = max(0, 1-max(0, u-1.2)/0.4)
        if stub > 0: d.line([nav, (nav[0]+40, nav[1]+20)], fill=(236, 160, 170), width=22)
        if u < 1.0: d.line([(nav[0]+70, nav[1]+30), end], fill=(236, 160, 170), width=22)
        if stub <= 0: d.ellipse([nav[0]-12, nav[1]-12, nav[0]+12, nav[1]+12], fill=(220, 170, 150))
    if born > 0.5: bubble(im, '응애!', (320, 300), min(1, (t-5.5)/0.3), 0.8)
    lab(im, '탯줄: 밥 길', (800, 420), LT, t, 1.0, 5.0)
    lab(im, '싹둑: 안 아파', (800, 420), LM, t, 7.2, 9.0)
    lab(im, '톡! 배꼽', (nav[0]+40, nav[1]+170), LG, t, 9.0)
    return im
if __name__ == '__main__' and sys.argv[1] == 'belly':
    build('belly', bb_s1, BB1, bb_s2, BB2, sys.argv[2], preview=[(bb_s1, int(3*F), BB1), (bb_s2, int(3*F), BB2), (bb_s2, int(7.6*F), BB2), (bb_s2, int(10*F), BB2)])

# ================= 5. 새와 전깃줄 =================
POLE = (150, 130, 110); WIRE = (70, 70, 80); BIRD = (170, 130, 100)
def sparrow(d, x, y, s=1.0):
    d.ellipse([x-40*s, y-60*s, x+40*s, y], fill=BIRD); d.ellipse([x+10*s, y-86*s, x+56*s, y-40*s], fill=BIRD)
    d.polygon([(x+56*s, y-66*s), (x+76*s, y-60*s), (x+56*s, y-54*s)], fill=(236, 180, 90)); d.ellipse([x+30*s, y-72*s, x+40*s, y-62*s], fill=INK)
    d.polygon([(x-40*s, y-30*s), (x-80*s, y-10*s), (x-40*s, y-10*s)], fill=(140, 104, 80))
    d.line([(x-10*s, y), (x-10*s, y+8*s)], fill=(200, 140, 90), width=int(5*s)); d.line([(x+14*s, y), (x+14*s, y+8*s)], fill=(200, 140, 90), width=int(5*s))
BW1 = 7*F
def bw_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.rectangle([0, 860, W, H], fill=PARK); d.text((W/2, 80), '새는 왜 안 찌릿해?', font=FBW, fill=TXT, anchor='mm')
    for px in (60, 1020): d.rectangle([px-14, 200, px+14, 860], fill=POLE); d.rectangle([px-80, 230, px+80, 250], fill=POLE)
    for wy in (300, 380): d.line([(60, 250+(wy-250)), (1020, 250+(wy-250))], fill=WIRE, width=6)
    for k, bx in enumerate((300, 420, 560, 720)):
        hop = abs(math.sin(t*3+k))*6 if (k == 2 and t > 2) else 0
        sparrow(d, bx, 300-hop, 0.8)
    kid(d, 420, 860, s=0.75); d.line([(460, 700), (560, 560)], fill=SKIN, width=22)
    lab(im, '전기 흐르는 줄', (780, 520), LT, t, 1.5)
    return im
BW2 = 10*F
def bw_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.text((W/2, 80), '줄을 크게 보면', font=FBW, fill=TXT, anchor='mm')
    wy = 560; d.line([(0, wy), (W, wy)], fill=WIRE, width=30)
    for k in range(14):
        x = ((t*220+k*80) % (W+80))-40
        d.ellipse([x-12, wy-12, x+12, wy+12], fill=(255, 230, 110))
    sparrow(d, 540, wy-14, 2.2)
    lab(im, '전기: 줄 따라 쭉', (260, 720), LT, t, 0.8)
    lab(im, '새: 줄 하나만', (800, 250), LM, t, 2.8)
    if t > 5.5:
        a = min(1, (t-5.5)/0.5); cx, cy = 820, 860
        pass
    lab(im, '사람은: 절대 만지면 안 돼', (540, 880), LG, t, 5.8)
    return im
if __name__ == '__main__' and sys.argv[1] == 'bird':
    build('bird', bw_s1, BW1, bw_s2, BW2, sys.argv[2], preview=[(bw_s1, int(3*F), BW1), (bw_s2, int(2*F), BW2), (bw_s2, int(4*F), BW2), (bw_s2, int(8*F), BW2)])

# ================= 6. 강아지 =================
DG1 = 7*F
def dg_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (200, 226, 246), (240, 246, 250))
    d.rectangle([0, 820, W, H], fill=(214, 206, 190)); d.text((W/2, 80), '강아지는 왜 헥헥해?', font=FBW, fill=TXT, anchor='mm')
    dog(d, 380, 820, 1.2, tongue=1, t=t)
    kid(d, 820, 820, s=0.85)
    if t > 2.5: d.rounded_rectangle([805, 820-290*0.85+40, 835, 820-290*0.85+80], radius=12, fill=(240, 130, 140))
    lab(im, '헥헥!', (540, 300), LT, t, 1.0)
    return im
DG2 = 10*F
def dg_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '더울 때 식히는 법', font=FBW, fill=TXT, anchor='mm')
    d.line([(540, 170), (540, 980)], fill=(214, 210, 224), width=4)
    kid(d, 270, 900, s=1.0)
    for k in range(6):
        ph = (t*0.5+k/6) % 1; x = 200+(k*37) % 140; y = 520+ph*200
        d.ellipse([x-9, y-14, x+9, y+10], fill=(130, 180, 240))
    dog(d, 760, 900, 1.0, tongue=1, t=t)
    hx, hy = 870, 670+40
    for k in range(5):
        ph = (t*0.9+k/5) % 1; x = hx+30*math.sin(k+ph*4); y = hy+60-ph*260
        a = 1-ph
        if a > 0: d = blend(im, lambda dd, x=x, y=y, a=a: dd.arc([x-26, y-18, x+26, y+18], 200, 340, fill=(160, 190, 230, int(255*a)), width=8))
    for px in (650, 720, 790, 830): d.ellipse([px-8, 905, px+8, 921], fill=(130, 180, 240))
    lab(im, '사람: 땀', (270, 300), LM, t, 0.8)
    lab(im, '강아지: 혀로 헥헥', (780, 300), LT, t, 2.6)
    lab(im, '마르면: 시원', (780, 400), LG, t, 5.6)
    return im
if __name__ == '__main__' and sys.argv[1] == 'dog':
    build('dog', dg_s1, DG1, dg_s2, DG2, sys.argv[2], preview=[(dg_s1, int(3*F), DG1), (dg_s2, int(2*F), DG2), (dg_s2, int(5*F), DG2), (dg_s2, int(8*F), DG2)])

# ================= 7. 메아리 =================
MT1 = (120, 160, 130); MT2 = (150, 186, 150); MT3 = (96, 130, 110)
def mountains(d):
    d.polygon([(560, 900), (880, 300), (1200, 900)], fill=MT3)
    d.polygon([(-100, 900), (200, 560), (520, 900)], fill=MT2)
    d.rectangle([0, 860, W, H], fill=MT1)
EC1 = 7*F
def ec_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.text((W/2, 80), '산이 따라 해!', font=FBW, fill=TXT, anchor='mm')
    mountains(d)
    kid(d, 220, 560, s=0.8)
    if 0.8 < t < 2.4: bubble(im, '야호!', (360, 330), min(1, (t-0.8)/0.2)*min(1, (2.4-t)/0.3))
    if 3.6 < t: bubble(im, '야호…', (820, 230), min(1, (t-3.6)/0.3)*0.6, 0.7)
    lab(im, '누가 있어?', (560, 700), LT, t, 4.4)
    return im
EC2 = 10*F
def ec_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.text((W/2, 80), '소리를 눈으로 보면', font=FBW, fill=TXT, anchor='mm')
    mountains(d); kid(d, 220, 560, s=0.8)
    sx, sy = 300, 420; mx, my = 800, 520
    T = 2.6
    u = (t-0.6) % 5.2 if t > 0.6 else -1
    if 0 <= u < T:
        k = u/T; x = sx+(mx-sx)*k; y = sy+(my-sy)*k; r = 34
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 214, 120))
        for g in (1, 2): d.arc([x-r-g*24, y-r-g*24, x+r+g*24, y+r+g*24], -40, 40, fill=(255, 214, 120), width=6)
    elif T <= u < 2*T:
        k = (u-T)/T; x = mx+(sx-mx)*k; y = my+(sy-my)*k; r = 34*(1-0.5*k)
        a = 1-0.5*k
        d = blend(im, lambda dd: dd.ellipse([x-r, y-r, x+r, y+r], fill=(255, 214, 120, int(255*a))))
        if k < 0.2: d.line([(mx-30, my-60), (mx+30, my+60)], fill=(255, 255, 255), width=6)
    lab(im, '야호: 슝~', (430, 290), LT, t, 0.8)
    lab(im, '산에 통!', (830, 400), LM, t, 3.2)
    lab(im, '돌아와서: 작게', (470, 650), LG, t, 5.4)
    return im
if __name__ == '__main__' and sys.argv[1] == 'echo':
    build('echo', ec_s1, EC1, ec_s2, EC2, sys.argv[2], preview=[(ec_s1, int(1.5*F), EC1), (ec_s1, int(5*F), EC1), (ec_s2, int(2*F), EC2), (ec_s2, int(4.5*F), EC2)])

# ================= 김치 =================
TABLE2 = (230, 206, 176); BOWL = (250, 250, 252); KRED = (224, 96, 80); KWHITE = (244, 240, 222); CAB = (214, 230, 170)
def kimchi_bowl(d, cx, cy, s, red):
    d.ellipse([cx-130*s, cy-40*s, cx+130*s, cy+40*s], fill=(236, 236, 240))
    d.chord([cx-130*s, cy-100*s, cx+130*s, cy+100*s], 0, 180, fill=BOWL)
    random.seed(int(cx))
    for k in range(9):
        x = cx+random.uniform(-90, 90)*s; y = cy-10*s+random.uniform(-26, 6)*s
        col = mix(KWHITE, KRED, red) if k % 3 else mix(CAB, (200, 80, 64), red)
        d.rounded_rectangle([x-34*s, y-16*s, x+34*s, y+16*s], radius=int(12*s), fill=col)
    if red > 0.3:
        for k in range(10):
            x = cx+random.uniform(-80, 80)*s; y = cy-14*s+random.uniform(-20, 4)*s
            d.ellipse([x-4*s, y-4*s, x+4*s, y+4*s], fill=(190, 50, 40))
KM1 = 7*F
def km_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (246, 238, 226)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '내 김치는 왜 하얘?', font=FBW, fill=TXT, anchor='mm')
    # 아빠(오른쪽) · 아이(왼쪽) 식탁 뒤에 앉음
    d.ellipse([740, 250, 940, 450], fill=SKIN); d.rounded_rectangle([700, 440, 980, 700], radius=60, fill=(150, 170, 210))
    d.ellipse([790, 320, 812, 342], fill=INK); d.ellipse([868, 320, 890, 342], fill=INK); d.arc([810, 360, 870, 400], 20, 160, fill=LIP, width=8)
    kid(d, 300, 820, s=0.95)
    d.rectangle([0, 640, W, H], fill=TABLE2)
    kimchi_bowl(d, 780, 720, 1.2, 1.0)
    kimchi_bowl(d, 330, 740, 1.0, 0.0)
    look = math.sin(t*2.2)
    lab(im, '왜 달라?', (540, 900), LT, t, 2.0)
    return im
KM2 = 11*F
def km_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (190, 220, 244), (236, 244, 250))
    d.text((W/2, 80), '아주 옛날에는', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 700, W, H], fill=(214, 200, 170))
    # 바다 (오른쪽)
    d.rectangle([640, 560, W, 700], fill=(150, 196, 230))
    # 장독 (왼쪽)
    jx, jy = 300, 720
    d.ellipse([jx-150, jy-230, jx+150, jy+20], fill=(150, 104, 80)); d.rectangle([jx-110, jy-250, jx+110, jy-200], fill=(130, 90, 70))
    red = ease((t-6.8)/1.6)
    kimchi_bowl(d, jx, jy+150, 1.1, red)
    # 배: 오른쪽에서 들어옴 (고추 싣고)
    bx = 1200 - ease((t-1.8)/2.6)*460
    d.polygon([(bx-150, 560), (bx+150, 560), (bx+110, 620), (bx-110, 620)], fill=(170, 120, 90))
    d.line([(bx, 560), (bx, 380)], fill=(140, 100, 80), width=10); d.polygon([(bx+6, 390), (bx+130, 520), (bx+6, 520)], fill=(250, 250, 250))
    for k in range(4):
        px = bx-110+k*50; d.ellipse([px-14, 520, px+14, 560], fill=(214, 60, 50)); d.line([(px, 520), (px+4, 506)], fill=(90, 150, 80), width=5)
    # 고추가 그릇으로 날아감
    if t > 4.8:
        k = ease((t-4.8)/1.8)
        for j in range(3):
            sx, sy = bx-60+j*40, 530; ex, ey = jx-40+j*40, jy+120
            x = sx+(ex-sx)*k; y = sy+(ey-sy)*k-180*math.sin(math.pi*k)
            if k < 1: d.ellipse([x-12, y-22, x+12, y+22], fill=(214, 60, 50))
    lab(im, '옛날 김치: 하양', (300, 400), LM, t, 0.6)
    lab(im, '고추: 배 타고 왔어', (760, 300), LT, t, 3.0)
    lab(im, '빨간 김치!', (300, 980), LG, t, 8.2)
    return im
if __name__ == '__main__' and sys.argv[1] == 'kimchi':
    build('kimchi', km_s1, KM1, km_s2, KM2, sys.argv[2], preview=[(km_s1, int(3*F), KM1), (km_s2, int(2*F), KM2), (km_s2, int(5.5*F), KM2), (km_s2, int(9.5*F), KM2)])

# ================= 0층 =================
FB2 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 64, index=1)
def floor_btn(d, x, y, txt, lit=False):
    d.ellipse([x-46, y-46, x+46, y+46], fill=(255, 236, 150) if lit else (236, 236, 244), outline=(190, 190, 206), width=6)
    d.text((x, y), txt, font=FB2, fill=TXT, anchor='mm')
ZF1 = 7*F
def zf_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (226, 228, 236)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '왜 0층은 없어?', font=FBW, fill=TXT, anchor='mm')
    d.rounded_rectangle([160, 170, 520, 1000], radius=30, fill=(200, 204, 216))
    labs = ['5', '4', '3', '2', '1', 'B1', 'B2']
    k = int(min(6, max(0, (t-0.8)/0.6)))
    for j, s in enumerate(labs):
        floor_btn(d, 340, 240+j*110, s, lit=(6-j) == k)
    # 1과 B1 사이 빈칸 물음표
    if t > 4.6: bubble(im, '0?', (340, 730+0), min(1, (t-4.6)/0.3), 0.7)
    kid(d, 700, 1000, s=0.9)
    fy = 240+(6-k)*110
    # 손 대신 반짝이는 별표로 지금 세는 버튼 표시 (팔을 늘이지 않음)
    d.polygon([(420, fy), (450, fy-14), (450, fy+14)], fill=LT)
    lab(im, '0은 어디?', (800, 300), LT, t, 5.0)
    return im
ZF2 = 10*F
def building(d, x, nums, hi):
    d.rectangle([x-150, 300, x+150, 900], fill=(236, 214, 190)); d.polygon([(x-170, 300), (x, 200), (x+170, 300)], fill=(210, 150, 130))
    for j, s in enumerate(nums):
        y = 820-j*170
        d.rectangle([x-110, y-60, x+110, y+40], fill=(210, 230, 246) if j != hi else (255, 236, 150))
        d.text((x-150-40, y-10), s, font=FB2, fill=TXT, anchor='mm')
ZF_SEL = 2
def zf_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.text((W/2, 80), '같은 건물, 다른 숫자', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=PARK)
    k = ease((t-3.2)/1.4)
    building(d, 320, ['1', '2', '3', '4'], 2)
    if k > 0:
        building(d, 820, ['0', '1', '2', '3'][:], 2)
        if k < 1: d = blend(im, lambda dd: dd.rectangle([600, 190, 1080, 900], fill=(214, 232, 246, int(255*(1-k)))))
    # 창문 속 아이 얼굴 (3번째 칸)
    for bx in (320,) + ((820,) if k > 0.5 else ()):
        y = 820-2*170-10; d.ellipse([bx-36, y-36, bx+36, y+36], fill=SKIN)
    lab(im, '우리: 1층부터', (320, 970), LT, t, 0.8)
    lab(im, '먼 나라: 0층부터', (820, 970), LM, t, 4.2)
    lab(im, '3층 = 2층!', (570, 170), LG, t, 6.5)
    return im
if __name__ == '__main__' and sys.argv[1] == 'zero':
    build('zero', zf_s1, ZF1, zf_s2, ZF2, sys.argv[2], preview=[(zf_s1, int(3*F), ZF1), (zf_s1, int(6*F), ZF1), (zf_s2, int(2*F), ZF2), (zf_s2, int(8*F), ZF2)])

# ================= 안녕 =================
def wave_kid(d, cx, gy, s, t, shirt, hand_phase=0):
    kid(d, cx, gy, s=s, shirt=shirt)
    a = math.sin(t*6+hand_phase)*0.4
    sx, sy = cx+60*s, gy-200*s
    ex, ey = sx+90*s*math.cos(-1.2+a), sy+90*s*math.sin(-1.2+a)
    d.line([(sx, sy), (ex, ey)], fill=SKIN, width=int(26*s)); d.ellipse([ex-20*s, ey-20*s, ex+20*s, ey+20*s], fill=SKIN)
AN1 = 7*F
def an_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (190, 222, 246), (246, 240, 226))
    d.text((W/2, 80), '아침: 만날 때', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=(220, 206, 186))
    d.ellipse([860, 140, 980, 260], fill=SUN)
    k = ease(t/2.5)
    wave_kid(d, 160+k*200, 860, 0.9, t, (180, 200, 230))
    wave_kid(d, 920-k*200, 860, 0.9, t, (240, 190, 170), 1.5)
    if t > 2.6: bubble(im, '안녕!', (540, 400), min(1, (t-2.6)/0.3))
    lab(im, '만날 때: 안녕', (540, 980), LT, t, 3.2)
    return im
AN2 = 10*F
def an_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (250, 200, 160), (246, 226, 214))
    d.text((W/2, 80), '저녁: 헤어질 때', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=(214, 196, 176))
    k = ease((t-2.4)/3.0)
    wave_kid(d, 360-k*200, 860, 0.9, t, (180, 200, 230))
    wave_kid(d, 720+k*200, 860, 0.9, t, (240, 190, 170), 1.5)
    if 0.6 < t: bubble(im, '안녕!', (540, 380), min(1, (t-0.6)/0.3))
    lab(im, '헤어질 때도: 안녕', (540, 980), LM, t, 1.2)
    if t > 5.8:
        a = min(1, (t-5.8)/0.6); s = 1+0.05*math.sin(t*4)
        def heart(dd, cx=540, cy=600, r=70*s):
            c = (240, 130, 150, int(255*a))
            dd.ellipse([cx-r, cy-r*0.6, cx, cy+r*0.4], fill=c); dd.ellipse([cx, cy-r*0.6, cx+r, cy+r*0.4], fill=c)
            dd.polygon([(cx-r*0.96, cy), (cx+r*0.96, cy), (cx, cy+r*1.1)], fill=c)
        d = blend(im, heart)
        lab(im, '안녕 = 편안해', (540, 760), LG, t, 6.2)
    return im
if __name__ == '__main__' and sys.argv[1] == 'annyeong':
    build('annyeong', an_s1, AN1, an_s2, AN2, sys.argv[2], preview=[(an_s1, int(4*F), AN1), (an_s2, int(2*F), AN2), (an_s2, int(5*F), AN2), (an_s2, int(8*F), AN2)])

# ================= 신호등 =================
def ped_light(d, x, y, red_on, green_on):
    d.rectangle([x-12, y+200, x+12, 900], fill=(120, 120, 130))
    d.rounded_rectangle([x-70, y-20, x+70, y+220], radius=20, fill=(60, 60, 70))
    d.ellipse([x-50, y, x+50, y+100], fill=(240, 80, 80) if red_on else (110, 70, 70))
    d.ellipse([x-50, y+110, x+50, y+210], fill=(90, 210, 130) if green_on else (60, 100, 80))
TL1 = 7*F
def tl_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.text((W/2, 80), '빨간색은 왜 멈춰?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=(170, 170, 180))
    for k in range(6): d.rectangle([120+k*150, 940, 200+k*150, 1060], fill=(245, 245, 250))
    ped_light(d, 820, 300, t < 5.2, t >= 5.2)
    kid(d, 300, 900, s=0.8)
    d.ellipse([420, 520, 560, 660], fill=SKIN); d.rounded_rectangle([400, 660, 580, 900], radius=60, fill=(150, 170, 210))
    lab(im, '빨간불: 멈춰!', (820, 240), LT, t, 1.0, 5.2)
    return im
TL2 = 10*F
def tl_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (214, 226, 236), (240, 236, 228))
    d.text((W/2, 80), '아주 옛날 기찻길', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 820, W, H], fill=(200, 186, 160))
    for x in range(0, W, 60): d.rectangle([x, 830, x+30, 850], fill=(140, 110, 90))
    d.line([(0, 820), (W, 820)], fill=(110, 110, 120), width=8); d.line([(0, 860), (W, 860)], fill=(110, 110, 120), width=8)
    # 신호기 (빨간 등)
    sx = 760; d.rectangle([sx-10, 420, sx+10, 820], fill=(110, 110, 120)); d.rounded_rectangle([sx-50, 360, sx+50, 460], radius=20, fill=(60, 60, 70))
    d.ellipse([sx-34, 376, sx+34, 444], fill=(240, 80, 80))
    # 기차: 왼쪽에서 와서 신호 앞에서 멈춤
    k = ease(t/3.2); tx = -300+k*820
    d.rounded_rectangle([tx-220, 640, tx+120, 800], radius=24, fill=(120, 160, 200)); d.rectangle([tx+30, 560, tx+120, 700], fill=(90, 120, 170))
    d.rectangle([tx-160, 590, tx-120, 640], fill=(80, 80, 90))
    for wx in (tx-170, tx-60, tx+60): d.ellipse([wx-34, 770, wx+34, 838], fill=(60, 60, 70))
    if t < 3.4:
        for j in range(3):
            age = (t*1.5+j/3) % 1; d.ellipse([tx-160-age*60-30, 560-age*150-30, tx-160-age*60+30, 560-age*150+30], fill=(236, 236, 240))
    lab(im, '기차: 빨강 멈춤', (sx, 300), LT, t, 1.6)
    # 5.5초~: 신호등으로 옮겨감
    if t > 5.6:
        u = ease((t-5.6)/1.6)
        cx, cy = sx+(300-sx)*u, 410+(640-410)*u
        d = blend(im, lambda dd: dd.rounded_rectangle([200, 520, 400, 900], radius=30, fill=(240, 240, 246, int(230*u))))
        ped_light(d, 300, 560, True, False)
        lab(im, '길에서도: 멈춤', (300, 460), LM, t, 6.6)
    return im
if __name__ == '__main__' and sys.argv[1] == 'traffic':
    build('traffic', tl_s1, TL1, tl_s2, TL2, sys.argv[2], preview=[(tl_s1, int(3*F), TL1), (tl_s1, int(6*F), TL1), (tl_s2, int(3*F), TL2), (tl_s2, int(8.5*F), TL2)])

# ================= 엘리베이터 거울 =================
EL1 = 7*F
def el_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (214, 216, 224)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '왜 거울이 있어?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([160, 180, 920, 1000], fill=(196, 198, 210))
    d.rectangle([260, 240, 820, 860], fill=(226, 238, 246), outline=(170, 174, 190), width=10)  # 거울
    # 거울 속 아이 (얼굴 표정 바뀜)
    face = int(t*1.5) % 3
    cx, cy = 540, 560
    d.ellipse([cx-120, cy-120, cx+120, cy+120], fill=SKIN)
    d.ellipse([cx-60, cy-40, cx-30, cy-10], fill=INK); d.ellipse([cx+30, cy-40, cx+60, cy-10], fill=INK)
    if face == 0: d.ellipse([cx-30, cy+30, cx+30, cy+80], fill=LIP)
    elif face == 1: d.rounded_rectangle([cx-20, cy+40, cx+20, cy+110], radius=18, fill=(240, 130, 140))
    else: d.arc([cx-50, cy+20, cx+50, cy+80], 20, 160, fill=LIP, width=10)
    d.rounded_rectangle([cx-110, cy+120, cx+110, cy+300], radius=60, fill=(180, 200, 230))
    d.line([(160, 180), (160, 1000)], fill=(150, 150, 170), width=12)
    lab(im, '메롱~', (800, 420), LT, t, 1.0, 4.0)
    lab(im, '거울은 왜?', (540, 960), LT, t, 4.4)
    return im
EL2 = 10*F
def wheelchair(d, x, y, s=1.0):
    d.ellipse([x-80*s, y-10*s, x+80*s, y+150*s], outline=(90, 90, 110), width=int(14*s))
    d.rounded_rectangle([x-60*s, y-90*s, x+60*s, y+40*s], radius=int(20*s), fill=(150, 170, 210))
    d.ellipse([x-45*s, y-190*s, x+45*s, y-100*s], fill=SKIN)
def el_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (236, 234, 240)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '휠체어는 뒤로 나와요', font=FBW, fill=TXT, anchor='mm')
    # 옆에서 본 엘리베이터: 왼쪽 문, 오른쪽 벽에 거울
    d.rectangle([180, 260, 900, 900], fill=(214, 216, 226), outline=(160, 164, 180), width=10)
    op = ease((t-3.0)/1.0)
    d.rectangle([180, 280, 200+int(-0*op), 890], fill=(170, 174, 190))
    door_w = 90*(1-op); d.rectangle([140, 280, 140+door_w+40, 890], fill=(160, 164, 180))
    d.rectangle([860, 360, 890, 820], fill=(206, 230, 246)); d.line([(860, 360), (860, 820)], fill=(150, 170, 200), width=6)
    # 휠체어 (오른쪽 거울 보고 있음), 문 열린 뒤 뒤로 나감
    back = ease((t-6.2)/2.5)
    wx = 620-back*520
    wheelchair(d, wx, 700, 1.1)
    if 1.2 < t < 6.4:
        k = ease((t-1.2)/1.2)
        dashed(d, (wx+40, 520), (860, 560), (120, 150, 210), w=8, k=k)
        if t > 3.6: dashed(d, (860, 560), (180, 600), (120, 150, 210), w=8, k=ease((t-3.6)/1.0))
    lab(im, '못 돌아', (wx, 440), LT, t, 0.6, 3.4)
    lab(im, '거울로 뒤 보기', (620, 200), LM, t, 2.0)
    lab(im, '문 열렸다!', (330, 960), LG, t, 4.8)
    return im
if __name__ == '__main__' and sys.argv[1] == 'mirror':
    build('mirror', el_s1, EL1, el_s2, EL2, sys.argv[2], preview=[(el_s1, int(2*F), EL1), (el_s1, int(5*F), EL1), (el_s2, int(4.5*F), EL2), (el_s2, int(8*F), EL2)])

# ================= 촛불 =================
CAKE = (250, 236, 226); CREAM = (255, 250, 246); BERRY = (230, 90, 110)
def cake(d, cx, cy, n, lit, t):
    d.rounded_rectangle([cx-260, cy-80, cx+260, cy+160], radius=40, fill=CAKE)
    d.rounded_rectangle([cx-260, cy-100, cx+260, cy-40], radius=30, fill=CREAM)
    for k in range(6): d.ellipse([cx-230+k*92, cy-60, cx-190+k*92, cy-20], fill=BERRY)
    for k in range(n):
        x = cx-180+k*(360/(n-1) if n > 1 else 0)
        d.rectangle([x-10, cy-230, x+10, cy-100], fill=[(140, 180, 240), (240, 170, 190), (160, 220, 170), (250, 220, 120), (200, 170, 240)][k % 5])
        if lit[k] > 0:
            fl = lit[k]*(1+0.1*math.sin(t*14+k))
            d.ellipse([x-16*fl, cy-236-54*fl, x+16*fl, cy-236], fill=(255, 200, 90)); d.ellipse([x-8*fl, cy-236-34*fl, x+8*fl, cy-236], fill=(255, 240, 180))
CD1 = 7*F
def cd_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (250, 238, 226)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '생일엔 왜 후 불어?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 820, W, H], fill=(214, 190, 160))
    blow = ease((t-3.0)/0.8)
    lit = [max(0, 1-ease((t-3.0-k*0.12)/0.3)) for k in range(5)]
    cake(d, 540, 700, 5, lit, t)
    # 아이 얼굴 (볼 빵빵)
    hx, hy = 540, 300
    d.ellipse([hx-110, hy-110, hx+110, hy+110], fill=SKIN)
    d.ellipse([hx-50, hy-30, hx-24, hy-4], fill=INK); d.ellipse([hx+24, hy-30, hx+50, hy-4], fill=INK)
    if 2.4 < t < 4.0:
        d.ellipse([hx-90, hy+10, hx-40, hy+60], fill=(250, 190, 190)); d.ellipse([hx+40, hy+10, hx+90, hy+60], fill=(250, 190, 190))
        d.ellipse([hx-16, hy+50, hx+16, hy+80], fill=LIP)
        for k in range(4):
            x = hx+(k-1.5)*50; y = hy+140+blow*80
            d.arc([x-30, y-12, x+30, y+12], 200, 340, fill=(200, 210, 230), width=6)
    else:
        d.arc([hx-50, hy+30, hx+50, hy+90], 20, 160, fill=LIP, width=10)
    # 연기
    if t > 3.4:
        for k in range(5):
            x0 = 540-180+k*90; age = t-3.4-k*0.12
            if age > 0:
                pts = [(x0+18*math.sin(yy/30+k), 470-yy) for yy in range(0, int(min(260, age*180)), 6)]
                if len(pts) > 1: d.line(pts, fill=(200, 200, 210), width=6)
    lab(im, '후~!', (860, 520), LT, t, 3.0)
    return im
CD2 = 10*F
def cd_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (60, 70, 120), (140, 130, 190))
    d.text((W/2, 80), '초 하나 = 한 살', font=FBW, fill=(245, 245, 250), anchor='mm')
    # 초가 하나씩 켜짐 (1~5)
    k = int(min(5, max(0, (t-0.4)/0.7)))
    lit = [1 if j < k else 0 for j in range(5)]
    cake(d, 540, 800, 5, lit, t)
    for j in range(k):
        x = 540-180+j*90; d.text((x, 1010), str(j+1), font=FB2, fill=(255, 240, 180), anchor='mm')
    # 소원 연기가 하늘로 → 별
    if t > 5.2:
        u = t-5.2
        for j in range(5):
            x = 540-180+j*90; y = 560-u*120
            if y > 200: d.ellipse([x-14, y-14, x+14, y+14], fill=(230, 230, 245))
        if u > 2.8:
            a = min(1, (u-2.8)/0.6); r = 40
            def star(dd):
                pts = []
                for q in range(10):
                    ang = -math.pi/2+q*math.pi/5; rr = r if q % 2 == 0 else r*0.45
                    pts.append((540+rr*math.cos(ang), 220+rr*math.sin(ang)))
                dd.polygon(pts, fill=(255, 236, 140, int(255*a)))
            d = blend(im, star)
    lab(im, '연기: 소원 슝~', (540, 360), LT, t, 5.6)
    return im
if __name__ == '__main__' and sys.argv[1] == 'candles':
    build('candles', cd_s1, CD1, cd_s2, CD2, sys.argv[2], preview=[(cd_s1, int(1.5*F), CD1), (cd_s1, int(4.5*F), CD1), (cd_s2, int(3.5*F), CD2), (cd_s2, int(9*F), CD2)])
