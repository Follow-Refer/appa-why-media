"""달 영상 문법: 문장 없음, 라벨 4개까지, 원리는 움직임. 14~20초."""
from vid import *
from common import pill
FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 54, index=1)
FH = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 200, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)

def fade_pill(im, text, xy, col, alpha):
    if alpha <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FS); x, y = xy; a = int(255*alpha)
    d.rounded_rectangle([x-w/2-22, y-30, x+w/2+22, y+30], radius=30, fill=(255, 255, 255, a), outline=col+(a,), width=4)
    d.text((x, y), text, font=FS, fill=TXT+(a,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))

def kid(d, cx, gy, s=1.0, lift=0, shirt=(180, 200, 230)):
    hy = gy-290*s-lift
    d.rounded_rectangle([cx-70*s, hy+90*s, cx+70*s, hy+240*s], radius=int(45*s), fill=shirt)
    d.line([cx-30*s, hy+240*s, cx-30*s, gy-lift], fill=SKIN, width=int(30*s)); d.line([cx+30*s, hy+240*s, cx+30*s, gy-lift], fill=SKIN, width=int(30*s))
    d.ellipse([cx-80*s, hy-80*s, cx+80*s, hy+80*s], fill=SKIN)
    d.ellipse([cx-34*s, hy-16*s, cx-20*s, hy-2*s], fill=INK); d.ellipse([cx+20*s, hy-16*s, cx+34*s, hy-2*s], fill=INK)
    d.arc([cx-24*s, hy+14*s, cx+24*s, hy+46*s], 20, 160, fill=LIP, width=int(5*s))

# ================= 그림자 =================
SKY1 = (250, 214, 170); SKY2 = (232, 224, 240); GROUND = (214, 198, 170); SUN = (255, 214, 120); RAY = (255, 232, 160); SHADOW = (150, 140, 160)
def sh_bg(d, title_txt):
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(SKY2, SKY1, y/H))
    d.rectangle([0, 760, W, H], fill=GROUND)
    d.text((W/2, 80), title_txt, font=FBW, fill=TXT, anchor='mm')
def sh_shadow(d, cx, gy, dirx=-1, L=330):
    x1 = cx+dirx*L
    d.polygon([(cx-45, gy), (cx+45, gy), (x1+dirx*10, gy+62), (x1-dirx*40, gy+74)], fill=SHADOW)
    d.ellipse([x1-75, gy+22, x1+35, gy+96], fill=SHADOW)
SH1 = 7*F
def sh_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    sh_bg(d, '얘가 자꾸 나 따라와!'); d.ellipse([860, 300, 1000, 440], fill=SUN)
    cx = 640 - int(200*(0.5-0.5*math.cos(math.pi*min(1, t/5)))); hop = abs(math.sin(t*4))*34 if t < 5.5 else 0
    sh_shadow(d, cx, 760); kid(d, cx, 760, lift=hop)
    fade_pill(im, '그림자: 같이 뛰어', (cx-330, 700), LT, min(1, max(0, (t-1.5)/0.6)))
    return im
SH2 = 10*F
def sh_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    sh_bg(d, '옆에서 보면'); sx, sy = 930, 330; d.ellipse([sx-70, sy-70, sx+70, sy+70], fill=SUN)
    gy = 760
    # 아이: 4~8초에 왼쪽으로 걸어감
    cx = 620 - int(240*(0.5-0.5*math.cos(math.pi*min(1, max(0, (t-4)/4)))))
    # 빛줄기: 해에서 여러 갈래, 아이한테 막힘 (아이 몸통 범위에서 멈춤), 나머지는 바닥까지
    k = min(1, t/2.0)
    for ey in (-260, -200, -140, -80, -20):
        # 목표: 아이 앞면(오른쪽) x=cx+70 의 높이 gy+ey... 광선은 해에서 직선으로
        tx, ty = cx+72, gy+ey
        x = sx+(tx-sx)*k; y = sy+(ty-sy)*k
        d.line([sx, sy, x, y], fill=RAY, width=10)
    for ty in (gy, gy):  # 아이 위로 지나가는 빛 두 줄: 바닥 먼 곳까지
        pass
    for tx in (cx-420, cx-560):
        x = sx+(tx-sx)*k; y = sy+(gy-sy)*k
        d.line([sx, sy, x, y], fill=RAY, width=10)
    # 그림자 (빛이 닿는 동안 서서히)
    a = min(1, max(0, (t-1.6)/1.2))
    if a > 0:
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
        x1 = cx-330
        dd.polygon([(cx-45, gy), (cx+45, gy), (x1-10, gy+62), (x1+40, gy+74)], fill=SHADOW+(int(255*a),))
        dd.ellipse([x1-75, gy+22, x1+35, gy+96], fill=SHADOW+(int(255*a),))
        im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')); d = ImageDraw.Draw(im)
    kid(d, cx, gy)
    fade_pill(im, '빛: 쭉 똑바로', (770, 250), LM, min(1, max(0, (t-0.8)/0.6)))
    fade_pill(im, '몸에 막혀', (cx+230, 620), LT, min(1, max(0, (t-2.2)/0.6)))
    fade_pill(im, '발에 딱 붙어', (cx-40, 700), LG, min(1, max(0, (t-4.2)/0.6)))
    return im

