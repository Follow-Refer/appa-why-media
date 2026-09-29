"""해답 장면 중심 영상 (9/29 사용자 지시): 글 전체가 아니라, 부모가 말로 설명하기 힘든 '답' 한 장면을 아이 눈높이로.
사용: python3 v5_answer.py <lightning|contrail> out.mp4"""
from v3_videos import *

# ================= 번개 = 아주 큰 문고리 따닥 =================
DOOR = (214, 190, 160); DOOR_D = (190, 164, 132); KNOB = (232, 196, 110); KNOB_D = (200, 160, 80)

def knob_scene(d, cx, cy, s, hand_x, spark):
    """문 가장자리 + 둥근 손잡이 + 다가오는 손(손가락 하나). spark 0~1."""
    d.rectangle([cx+60*s, cy-420*s, cx+400*s, cy+420*s], fill=DOOR)
    d.rectangle([cx+60*s, cy-420*s, cx+80*s, cy+420*s], fill=DOOR_D)
    d.ellipse([cx+100*s, cy-30*s, cx+160*s, cy+30*s], fill=KNOB_D)            # 손잡이 목
    d.ellipse([cx-10*s, cy-70*s, cx+130*s, cy+70*s], fill=KNOB)
    d.ellipse([cx+10*s, cy-50*s, cx+60*s, cy-10*s], fill=(250, 226, 160))
    # 손: 둥근 주먹 + 검지 하나 (팔 없음, 화면 왼쪽 밖에서 들어옴)
    hx = hand_x
    if hx-200*s > -10: d.rectangle([-10, cy-40*s, hx-200*s, cy+100*s], fill=(150, 170, 210))                 # 소매(화면 밖에서 이어짐)
    d.rounded_rectangle([hx-230*s, cy-60*s, hx-60*s, cy+90*s], radius=int(60*s), fill=SKIN)
    d.rounded_rectangle([hx-90*s, cy-34*s, hx, cy+6*s], radius=int(20*s), fill=SKIN)
    d.ellipse([hx-26*s, cy-30*s, hx-6*s, cy+2*s], fill=(246, 214, 200))       # 손톱
    if spark > 0:
        gap0, gap1 = hx+4*s, cx-12*s
        random.seed(int(spark*7))
        pts = [(gap0, cy-14*s)]
        for k in range(1, 4):
            f = k/4; pts.append((gap0+(gap1-gap0)*f, cy-14*s+random.uniform(-16, 16)*s))
        pts.append((gap1, cy-14*s))
        d.line(pts, fill=(255, 236, 120), width=max(4, int(14*s*spark)), joint='curve')
        mx, my = (gap0+gap1)/2, cy-14*s
        for a in range(8):
            ang = a*math.pi/4; r0, r1 = 30*s, (30+40*spark)*s
            d.line([mx+math.cos(ang)*r0, my+math.sin(ang)*r0, mx+math.cos(ang)*r1, my+math.sin(ang)*r1], fill=(255, 226, 110), width=max(3, int(8*s)))

LA1 = int(7.6*F)
SIT = 2.8
def la_s1(i, n):
    if i/F < SIT:
        return ln_s1(int((i/F + 0.6)*F), n)          # 원래 상황 장면(번쩍 → 이불 속)을 짧게
    t = i/F - SIT + 0.2
    sp = max(0, 1-abs(t-3.0)/0.25) + max(0, 1-abs(t-3.35)/0.15)*0.6
    im = Image.new('RGB', (W, H), mix((236, 226, 214), (255, 252, 230), min(1, sp*0.5))); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '겨울에 문고리 만지면', font=FBW, fill=TXT, anchor='mm')
    hx = lerp_(80, 468, ease(t/2.9)) if t < 3.0 else 468 - 60*ease((t-3.2)/0.4)
    knob_scene(d, 500, 560, 1.0, hx, min(1, sp))
    lab(im, '따닥!', (560, 330), LT, t, 3.0)
    return im

def lerp_(a, b, k): return a+(b-a)*k

