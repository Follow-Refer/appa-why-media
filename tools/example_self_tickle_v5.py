"""내가 하면 왜 안 간지러워(11/6): 상황(잠자리, 아이가 자기 옆구리를 간지럽혀도 멀뚱) → 답(내 손: 머리가 미리 알아서 살살 / 아빠 손: 깜짝! 까르르)."""
from v5_answer import *
BG = (236, 232, 246); BED = (214, 204, 232); PILLOW = (250, 246, 236); BLANKET = (196, 210, 236)
DAD_SLEEVE = (170, 196, 170); KID_SHIRT = (246, 200, 150)
SPARK = (250, 206, 120); SPARK2 = (240, 160, 170)

def kid_face(d, cx, cy, s, mood):
    """mood: 'calm' 멀뚱 / 'laugh' 까르르 / 'hmm' 갸우뚱"""
    d.ellipse([cx-90*s, cy-90*s, cx+90*s, cy+90*s], fill=SKIN)
    d.chord([cx-92*s, cy-96*s, cx+92*s, cy+40*s], 180, 360, fill=(120, 96, 82))
    w = max(3, int(6*s))
    if mood == 'laugh':
        for ex in (cx-36*s, cx+36*s): d.arc([ex-16*s, cy-2*s, ex+16*s, cy+22*s], 200, 340, fill=INK, width=w)
        d.chord([cx-34*s, cy+30*s, cx+34*s, cy+78*s], 0, 180, fill=(214, 120, 124))
        d.ellipse([cx-70*s, cy+24*s, cx-44*s, cy+44*s], fill=(248, 196, 190)); d.ellipse([cx+44*s, cy+24*s, cx+70*s, cy+44*s], fill=(248, 196, 190))
    else:
        for ex in (cx-36*s, cx+36*s): d.ellipse([ex-9*s, cy+0*s, ex+9*s, cy+18*s], fill=INK)
        if mood == 'hmm': d.line([cx-18*s, cy+56*s, cx+18*s, cy+52*s], fill=LIP, width=w)
        else: d.line([cx-20*s, cy+56*s, cx+20*s, cy+56*s], fill=LIP, width=w)

def mitten(d, x, y, s, col=SKIN, wig=0.0):
    """둥근 손 + 손가락 셋(꼼지락). 팔은 짧은 소매로만."""
    d.rounded_rectangle([x-48*s, y-36*s, x+48*s, y+36*s], radius=int(34*s), fill=col)
    for k in range(3):
        fx = x-30*s+k*30*s; fy = y-30*s - (10*s if (k % 2 == 0) == (wig > 0.5) else 0)
        d.rounded_rectangle([fx-11*s, fy-38*s, fx+11*s, fy+6*s], radius=int(11*s), fill=col)

def sparks(d, x, y, r, k, cols=(SPARK, SPARK2)):
    if k <= 0: return
    for a in range(8):
        ang = a*math.pi/4 + 0.3
        r0, r1 = r*0.55, r*(0.55+0.6*k)
        d.line([x+math.cos(ang)*r0, y+math.sin(ang)*r0, x+math.cos(ang)*r1, y+math.sin(ang)*r1], fill=cols[a % 2], width=max(4, int(10*k)))

def kid_body(d, cx, cy, s):
    """얼굴 아래 몸통(이불 위로 상반신)."""
    d.rounded_rectangle([cx-120*s, cy+70*s, cx+120*s, cy+330*s], radius=int(70*s), fill=KID_SHIRT)

# ---------------- 장면 1: 잠자리, 아이가 자기 옆구리를 간지럽혀 봄 ----------------
TK1 = int(5*F)
def tk_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '내가 하면 왜 안 간지러워?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 820, W, H], fill=BED)
    d.rounded_rectangle([300, 300, 780, 520], radius=90, fill=PILLOW)
    cx, cy = 540, 470
    kid_body(d, cx, cy, 1.0)
    d.rounded_rectangle([120, 720, 960, 1100], radius=80, fill=BLANKET)
    kid_face(d, cx, cy, 1.0, 'hmm' if t > 2.6 else 'calm')
    # 자기 손으로 옆구리 꼼지락 (몸 바로 옆, 짧게)
    wig = (math.sin(t*12) > 0)
    hx, hy = cx+118, cy+225 + 8*math.sin(t*12)
    d.rounded_rectangle([cx+90, cy+190, cx+150, cy+260], radius=26, fill=KID_SHIRT)   # 짧은 소매
    mitten(d, hx, hy, 0.85, wig=1.0 if wig else 0.0)
    for k in range(2):
        a = ease((t-2.8-k*0.45)/0.4)
        if a > 0: d.text((cx+190+k*60, cy-80-k*40-a*16), '?', font=FBW, fill=mix(BG, LM, a), anchor='mm')
    lab(im, '내 손', (cx+170, cy+120), LM, t, 1.2)
    return im