# ================= 고양이 =================
N1 = (70, 72, 110); N2 = (120, 110, 150); NG = (92, 92, 118); LAMP = (255, 226, 150); CAT = (120, 112, 128); EYE = (60, 56, 70); GLOW = (200, 240, 150)
def ct_bg(d, title_txt, dark=0.0):
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(mix(N1, N2, y/H), (40, 40, 70), dark))
    d.rectangle([0, 780, W, H], fill=mix(NG, (50, 50, 70), dark))
    d.text((W/2, 80), title_txt, font=FBW, fill=(240, 236, 250), anchor='mm')
def lamp(d, x, y, on=1.0):
    d.rectangle([x-8, y, x+8, 780], fill=(150, 150, 170))
    d.rounded_rectangle([x-60, y-40, x+60, y+10], radius=20, fill=(170, 170, 190))
    d.ellipse([x-38, y-30, x+38, y+2], fill=mix((120, 120, 130), LAMP, on))
def cat(d, cx, gy, s=1.0, glow=0.0):
    d.ellipse([cx-150*s, gy-200*s, cx+90*s, gy], fill=CAT)
    d.ellipse([cx+20*s, gy-300*s, cx+200*s, gy-140*s], fill=CAT)
    d.polygon([(cx+50*s, gy-280*s), (cx+70*s, gy-350*s), (cx+110*s, gy-290*s)], fill=CAT)
    d.polygon([(cx+130*s, gy-290*s), (cx+170*s, gy-350*s), (cx+180*s, gy-275*s)], fill=CAT)
    d.line([cx-140*s, gy-40*s, cx-230*s, gy-130*s], fill=(98, 90, 108), width=int(24*s))
    for ex in (cx+85*s, cx+150*s):
        ey = gy-225*s; col = mix(EYE, GLOW, glow)
        if glow > 0.3:
            r = int(34*s*glow); d.ellipse([ex-r, ey-r, ex+r, ey+r], fill=mix(N1, GLOW, glow*0.35))
        d.ellipse([ex-22*s, ey-16*s, ex+22*s, ey+16*s], fill=col)
    d.ellipse([cx+185*s, gy-200*s, cx+205*s, gy-186*s], fill=(230, 170, 170))
CT1 = 7*F
def ct_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    on = ease((t-2.5)/0.6)
    ct_bg(d, '고양이 눈에 불 켜졌어!', dark=1-on)
    lamp(d, 860, 200, on)
    if on > 0:
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
        dd.polygon([(860, 210), (430, 780), (1080, 780)], fill=LAMP+(int(70*on),))
        im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')); d = ImageDraw.Draw(im)
    cat(d, 560, 780, glow=on*(0.7+0.3*abs(math.sin(t*3))))
    fade_pill(im, '가로등 꺼짐: 안 빛나', (300, 300), LM, min(1, max(0, (t-0.8)/0.5))*(1 if t < 2.4 else max(0, (2.9-t)/0.5)))
    fade_pill(im, '가로등 켜짐: 반짝', (300, 300), LT, min(1, max(0, (t-3.2)/0.5)))
    return im
CT2 = 10*F
def ct_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    ct_bg(d, '눈을 크게 보면')
    # 왼쪽 위 가로등 머리, 가운데 큰 고양이 눈(옆에서 본 아몬드), 눈 뒤에 거울
    lx, ly = 150, 260; d.rounded_rectangle([lx-60, ly-40, lx+60, ly+10], radius=20, fill=(170, 170, 190)); d.ellipse([lx-38, ly-30, lx+38, ly+2], fill=LAMP)
    ex, ey = 640, 560
    d.ellipse([ex-260, ey-190, ex+260, ey+190], fill=(232, 214, 120))   # 눈(노란 홍채)
    d.ellipse([ex-60, ey-150, ex+60, ey+150], fill=(50, 46, 60))        # 세로 동공
    d.arc([ex-250, ey-180, ex+250, ey+180], 300, 60, fill=(230, 236, 250), width=26)  # 눈 뒤 거울
    # 빛 점: 가로등 → 눈 속 거울 → 다시 밖으로 (4초 주기로 두 번)
    tt = (t % 4.0)
    mx, my = ex+225, ey  # 거울 자리
    if tt < 1.8:
        k = ease(tt/1.8); px, py = lx+(mx-lx)*k, ly+(my-ly)*k
        d.line([lx, ly, px, py], fill=RAY, width=12)
    elif tt < 3.6:
        k = ease((tt-1.8)/1.8); px, py = mx+(lx-mx)*k*0.9, my+(ly-my)*k*0.9
        d.line([lx, ly, mx, my], fill=mix(N1, RAY, 0.35), width=8)
        d.line([mx, my, px, py], fill=(220, 250, 170), width=14)
        d.ellipse([px-16, py-16, px+16, py+16], fill=(230, 255, 190))
    fade_pill(im, '빛: 들어가', (380, 380), LM, min(1, max(0, (t-0.6)/0.5)))
    fade_pill(im, '거울*: 튕겨 나와', (ex+180, ey+260), LT, min(1, max(0, (t-2.2)/0.5)))
    footnote(d, "*눈 속의 이 거울 같은 층을 '휘판'이라고 해요")
    return im