LA2 = 10*F
def la_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(RN1, RN2, yy/H))
    d.text((W/2, 80), '구름 속에서도 따닥!', font=FBW, fill=(240, 236, 250), anchor='mm')
    d.rectangle([0, 940, W, H], fill=(70, 80, 90))
    for x in range(40, 1080, 180): d.rectangle([x, 880, x+120, 940], fill=(90, 100, 110))
    for cx, cy, r in ((300, 380, 170), (520, 320, 210), (760, 380, 180), (420, 500, 170), (660, 500, 180)):
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=CLOUD)
    # 작은 얼음은 위로, 큰 얼음은 아래로. 부딪힐 때마다 작은 '따닥'
    for k in range(10):
        ph = (t*0.45+k*0.1) % 1; xs = 260+k*52
        if k % 2 == 0: y = 580-ph*300; r = 12; c = (230, 240, 255)
        else: y = 280+ph*300; r = 22; c = (200, 214, 240)
        if t < 5.8: d.ellipse([xs-r, y-r, xs+r, y+r], fill=c)
        if abs(ph-0.5) < 0.05 and t < 5.6:
            sx, sy = xs-26, 430
            d.line([(sx-18, sy-10), (sx-4, sy+6), (sx+6, sy-6), (sx+20, sy+10)], fill=YEL, width=7)
    # 따닥이 모여 구름이 점점 빛남
    charge = min(1, max(0, (t-1.0)/4.5))
    if 0 < charge and t < 6.0:
        d = blend(im, lambda dd: dd.ellipse([260, 250, 820, 620], fill=(255, 236, 120, int(100*charge*(0.5+0.5*abs(math.sin(t*7)))))))
    # 6초: 아주 큰 따닥 = 번개
    if t >= 6.0:
        u = t-6.0; a = max(0, 1-max(0, u-0.6)/1.0)
        if a > 0:
            d = blend(im, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 230, int(120*a*(1 if u < 0.15 else 0.4)))))
            bolt(d, 560, 560, 600, 880, seed=7, w=int(30*a)+2, col=mix(RN1, BOLT, a))
    if t >= 8.0 and int(t*3) % 2 == 0:                      # 작은 따닥과 같은 박자로 큰 따닥
        bolt(d, 560, 560, 600, 880, seed=7, w=26, col=BOLT)
    # 7.5초~: 작은 문고리 따닥을 옆에 나란히 (같은 거야, 크기만 달라)
    k = ease((t-7.4)/0.6)
    if k > 0:
        def inset(dd):
            dd.ellipse([40, 620, 360, 940], fill=(236, 226, 214, int(255*k)), outline=(255, 255, 255, int(255*k)), width=8)
        d = blend(im, inset)
        if k > 0.6:
            sub = Image.new('RGB', (W, H), (236, 226, 214)); sd = ImageDraw.Draw(sub)
            knob_scene(sd, 500, 560, 1.0, 468, 1.0 if int(t*3) % 2 == 0 else 0.0)
            sub = sub.crop((260, 330, 740, 810)).resize((300, 300))
            m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
            im.paste(sub, (50, 630), m); d = ImageDraw.Draw(im)
    lab(im, '얼음: 콩콩', (190, 220), LM, t, 0.6, 6.0)
    lab(im, '아주 큰 따닥!', (820, 720), LT, t, 6.1)
    return im

def la_sounds(total, sr):
    y = np.zeros(int(sr*total)); rng = np.random.default_rng(2)
    for t0, amp, dur in ((5.6, 0.25, 0.08), (5.95, 0.15, 0.06)):          # 작은 따닥
        a = int(sr*t0); n = int(sr*dur); y[a:a+n] += amp*rng.normal(0, 1, n)*np.exp(-np.arange(n)/(sr*0.015))
    for t0, amp in ((1.65, 0.3), (LA1/F-1.0+6.05, 0.45)):                   # 창밖 번쩍, 큰 번개
      n = int(sr*1.6); a = int(sr*t0)
      if a < len(y):
        tt = np.arange(n)/sr; rum = np.convolve(rng.normal(0, 1, n), np.ones(300)/300, mode='same')*8
        y[a:a+n] += (amp*rum*np.exp(-tt/0.6))[:len(y)-a]
    return y

# ================= 비행기구름 = 비행기의 하~ 입김 =================
def breath(d, mx, my, t, period=2.4):
    for j in range(12):                       # 입에서 퍼져 나가는 하얀 김 알갱이 12개
        born = j*0.07
        ph = ((t % period) - born)
        if ph < 0 or ph > 1.6: continue
        f = ph/1.6
        x = mx + 30 + f*330 + (j % 3)*14; y = my - f*70 + ((j*37) % 21 - 10)*f*2; r = 18 + f*46
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, int(235*(1-f)**0.8)))

def winter_kid(im, cx, gy, s, t):
    d = ImageDraw.Draw(im)
    kid(d, cx, gy, s=s, shirt=(200, 150, 160))
    hy = gy-290*s
    d.chord([cx-84*s, hy-92*s, cx+84*s, hy+40*s], 180, 360, fill=(120, 150, 200))       # 털모자
    d.ellipse([cx-18*s, hy-122*s, cx+18*s, hy-86*s], fill=(240, 240, 250))
    d.rounded_rectangle([cx-78*s, hy+70*s, cx+78*s, hy+110*s], radius=int(20*s), fill=(230, 120, 120))  # 목도리
    ph = (t % 2.4)/2.4
    if ph < 0.75:                                                                       # '하~' 입 모양
        d.ellipse([cx+4*s, hy+18*s, cx+34*s, hy+50*s], fill=MOUTH_IN)
    return d

