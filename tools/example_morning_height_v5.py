"""나 아침엔 더 커?(11/7): 상황(잠자리 문틀 키 재기, '아침엔 여기 넘었는데!') → 답(블록 사이 스펀지 쿠션: 낮엔 꾹꾹 납작, 밤엔 통통 → 옆의 아이도 같은 박자로 작아졌다 커짐).
사용: python3 example_morning_height_v5.py out.mp4 [preview.png]"""
import sys, math
sys.path.insert(0, '/home/claude/appa-why-media/tools')
import vid
from vid import *

FBW = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 58, index=1)
FLB = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
LT = (232, 150, 120); LM = (140, 160, 210); LG = (130, 176, 146)
BG = (240, 238, 246); WALL = (236, 230, 242); FLOOR = (214, 204, 186)
FRAME = (214, 190, 160); FRAME_D = (190, 164, 132)
SHIRT = (246, 200, 150); PANTS = (150, 170, 210); HAIR = (120, 96, 82)
SPONGE = (246, 214, 140); SPONGE_D = (226, 190, 110); WATER = (130, 176, 230)
BLOCKS = [(246, 176, 166), (170, 214, 180), (160, 190, 230), (226, 186, 226), (250, 206, 150)]
DAY_T, DAY_B = (196, 220, 244), (236, 240, 246); NIGHT_T, NIGHT_B = (90, 100, 150), (150, 150, 196)


def lab(im, text, xy, col, t, t_on, t_off=None):
    """흰 알약 라벨, 색 테두리. 0.5초 페이드."""
    a = min(1, max(0, (t-t_on)/0.5))
    if t_off is not None: a = min(a, max(0, (t_off-t)/0.4))
    if a <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FLB); x, y = xy; x = min(max(x, w/2+50), W-w/2-50); A = int(255*a)
    d.rounded_rectangle([x-w/2-30, y-40, x+w/2+30, y+40], radius=40, fill=(255, 255, 255, A), outline=col+(A,), width=6)
    d.text((x, y), text, font=FLB, fill=TXT+(A,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def kid(d, cx, gy, s, grow, mood='smile'):
    """서 있는 아이. grow(px)만큼 몸통(등)이 길어짐 — 팔다리는 그대로."""
    leg = 150*s; torso = 190*s + grow; head = 78*s
    hip = gy-leg; sh = hip-torso
    for dx in (-34*s, 34*s):
        d.rounded_rectangle([cx+dx-24*s, hip-10*s, cx+dx+24*s, gy], radius=int(22*s), fill=PANTS)
        d.ellipse([cx+dx-30*s, gy-20*s, cx+dx+30*s, gy+8*s], fill=SKIN)
    d.rounded_rectangle([cx-80*s, sh, cx+80*s, hip+20*s], radius=int(50*s), fill=SHIRT)
    for dx in (-1, 1):   # 짧은 팔, 몸 옆에 붙임
        d.rounded_rectangle([cx+dx*80*s-(22*s if dx > 0 else 22*s), sh+20*s, cx+dx*80*s+22*s, sh+150*s], radius=int(22*s), fill=SHIRT)
        d.ellipse([cx+dx*80*s-20*s, sh+138*s, cx+dx*80*s+20*s, sh+176*s], fill=SKIN)
    hy = sh-head+6*s
    d.ellipse([cx-head, hy-head, cx+head, hy+head], fill=SKIN)
    d.chord([cx-head-2, hy-head-6*s, cx+head+2, hy+30*s], 180, 360, fill=HAIR)
    for ex in (cx-30*s, cx+30*s): d.ellipse([ex-8*s, hy+4*s, ex+8*s, hy+20*s], fill=INK)
    if mood == 'wow': d.ellipse([cx-14*s, hy+34*s, cx+14*s, hy+60*s], fill=(214, 120, 124))
    else: d.arc([cx-20*s, hy+30*s, cx+20*s, hy+56*s], 20, 160, fill=LIP, width=max(3, int(5*s)))
    return hy-head   # 머리 꼭대기 y


# ---------------- 장면 1: 잠자리 전 문틀 키 재기 ----------------
MH1 = int(4.5*F)
def mh_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), WALL); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '아빠, 나 아침엔 더 커?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 900, W, H], fill=FLOOR)
    d.rectangle([600, 160, 650, 900], fill=FRAME); d.rectangle([600, 160, 612, 900], fill=FRAME_D)
    d.rectangle([650, 160, 1080, 900], fill=(226, 220, 236))
    # 창밖 달(밤)
    d.rounded_rectangle([50, 190, 290, 380], radius=30, fill=NIGHT_B)
    d.ellipse([190, 220, 260, 290], fill=(250, 236, 180)); d.ellipse([210, 212, 272, 278], fill=NIGHT_B)
    top = kid(d, 500, 900, 1.0, 0)
    # 문틀의 선: 아침에 그은 선(위) / 지금(아래)
    ym = top-26
    d.line([612, ym, 700, ym], fill=LT, width=8)
    d.text((712, ym), '아침', font=FS, fill=LT, anchor='lm')
    k = ease((t-1.0)/0.8)
    if k > 0:
        d.line([612, top+2, 612+88*k, top+2], fill=LM, width=8)
        d.text((712, top+30), '밤', font=FS, fill=mix((226, 220, 236), LM, k), anchor='lm')
    for j in range(2):
        a = ease((t-2.2-j*0.4)/0.4)
        if a > 0: d.text((400+j*0-j*40, top+10-j*70-a*14), '?', font=FBW, fill=mix(WALL, LT, a), anchor='mm')
    return im


