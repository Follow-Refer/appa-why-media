"""여기서 바다 소리 나!(11/19): 상황(잠자리, 소라를 귀에 대고 쏴아~) → 답(냉장고·창밖 차 소리가 소라와 컵으로 들어가 쏴아. 소리가 멈추면 쏴아도 작아짐).
사용: python3 example_seashell_sound_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import numpy as np
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
HAIR = (120, 96, 82); KID_SHIRT = (246, 200, 150); MOUTH = (200, 110, 118)
SHELL = (246, 206, 190); SHELL_D = (222, 168, 150); CUP = (180, 206, 232); CUP_D = (140, 172, 210)
FRIDGE = (236, 240, 246); FRIDGE_D = (200, 206, 222)
WAVE = (232, 150, 120); WAVE2 = (140, 160, 210)


def lab(im, text, xy, col, t, t_on, t_off=None):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def face(d, cx, cy, r, mood='smile'):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=SKIN)
    d.chord([cx-r-2, cy-r-6, cx+r+2, cy+r*0.38], 180, 360, fill=HAIR)
    ex = r*0.38; ey = cy+r*0.10; er = r*0.10
    for sx in (cx-ex, cx+ex):
        if mood == 'listen':
            d.arc([sx-er*1.6, ey-er*1.2, sx+er*1.6, ey+er*1.2], 200, 340, fill=INK, width=max(3, int(r*0.07)))
        else:
            d.ellipse([sx-er, ey-er*1.1, sx+er, ey+er*1.1], fill=INK)
    my = cy+r*0.55
    if mood == 'wow':
        d.ellipse([cx-r*0.14, my-r*0.06, cx+r*0.14, my+r*0.20], fill=MOUTH)
    else:
        d.arc([cx-r*0.24, my-r*0.16, cx+r*0.24, my+r*0.14], 20, 160, fill=LIP, width=max(3, int(r*0.07)))
    d.ellipse([cx-r*0.72, cy+r*0.32, cx-r*0.48, cy+r*0.48], fill=(250, 206, 196))
    d.ellipse([cx+r*0.48, cy+r*0.32, cx+r*0.72, cy+r*0.48], fill=(250, 206, 196))


def shell(d, x, y, s, flip=1):
    """소라: 귀 쪽(x)으로 입이 열린 원뿔 + 나선 줄."""
    tip = (x-flip*150*s, y-40*s)
    pts = [(x, y-62*s), (x, y+62*s), (x-flip*70*s, y+70*s), tip, (x-flip*80*s, y-78*s)]
    d.polygon(pts, fill=SHELL)
    for k in range(1, 4):
        xx = x-flip*(35+32*k)*s
        d.arc([xx-28*s, y-62*s+k*8*s, xx+28*s, y+62*s-k*12*s], 250 if flip > 0 else -70, 110 if flip > 0 else 70, fill=SHELL_D, width=int(6*s))
    d.ellipse([x-18*s, y-62*s, x+18*s, y+62*s], fill=(250, 232, 222), outline=SHELL_D, width=int(5*s))


def cup(d, x, y, s, flip=-1):
    """컵: 옆으로 눕혀 입구가 귀 쪽(x)."""
    x2 = x-flip*130*s
    x0, x1 = sorted((x, x2))
    d.rounded_rectangle([x0, y-58*s, x1, y+58*s], radius=int(22*s), fill=CUP)
    d.ellipse([x-16*s, y-60*s, x+16*s, y+60*s], fill=(226, 238, 248), outline=CUP_D, width=int(5*s))
    hx = (x+x2)/2
    d.arc([hx-36*s, y+30*s, hx+36*s, y+100*s], 0, 180, fill=CUP_D, width=int(12*s))


def kid(d, cx, cy, r, mood, left=None, right=None):
    """상반신 아이. left/right: 'shell' 'cup' None. 팔은 짧게 귀 옆으로 접음."""
    by = cy+r*0.85
    d.rounded_rectangle([cx-r*1.05, by, cx+r*1.05, by+r*2.2], radius=int(r*0.6), fill=KID_SHIRT)
    face(d, cx, cy, r, mood)
    for side, obj in ((-1, left), (1, right)):
        ex = cx+side*r*1.02
        if obj is None: continue
        sh = (cx+side*r*0.95, by+r*0.45); hand = (ex+side*r*0.30, cy+r*0.42)
        d.line([sh, hand], fill=KID_SHIRT, width=int(r*0.36))
        d.ellipse([sh[0]-r*0.18, sh[1]-r*0.18, sh[0]+r*0.18, sh[1]+r*0.18], fill=KID_SHIRT)
        s = r/130
        if obj == 'shell': shell(d, ex+side*4, cy, s*0.95, flip=-side)
        else: cup(d, ex+side*4, cy, s*0.95, flip=-side)
        d.ellipse([hand[0]-r*0.16, hand[1]-r*0.16, hand[0]+r*0.16, hand[1]+r*0.16], fill=SKIN)


def ripple(im, cx, cy, side, amp, t, col):
    """귀 옆에서 퍼지는 작은 물결(쏴아)."""
    if amp <= 0.02: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for k in range(3):
        u = ((t*0.9+k/3) % 1)
        r = 30+u*90*amp+10
        a = int(200*amp*(1-u))
        if side < 0: ld.arc([cx-r, cy-r, cx+r, cy+r], 200, 250, fill=col+(a,), width=8)
        else: ld.arc([cx-r, cy-r, cx+r, cy+r], 290, 340, fill=col+(a,), width=8)
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


# ---------------- 장면 1: 잠자리, 소라 귀에 대기 ----------------
S1 = int(4.0*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((120, 126, 176), (176, 170, 210), yy/H))
    d.text((W/2, 80), '여기서 바다 소리 나!', font=FBW, fill=(244, 240, 252), anchor='mm')
    d.rounded_rectangle([90, 170, 300, 340], radius=30, fill=(90, 100, 150))
    d.ellipse([210, 200, 270, 260], fill=(250, 236, 180)); d.ellipse([228, 192, 282, 250], fill=(90, 100, 150))
    d.rounded_rectangle([150, 440, 930, 700], radius=40, fill=(214, 190, 160))
    k = ease((t-0.3)/1.0)
    kid(d, 540, 560, 130, 'listen' if t > 1.4 else 'smile', left='shell' if k > 0.5 else None)
    if k <= 0.5:   # 아직 손에 든 소라
        shell(d, 330, 820-40*k, 0.9, flip=-1)
    d.rounded_rectangle([110, 820, 970, 1080], radius=60, fill=(196, 214, 236))
    for x in range(180, 940, 150): d.ellipse([x, 880, x+40, 920], fill=(170, 192, 222))
    # 그림책(이불 위)
    d.polygon([(560, 890), (690, 870), (690, 960), (560, 980)], fill=(246, 214, 140))
    d.polygon([(820, 890), (690, 870), (690, 960), (820, 980)], fill=(250, 226, 160))
    for wx in range(585, 670, 30): d.arc([wx, 915, wx+30, 935], 180, 360, fill=(140, 170, 210), width=4)
    ripple(im, 540-130*1.02-120, 560, -1, ease((t-1.3)/0.6), t, WAVE)
    lab(im, '쏴아~', (190, 430), LT, t, 1.5)
    return im


# ---------------- 장면 2: 집 소리가 소라·컵으로 ----------------
S2 = int(14.0*F)
QUIET = 8.0           # 냉장고·차 소리 멈추는 시각
KX, KY, KR = 560, 600, 118


def loud(t):
    """주변 소리 크기 0~1."""
    on = ease((t-0.8)/1.2)
    off = 1-0.85*ease((t-QUIET)/1.6)
    return on*off


def car_x(t):
    if t > QUIET+0.6: return None
    return 560+((t*150) % 520)


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix((222, 226, 240), (240, 236, 246), yy/H))
    d.text((W/2, 80), '쏴아 소리, 어디서 왔을까?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 960, W, H], fill=(214, 204, 186))
    # 냉장고(왼쪽)
    d.rounded_rectangle([40, 330, 220, 960], radius=26, fill=FRIDGE, outline=FRIDGE_D, width=5)
    d.line([40, 560, 220, 560], fill=FRIDGE_D, width=5)
    d.rounded_rectangle([190, 400, 202, 500], radius=6, fill=FRIDGE_D)
    d.rounded_rectangle([190, 600, 202, 720], radius=6, fill=FRIDGE_D)
    # 창(오른쪽 위) + 차
    wx0, wy0, wx1, wy1 = 640, 150, 1040, 360
    d.rounded_rectangle([wx0, wy0, wx1, wy1], radius=24, fill=(206, 224, 244), outline=(200, 196, 214), width=8)
    d.rectangle([wx0+8, 300, wx1-8, wy1-8], fill=(190, 190, 200))
    cx = car_x(t)
    if cx is not None and cx < wx1-30:
        x = max(wx0+10, cx)
        d.rounded_rectangle([x, 262, min(wx1-10, x+110), 305], radius=16, fill=(232, 150, 120))
        d.rounded_rectangle([x+20, 240, min(wx1-10, x+80), 270], radius=12, fill=(240, 180, 160))
        for wxx in (x+25, x+85):
            if wxx < wx1-16: d.ellipse([wxx-12, 296, wxx+12, 320], fill=(110, 104, 126))
    # 소리 물결: 냉장고 → 아이, 창 → 아이
    L = loud(t)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    srcs = [((220, 620), (KX-KR-150, KY), WAVE2), ((wx0+40, wy1), (KX+KR+150, KY), WAVE)]
    for (sx, sy), (tx, ty), col in srcs:
        for k in range(4):
            u = ((t*0.45+k/4) % 1)
            px = sx+(tx-sx)*u; py = sy+(ty-sy)*u
            a = int(190*L*math.sin(math.pi*u))
            if a <= 4: continue
            ang = math.degrees(math.atan2(ty-sy, tx-sx))
            ld.arc([px-34, py-34, px+34, py+34], ang-50, ang+50, fill=col+(a,), width=9)
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')); d = ImageDraw.Draw(im)
    mood = 'wow' if L > 0.5 else 'smile'
    kid(d, KX, KY, KR, mood, left='shell', right='cup')
    amp = 0.25+0.75*L
    ripple(im, KX-KR*1.02-110, KY, -1, amp, t, WAVE)
    ripple(im, KX+KR*1.02+110, KY, 1, amp, t, WAVE)
    lab(im, '집 소리', (150, 260), LM, t, 1.6, QUIET)
    lab(im, '컵도 쏴아', (KX+190, KY+230), LG, t, 4.2, QUIET)
    lab(im, '조용하면 작게', (KX, KY-230), LT, t, QUIET+1.2)
    return im


def sounds(total, sr):
    n = int(total*sr); rng = np.random.default_rng(3)
    x = rng.standard_normal(n)
    # 부드러운 파도 소리: 저역 통과(이동 평균 두 번)
    k = 60; x = np.convolve(x, np.ones(k)/k, 'same'); x = np.convolve(x, np.ones(k)/k, 'same')
    x /= np.max(np.abs(x))+1e-9
    tt = np.arange(n)/sr
    t1 = S1/F; off = t1-1.0
    g = np.zeros(n)
    # 장면1: 소라 댈 때 작게
    g += np.clip((tt-1.3)/0.6, 0, 1)*np.clip((off+0.5-tt)/0.5, 0, 1)*0.35
    # 장면2: 주변 소리 따라
    t2 = tt-off
    L = np.array([loud(v) if v >= 0 else 0 for v in t2[::sr//100]])
    L = np.interp(np.arange(n), np.arange(len(L))*(sr//100), L)
    g += np.where(t2 >= 0, 0.15+0.85*L, 0)*np.clip(t2/0.8, 0, 1)
    swell = 0.8+0.2*np.sin(2*np.pi*tt/3.2)
    y = x*g*swell*0.16
    y[-int(sr*0.6):] *= np.linspace(1, 0, int(sr*0.6))
    return y


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/seashell_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('seashell', s1, S1, s2, S2, out, sounds=sounds,
              preview=[(s1, int(2.6*F), S1), (s2, int(3.0*F), S2), (s2, int(6.0*F), S2), (s2, int(13.5*F), S2)])