# ================= 한글 =================
WOOD = (226, 206, 176); WOOD_D = (204, 182, 150); TAG = (255, 252, 240); MOUTH_IN = (160, 90, 100); TEETH = (255, 255, 255)
HG1 = 6*F
def hg_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (246, 240, 232)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '이 글자 누가 만들었어?', font=FBW, fill=TXT, anchor='mm')
    x0, y0, cw, ch = 90, 250, 300, 270; names = ['민서', '하늘', '지우', '']
    for r in range(2):
        for c in range(2):
            x = x0+c*cw; y = y0+r*ch
            d.rectangle([x, y, x+cw-14, y+ch-14], fill=WOOD, outline=WOOD_D, width=6)
            d.rounded_rectangle([x+50, y+165, x+135, y+215], radius=20, fill=(150, 170, 210)); d.rounded_rectangle([x+150, y+165, x+235, y+215], radius=20, fill=(150, 170, 210))
            nm = names[r*2+c]
            if nm:
                d.rounded_rectangle([x+60, y+40, x+cw-74, y+110], radius=14, fill=TAG, outline=(220, 210, 190), width=3)
                d.text((x+(cw-14)/2, y+75), nm, font=FNM, fill=INK, anchor='mm')
    hx, hy = 880, 560
    d.ellipse([hx-70, hy-70, hx+70, hy+70], fill=SKIN); d.ellipse([hx-38, hy-18, hx-22, hy-2], fill=INK); d.ellipse([hx+22, hy-18, hx+38, hy-2], fill=INK)
    d.arc([hx-30, hy+5, hx+30, hy+45], 20, 160, fill=LIP, width=6)
    d.rounded_rectangle([hx-60, hy+70, hx+60, hy+200], radius=40, fill=(180, 200, 230))
    k = ease(t/1.2); ax, ay = hx-50, hy+110; tx, ty = 700, 330; ex_, ey_ = int(ax+(tx-ax)*k), int(ay+(ty-ay)*k)
    d.line([ax, ay, ex_, ey_], fill=SKIN, width=30); d.ellipse([ex_-20, ey_-20, ex_+20, ey_+20], fill=SKIN)
    fade_pill(im, '글자: 입 모양 그림', (540, 900), LT, min(1, max(0, (t-2.5)/0.6)))
    return im
def face(d, cx, cy, mouth, teeth=0.0, close=0.0):
    d.ellipse([cx-260, cy-260, cx+260, cy+260], fill=SKIN)
    d.ellipse([cx-120, cy-90, cx-80, cy-50], fill=INK); d.ellipse([cx+80, cy-90, cx+120, cy-50], fill=INK)
    d.ellipse([cx-200, cy-10, cx-140, cy+30], fill=(250, 200, 200)); d.ellipse([cx+140, cy-10, cx+200, cy+30], fill=(250, 200, 200))
    mh = 10+110*mouth
    if close >= 1: d.line([cx-110, cy+120, cx+110, cy+120], fill=LIP, width=18)
    else:
        d.ellipse([cx-120, cy+120-mh, cx+120, cy+120+mh], fill=MOUTH_IN, outline=LIP, width=10)
        if teeth > 0:
            n = 6; th = int(34*teeth)
            for k in range(n):
                x = cx-96+k*192/n; d.rounded_rectangle([x+3, cy+120-mh+10, x+192/n-3, cy+120-mh+10+th], radius=8, fill=TEETH)
HG2 = 11*F
def trace_rect(d, box, k, col, w=16):
    x0, y0, x1, y1 = box; per = 2*((x1-x0)+(y1-y0)); L = k*per
    segs = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    for (a, b) in segs:
        sl = math.dist(a, b)
        if L <= 0: break
        f = min(1, L/sl); d.line([a, (a[0]+(b[0]-a[0])*f, a[1]+(b[1]-a[1])*f)], fill=col, width=w); L -= sl