CA1 = int(8.4*F)
def sit_contrail(t):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d)
    d.rectangle([0, 860, W, H], fill=PARK); d.text((W/2, 80), '하늘에 누가 줄 그었어!', font=FBW, fill=TXT, anchor='mm')
    px = 100+ease(t/3.0)*900; py = 330-0.08*px
    if px-170 > -100:
        d = blend(im, lambda dd: dd.line([(-100, 338), (px-170, py+8)], fill=(255, 255, 255, 235), width=26))
    plane(d, px, py, 0.55)
    kid(d, 330, 860, s=0.85)
    lab(im, '하얀 줄!', (760, 560), LT, t, 1.2)
    return im
def ca_s1(i, n):
    if i/F < 3.2: return sit_contrail(i/F)
    t = i/F - 3.2; im = Image.new('RGB', (W, H), (226, 234, 244)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '추운 날 하~', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=(240, 244, 250))
    for k in range(18):                                                                  # 눈송이
        x = (k*83 + int(t*30)) % W; y = (k*131 + int(t*60)) % 820 + 120
        d.ellipse([x-5, y-5, x+5, y+5], fill=(255, 255, 255))
    winter_kid(im, 330, 860, 1.0, t)
    hy = 860-290
    blend(im, lambda dd: breath(dd, 360, hy+34, t))
    lab(im, '하~ 하얀 입김', (740, 420), LM, t, 1.2)
    return im

CA2 = 10*F
def ca_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (70, 120, 200), (150, 196, 240))
    d.text((W/2, 80), '비행기도 하~', font=FBW, fill=(245, 245, 250), anchor='mm')
    ex, ey = 860, 470
    d.rounded_rectangle([ex-150, ey-80, ex+150, ey+80], radius=70, fill=(220, 224, 236)); d.ellipse([ex-170, ey-80, ex-110, ey+80], fill=(120, 124, 140))
    d.polygon([(ex-60, ey-80), (ex+40, ey-230), (ex+120, ey-230), (ex+80, ey-80)], fill=PLANE_D)
    for k in range(60):
        born = k*0.13
        if t > born:
            age = t-born; x = ex-180-age*190; y = ey+math.sin(k*1.7)*30*(1+age*0.4)
            if x > -40:
                cool = min(1, age/1.2); col = mix((255, 196, 150), (255, 255, 255), cool); r = 16+6*cool
                d.ellipse([x-r, y-r, x+r, y+r], fill=col)
                if cool > 0.95 and k % 3 == 0:
                    d.line([x-r-6, y, x+r+6, y], fill=(210, 230, 255), width=3); d.line([x, y-r-6, x, y+r+6], fill=(210, 230, 255), width=3)
    tx, ty = 150, 760                                                                    # 온도계
    d.rounded_rectangle([tx-18, ty-200, tx+18, ty+20], radius=18, fill=(245, 245, 250)); d.ellipse([tx-34, ty, tx+34, ty+68], fill=(120, 170, 240))
    d.rectangle([tx-8, ty-40, tx+8, ty+20], fill=(120, 170, 240))
    # 7초~: 아이 입김을 옆에 작게 나란히
    k = ease((t-7.0)/0.6)
    if k > 0:
        sub = Image.new('RGB', (W, H), (226, 234, 244)); winter_kid(sub, 330, 860, 1.0, t)
        blend(sub, lambda dd: breath(dd, 360, 860-290+34, t))
        sub = sub.crop((200, 400, 760, 960)).resize((300, 300))
        m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=int(255*k))
        im.paste(sub, (700, 640), m); d = ImageDraw.Draw(im)
        d.ellipse([700, 640, 1000, 940], outline=(255, 255, 255), width=8)
    lab(im, '엔진도 후~', (ex-120, ey+170), LT, t, 0.6, 7.0)
    lab(im, '꽁꽁: 하얀 줄', (330, 800), LM, t, 3.0)
    return im

if __name__ == '__main__':
    which, out = sys.argv[1], sys.argv[2]
    if which == 'lightning':
        build('lightning5', la_s1, LA1, la_s2, LA2, out, sounds=la_sounds, preview=[(la_s1, int(1.9*F), LA1), (la_s1, int(5.85*F), LA1), (la_s2, int(4.5*F), LA2), (la_s2, int(8.5*F), LA2)])
    elif which == 'contrail':
        build('contrail5', ca_s1, CA1, ca_s2, CA2, out, preview=[(ca_s1, int(2.5*F), CA1), (ca_s1, int(5.5*F), CA1), (ca_s2, int(3.5*F), CA2), (ca_s2, int(8.5*F), CA2)])