# ---------------- 장면 2: 내 손 vs 아빠 손, 나란히 ----------------
PL = (40, 170, 520, 960); PR = (560, 170, 1040, 960)
def panel_kid(im0, box, t_touch, t, own):
    im = Image.new('RGB', im0.size, BG); _panel(im, box, t_touch, t, own)
    m = Image.new('L', im0.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, radius=50, fill=255)
    im0.paste(im, (0, 0), m); ImageDraw.Draw(im0).rounded_rectangle(box, radius=50, outline=(255, 255, 255), width=8)

def _panel(im, box, t_touch, t, own):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box; cx = (x0+x1)//2; cy = y0+330
    d.rounded_rectangle(box, radius=50, fill=(248, 246, 252))
    d.rounded_rectangle([x0, y1-170, x1, y1], radius=50, fill=BLANKET)
    kid_body(d, cx, cy, 0.75)
    u = t - t_touch
    touched = u >= 0
    if own:
        # 머리 위 생각 구름: 손 그림이 '먼저' 나타남 → 그다음 진짜 손이 닿음
        kb = ease((t-(t_touch-1.4))/0.5)
        if kb > 0:
            bx, by = cx+60, cy-205
            d.ellipse([cx+18, cy-110, cx+40, cy-88], fill=mix((248, 246, 252), (255, 255, 255), kb), outline=mix((248, 246, 252), (200, 196, 214), kb), width=3)
            d.ellipse([bx-110, by-62, bx+110, by+62], fill=(255, 255, 255), outline=mix((248, 246, 252), (200, 196, 214), kb), width=4)
            mitten(d, bx, by+14, 0.6*kb, col=mix((255, 255, 255), SKIN, kb), wig=0)
        mood = 'calm'
        hx = cx+110; hy = cy+190 + (8*math.sin(t*12) if touched else 0)
        if not touched: hx += 60*(1-ease((t-(t_touch-0.9))/0.9))
        d.rounded_rectangle([cx+60, cy+150, cx+110, cy+215], radius=22, fill=KID_SHIRT)
        mitten(d, hx, hy, 0.7, wig=1.0 if (touched and math.sin(t*12) > 0) else 0.0)
        if touched: sparks(d, hx-60, hy-10, 70, 0.25)            # 살살, 아주 작게
        kid_face(d, cx, cy, 0.75, mood)
    else:
        # 아빠 손: 패널 오른쪽 밖에서 소매와 함께 들어옴 (어른 손 크기, 팔 길게 늘이지 않음)
        k = ease((t-(t_touch-1.2))/1.2)
        hx = x1+90 - (x1+90-(cx+120))*k; hy = cy+200 + (10*math.sin(t*13) if touched else 0)
        if k > 0:
            d.rounded_rectangle([hx+40, hy-50, max(hx+60, x1+20), hy+50], radius=40, fill=DAD_SLEEVE)
            mitten(d, hx, hy, 1.0, col=(240, 210, 184), wig=1.0 if (touched and math.sin(t*13) > 0) else 0.0)
        laugh = touched and u > 0.15
        bounce = 10*abs(math.sin(t*9)) if laugh else 0
        if laugh:
            sparks(d, hx-40, hy-60, 70, min(1, u/0.4))
            sparks(d, cx-150, cy-110-bounce, 70, min(1, u/0.5))
        kid_face(d, cx, cy-bounce, 0.75, 'laugh' if laugh else ('hmm' if k > 0.5 else 'calm'))

TK2 = int(12.5*F)
def tk_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '누구 손이 간지러울까?', font=FBW, fill=TXT, anchor='mm')
    panel_kid(im, PL, 2.4, t, own=True)
    # 오른쪽 패널은 왼쪽이 끝난 뒤 시작
    panel_kid(im, PR, 6.4, t, own=False)
    lab(im, '내 손', ((PL[0]+PL[2])//2, 1010), LM, t, 0.4)
    lab(im, '미리 알아!', ((PL[0]+PL[2])//2+60, 200), LG, t, 1.6)
    lab(im, '아빠 손', ((PR[0]+PR[2])//2, 1010), LT, t, 4.6)
    lab(im, '깜짝!', ((PR[0]+PR[2])//2-110, 220), LT, t, 6.7)
    return im

if __name__ == '__main__':
    import vid
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/tickle_preview.png'
    vid.preview_path = lambda name: pv
    build('tickle', tk_s1, TK1, tk_s2, TK2, out,
          preview=[(tk_s1, int(3.5*F), TK1), (tk_s2, int(3.5*F), TK2), (tk_s2, int(7.5*F), TK2), (tk_s2, int(11.5*F), TK2)])