# ---------------- 장면 2: 블록 탑의 스펀지 쿠션 + 같은 박자로 아이 키 ----------------
def squash(t):
    """0=통통(아침), 1=납작(저녁). 낮 1.0~4.5s 눌림 → 밤 6.0~9.0s 다시 통통."""
    if t < 1.0: return 0.0
    if t < 4.5: return ease((t-1.0)/3.5)
    if t < 6.0: return 1.0
    return 1-ease((t-6.0)/3.0)

def sky(t):
    if t < 4.6: return 0.0
    if t < 5.6: return ease((t-4.6)/1.0)
    if t < 9.4: return 1.0
    return 1-ease((t-9.4)/1.0)

MH2 = int(13.5*F)
def mh_s2(i, n):
    t = i/F; q = squash(t); nk = sky(t)
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    tt, bb = mix(DAY_T, NIGHT_T, nk), mix(DAY_B, NIGHT_B, nk)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=mix(tt, bb, yy/H))
    d.text((W/2, 80), '등 속 쿠션', font=FBW, fill=mix(TXT, (240, 236, 250), nk), anchor='mm')
    # 해 / 달
    sa = 1-nk
    if sa > 0: d.ellipse([880, 150, 980, 250], fill=mix(tt, (255, 220, 140), sa))
    if nk > 0:
        d.ellipse([880, 150, 960, 230], fill=mix(tt, (250, 236, 180), nk)); d.ellipse([904, 140, 974, 214], fill=tt)
    d.rectangle([0, 920, W, H], fill=FLOOR)
    # 왼쪽: 블록 5개 + 사이 스펀지 4개
    bx, gy = 290, 920; bw, bh = 240, 84
    sp_full, sp_flat = 58, 18
    sp = sp_full + (sp_flat-sp_full)*q
    y = gy
    tops = []
    for k in range(5):
        d.rounded_rectangle([bx-bw/2, y-bh, bx+bw/2, y], radius=22, fill=BLOCKS[k]); y -= bh
        if k < 4:
            wide = 1+0.10*q
            d.rounded_rectangle([bx-bw/2*0.86*wide, y-sp, bx+bw/2*0.86*wide, y], radius=int(min(26, sp/2)), fill=SPONGE, outline=SPONGE_D, width=4)
            for h in range(4):   # 스펀지 구멍
                hx = bx-70+h*46; d.ellipse([hx-6, y-sp/2-4*(1-q)-3, hx+6, y-sp/2+4*(1-q)+3], fill=SPONGE_D)
            tops.append(y-sp/2); y -= sp
    top_y = y
    # 낮: 위에서 손바닥이 꾹 누름 (화면 위쪽 밖에서 내려오는 짧은 소매)
    pa = 0.0
    if 0.6 < t < 5.0: pa = ease((t-0.6)/0.4)*(1-ease((t-4.6)/0.4))
    if pa > 0:
        py = top_y - 10 - (1-pa)*260
        d.rounded_rectangle([bx-60, py-200, bx+60, py-70], radius=40, fill=(170, 196, 170))
        d.rounded_rectangle([bx-110, py-90, bx+110, py], radius=44, fill=(240, 210, 184))
    # 물방울: 낮엔 스펀지에서 빠져나감, 밤엔 다시 들어감
    for k, sy in enumerate(tops):
        for j in range(2):
            if 1.4 < t < 4.6:
                ph = ((t-1.4)*0.9 + j*0.5 + k*0.17) % 1
                x = bx + (1 if j == 0 else -1)*(bw/2*0.9 + ph*60); yy = sy + ph*30
                d.ellipse([x-9, yy-12, x+9, yy+12], fill=mix(tt, WATER, 1-ph))
            elif 6.0 < t < 9.0:
                ph = ((t-6.0)*0.9 + j*0.5 + k*0.17) % 1
                x = bx + (1 if j == 0 else -1)*(bw/2*0.9 + (1-ph)*60); yy = sy + (1-ph)*30
                d.ellipse([x-9, yy-12, x+9, yy+12], fill=mix(tt, WATER, ph))
    # 오른쪽: 같은 박자로 키가 줄었다 늘었다 (몸통만, 크게 과장)
    kx = 760
    top = kid(d, kx, 920, 1.0, 40*(1-q), mood='wow' if t > 9.6 else 'smile')
    ref = 920 - (150+190+40) - 2*78 + 6 + 0   # 아침(통통) 때 머리 꼭대기
    d.line([kx-150, ref, kx+150, ref], fill=(255, 255, 255), width=6)
    for xx in range(int(kx-150), int(kx+150), 36): d.line([xx, ref, xx+18, ref], fill=LT, width=6)
    lab(im, '낮: 꾹꾹', (bx, 1000), LT, t, 1.4, 5.0)
    lab(im, '밤: 통통', (bx, 1000), LM, t, 6.2, 9.6)
    lab(im, '아침: 쑥!', (kx, ref-120), LG, t, 9.8)
    return im


if __name__ == '__main__':
    out = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/morning_preview.png'
    vid.preview_path = lambda name: pv
    vid.build('morning', mh_s1, MH1, mh_s2, MH2, out,
              preview=[(mh_s1, int(3.2*F), MH1), (mh_s2, int(3.5*F), MH2), (mh_s2, int(8.0*F), MH2), (mh_s2, int(12.5*F), MH2)])