# ================= 구름 = 분무기 안개처럼 아주 작은 물방울 =================
def cup_vs_spray(t):
    im = Image.new('RGB', (W, H), (236, 242, 248)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '물을 붓거나, 칙 뿌리면', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=(214, 204, 186)); d.line([540, 150, 540, 900], fill=(210, 216, 226), width=6)
    # 왼쪽: 기울어진 컵에서 큰 물덩이가 '뚝'
    cx, cy = 180, 280
    def rot(px, py, a=math.radians(112)):
        return (cx + px*math.cos(a) - py*math.sin(a), cy + px*math.sin(a) + py*math.cos(a))
    body = [rot(-70, -110), rot(70, -110), rot(55, 110), rot(-55, 110)]          # 위가 넓은 컵, 오른쪽으로 기울임
    water = [rot(-70, -110), rot(70, -110), rot(62, -10), rot(-62, -10)]
    d.polygon(body, fill=(226, 236, 246)); d.polygon(water, fill=(150, 196, 236))
    d.line(body + [body[0]], fill=(170, 186, 206), width=8)
    ph = (t % 1.2)
    if ph < 0.6:
        mx, my = rot(0, -150)
        y = my + (ph/0.6)**2*(880-my)
        d.ellipse([mx-32, y-34, mx+32, y+34], fill=(110, 160, 226))
    else:
        mx, my = rot(0, -150); u = (ph-0.6)/0.6; d.ellipse([mx-52-40*u, 880, mx+52+40*u, 910], fill=(140, 180, 230))
    # 오른쪽: 분무기에서 아주 작은 물방울이 둥둥
    sx, sy = 900, 260
    d.rounded_rectangle([sx-40, sy-20, sx+60, sy+170], radius=24, fill=(150, 200, 170))
    d.rectangle([sx-70, sy-40, sx+40, sy], fill=(120, 170, 140)); d.rectangle([sx-100, sy-30, sx-70, sy-12], fill=(120, 170, 140))
    random.seed(11)
    for puff in range(6):
        born = puff*1.4
        if t < born: continue
        age = t-born
        for j in range(18):
            ang = random.uniform(-0.5, 0.5); sp = random.uniform(120, 220)
            dx = -min(age, 0.5)*sp*math.cos(ang)*2
            x = sx-110 + dx + 12*math.sin(age*2+j)
            y = sy-20 + min(age, 0.5)*sp*math.sin(ang)*2 + age*28
            if y < 890: d.ellipse([x-5, y-5, x+5, y+5], fill=(110, 160, 226))
    return im

CD1 = int(9.5*F)
def cd_s1(i, n):
    if i/F < 3.0: return cl_s1(int((i/F+0.6)*F), n)
    t = i/F - 3.0; im = cup_vs_spray(t)
    lab(im, '크면: 뚝!', (270, 960), LT, t, 0.8)
    lab(im, '작으면: 둥둥', (800, 960), LM, t, 2.2)
    return im

CD2 = 10*F
def cd_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); sky_bg(d, (150, 180, 214), (214, 226, 240))
    d.text((W/2, 80), '구름 속을 보면', font=FBW, fill=TXT, anchor='mm')
    random.seed(5); drops = [(random.uniform(80, 1000), random.uniform(200, 760), random.uniform(0, 6)) for _ in range(110)]
    merge = ease((t-5.0)/1.5); tx, ty = 560, 520
    for k, (x, y, ph) in enumerate(drops):
        x += 10*math.sin(t*2+ph); y += 8*math.cos(t*1.7+ph)
        if k < 14:
            x = x+(tx-x)*merge; y = y+(ty-y)*merge
            if merge >= 1: continue
        d.ellipse([x-5, y-5, x+5, y+5], fill=(120, 170, 230))
    if merge >= 1:
        u = t-6.5; y = ty+max(0, u-0.4)**2*380
        d.polygon([(tx, y-60), (tx-36, y+10), (tx+36, y+10)], fill=(90, 140, 220)); d.ellipse([tx-38, y-14, tx+38, y+54], fill=(90, 140, 220))
    lab(im, '분무기보다 더 작아', (330, 200), LM, t, 0.6)
    lab(im, '뭉치면: 비', (820, 560), LG, t, 6.6)
    return im

if __name__ == '__main__' and sys.argv[1] == 'cloud':
    build('cloud5', cd_s1, CD1, cd_s2, CD2, sys.argv[2], preview=[(cd_s1, int(1.5*F), CD1), (cd_s1, int(6.5*F), CD1), (cd_s2, int(3*F), CD2), (cd_s2, int(8*F), CD2)])
