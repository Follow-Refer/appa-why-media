"""내 코 한쪽만 숨 쉬어(11/24): 상황(잠자리, 옆으로 누운 아이 '한쪽만 숨 쉬어!') →
답(같은 아이를 크게. 베개 쪽 콧구멍은 납작 '막혔어', 위쪽 콧구멍은 숨 쉭쉭 '뻥 뚫려' →
돌아누우면 아래로 간 쪽이 납작해지고, 위로 올라간 쪽에서 숨이 나옴).
사용: python3 example_one_nostril_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
HAIR = (120, 96, 82); NOSE = (240, 196, 172); NOSTRIL = (196, 140, 128)
NIGHT = (206, 210, 236); WALL = (222, 224, 242); PILLOW = (252, 250, 246); PILLOW_D = (228, 224, 236)
BLANKET = (246, 214, 140); BLANKET_D = (232, 196, 120); MOON = (250, 236, 180)


def lab(im, text, xy, col, t, t_on, t_off=None):
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def rot(dx, dy, th):
    """레이어 안 (dx,dy)를 PIL rotate(th, 반시계)와 같게 돌린 화면 좌표 오프셋."""
    a = math.radians(th)
    return dx*math.cos(a)+dy*math.sin(a), -dx*math.sin(a)+dy*math.cos(a)


def head_layer(r, th, openA, openB):
    """정면 얼굴을 그린 뒤 th도 돌린 RGBA. openA/openB: 콧구멍 열린 정도 0(납작)~1."""
    S = int(r*6.4); c = S/2
    L = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # 어깨 + 이불(턱 아래 짧게)
    d.rounded_rectangle([c-r*0.95, c+r*0.78, c+r*0.95, c+r*3.4], radius=int(r*0.45), fill=BLANKET)
    d.line([(c-r*0.85, c+r*1.10), (c+r*0.85, c+r*1.10)], fill=BLANKET_D, width=int(r*0.06))
    d.ellipse([c-r, c-r, c+r, c+r], fill=SKIN)
    d.chord([c-r-2, c-r-6, c+r+2, c+r*0.30], 180, 360, fill=HAIR)
    ey = c+r*0.06; er = r*0.10
    for sx in (c-r*0.38, c+r*0.38):     # 졸린 눈(반달)
        d.arc([sx-er*1.1, ey-er*0.9, sx+er*1.1, ey+er*0.9], 200, 340, fill=INK, width=int(r*0.05))
    d.ellipse([c-r*0.25, c+r*0.14, c+r*0.25, c+r*0.50], fill=NOSE)
    for sx, o in ((c-r*0.11, openA), (c+r*0.11, openB)):
        hy = r*(0.014+0.07*o); hx = r*0.07
        d.ellipse([sx-hx, c+r*0.40-hy, sx+hx, c+r*0.40+hy], fill=NOSTRIL)
    my = c+r*0.66
    d.arc([c-r*0.14, my-r*0.06, c+r*0.14, my+r*0.06], 20, 160, fill=(214, 120, 128), width=int(r*0.04))
    d.ellipse([c-r*0.74, c+r*0.36, c-r*0.50, c+r*0.52], fill=(250, 206, 196))
    d.ellipse([c+r*0.50, c+r*0.36, c+r*0.74, c+r*0.52], fill=(250, 206, 196))
    return L.rotate(th, resample=Image.BICUBIC)


def nostrils(cx, cy, r, th):
    """A(처음 아래쪽), B(처음 위쪽) 화면 위치와 '바깥' 방향."""
    out = {}
    for k, sx in (('A', -0.11), ('B', 0.11)):
        dx, dy = rot(sx*r, 0.40*r, th)
        ox, oy = rot(1 if sx > 0 else -1, 0.25, th)      # 옆+아래로 비스듬히
        n = math.hypot(ox, oy)
        out[k] = (cx+dx, cy+dy, ox/n, oy/n)
    return out


def puffs(im, x, y, ux, uy, r, t, strength):
    if strength <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for k in range(4):
        ph = (t*0.7+k/4) % 1.0
        dist = r*(0.30+1.0*ph)
        px = x+ux*dist; py = y+uy*dist
        s = r*(0.06+0.10*ph)
        a = int(255*strength*min(1, ph*5)*(1-ph))
        d.ellipse([px-s, py-s, px+s, py+s], fill=(255, 255, 255, a), outline=(170, 186, 226, a), width=5)
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def bed(d, top):
    d.rounded_rectangle([60, top, 1020, top+150], radius=60, fill=PILLOW, outline=PILLOW_D, width=6)


def draw_kid(im, cx, cy, r, th, oA, oB, t):
    L = head_layer(r, th, oA, oB)
    im.paste(L, (int(cx-L.width/2), int(cy-L.height/2)), L)
    ns = nostrils(cx, cy, r, th)
    for k, o in (('A', oA), ('B', oB)):
        x, y, ux, uy = ns[k]
        puffs(im, x, y, ux, uy, r, t, max(0, (o-0.5)*2))
    return ns


# ---------------- 장면 1: 잠자리, 옆으로 누워서 ----------------
S1 = int(3.2*F)
def s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.rounded_rectangle([640, 170, 960, 430], radius=30, fill=NIGHT)
    d.ellipse([760, 220, 860, 320], fill=MOON); d.ellipse([790, 205, 890, 305], fill=NIGHT)
    for (sx, sy) in ((690, 230), (700, 380), (910, 370)):
        d.ellipse([sx-6, sy-6, sx+6, sy+6], fill=(250, 246, 220))
    d.text((W/2, 80), '한쪽만 숨 쉬어!', font=FBW, fill=TXT, anchor='mm')
    bed(d, 760)
    d.rounded_rectangle([40, 880, 1040, 1080], radius=50, fill=BLANKET)
    draw_kid(im, 420, 660, 150, 90, 0.0, 1.0, t)
    d = ImageDraw.Draw(im)
    a = ease((t-1.2)/0.5)
    if a > 0: d.text((420, 440-a*14), '?', font=FBW, fill=mix(WALL, LT, a), anchor='mm')
    return im


# ---------------- 장면 2: 크게, 돌아누우면 ----------------
S2 = int(15.0*F)
CX, CY, CR = 540, 560, 230
T_ROLL, ROLL = 5.0, 1.8
T_SWAP, SWAP = T_ROLL+ROLL, 2.0


def s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '돌아누우면?', font=FBW, fill=TXT, anchor='mm')
    bed(d, CY+int(CR*0.80))
    th = 90-180*ease((t-T_ROLL)/ROLL)
    k = ease((t-T_SWAP)/SWAP)
    oA, oB = k, 1-k
    ns = draw_kid(im, CX, CY, CR, th, oA, oB, t)
    # 1막: A 아래(막힘), B 위(뚫림)
    xA, yA = ns['A'][:2]; xB, yB = ns['B'][:2]
    lab(im, '뻥 뚫려', (xB+150, yB-260), LG, t, 0.6, T_ROLL-0.2)
    lab(im, '막혔어', (xA, yA+120), LT, t, 1.6, T_ROLL-0.2)
    # 2막: 돌아누운 뒤 A 위(뚫림), B 아래(막힘)
    lab(im, '뻥 뚫려', (xA-150, yA-260), LG, t, T_SWAP+SWAP*0.6)
    lab(im, '막혔어', (xB, yB+120), LT, t, T_SWAP+SWAP*0.6+0.9)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/one_nostril_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('onenostril', s1, S1, s2, S2, out,
              preview=[(s1, int(2.2*F), S1), (s2, int(3.5*F), S2), (s2, int(6.0*F), S2), (s2, int(13.0*F), S2)])