def trace_siot(d, cx, cy, size, k, col, w=16):
    # ㅅ: 꼭짓점에서 양쪽 다리로
    top = (cx, cy-size); l = (cx-size*0.7, cy+size); r = (cx+size*0.7, cy+size)
    f1 = min(1, k*2); f2 = min(1, max(0, k*2-1))
    if f1 > 0: d.line([top, (top[0]+(l[0]-top[0])*f1, top[1]+(l[1]-top[1])*f1)], fill=col, width=w)
    if f2 > 0: d.line([top, (top[0]+(r[0]-top[0])*f2, top[1]+(r[1]-top[1])*f2)], fill=col, width=w)
def hg_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '거울 앞에서', font=FBW, fill=TXT, anchor='mm')
    cx, cy = 360, 500
    if t < 5.2:
        k = ease((t-0.3)/1.2); closed = t > 1.5
        face(d, cx, cy, mouth=0.5*(1-k), close=1 if closed else 0)
        if closed:
            d.rounded_rectangle([cx-110, cy+100, cx+110, cy+140], radius=18, fill=LIP)   # 다문 입술
            tk = ease((t-1.6)/1.8)
            box = [cx-118, cy+92, cx+118, cy+148]
            if tk > 0: trace_rect(d, box, tk, INK)                                      # 입 따라 ㅁ 그리기
            sk = ease((t-3.6)/1.2)
            if sk > 0:  # 그려진 ㅁ이 옆으로 옮겨가며 정사각형 글자로
                bx0 = box[0]+(700-box[0])*sk; bx1 = box[2]+(960-box[2])*sk; by0 = box[1]+(380-box[1])*sk; by1 = box[3]+(640-box[3])*sk
                d.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=INK, width=22)
        fade_pill(im, '음~  다문 입', (cx, 860), LT, min(1, max(0, (t-0.4)/0.5))*(1 if t < 4.6 else max(0, (5.2-t)/0.6)))
    else:
        u = t-5.2; k = ease((u-0.2)/1.2); face(d, cx, cy, mouth=0.35, teeth=k)
        d.rounded_rectangle([700, 380, 960, 640], radius=10, outline=INK, width=22)
        mh = 10+110*0.35; ty = cy+120-mh+10  # 이 윗선
        tk = ease((u-1.5)/1.6)
        tooth_cx = cx+16; tooth_cy = ty+30
        if tk > 0: trace_siot(d, tooth_cx, tooth_cy, 44, tk, LT, w=14)               # 이 하나 따라 ㅅ
        sk = ease((u-3.3)/1.2)
        if sk > 0:
            sx = tooth_cx+(830-tooth_cx)*sk; sy = tooth_cy+(800-tooth_cy)*sk; size = 44+(95-44)*sk
            trace_siot(d, sx, sy, size, 1, mix(LT, INK, sk), w=int(14+10*sk))
        fade_pill(im, '스~  이가 보여', (cx, 860), LM, min(1, max(0, (u-0.2)/0.5)))
    return im
def hg_sounds(total, sr):
    y = np.zeros(int(sr*total)); base = HG1/F-1.0
    t0 = base+0.6; n = int(sr*1.4); tt = np.arange(n)/sr
    y[int(sr*t0):int(sr*t0)+n] += (0.18*np.sin(2*np.pi*165*tt)+0.08*np.sin(2*np.pi*330*tt))*env(sr, n, 0.15, 0.3)
    t1 = base+5.4; n = int(sr*1.2); rng = np.random.default_rng(1); noise = np.convolve(rng.normal(0, 1, n), np.ones(6)/6, mode='same')
    y[int(sr*t1):int(sr*t1)+n] += 0.06*noise*env(sr, n, 0.2, 0.4)
    return y

if __name__ == '__main__':
    which = sys.argv[1]; out = sys.argv[2]
    if which == 'shadow':
        build('shadow2', sh_s1, SH1, sh_s2, SH2, out, preview=[(sh_s1, 3*F, SH1), (sh_s2, int(3*F), SH2), (sh_s2, int(6*F), SH2), (sh_s2, int(9*F), SH2)])
    elif which == 'cat':
        build('cat2', ct_s1, CT1, ct_s2, CT2, out, preview=[(ct_s1, int(1.5*F), CT1), (ct_s1, int(5*F), CT1), (ct_s2, int(1.2*F), CT2), (ct_s2, int(3*F), CT2)])
    elif which == 'hangeul':
        build('hangeul2', hg_s1, HG1, hg_s2, HG2, out, sounds=hg_sounds, preview=[(hg_s1, 4*F, HG1), (hg_s2, int(3*F), HG2), (hg_s2, int(8*F), HG2), (hg_s2, int(10*F), HG2)])
