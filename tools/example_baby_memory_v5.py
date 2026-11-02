"""아기 때 기억(10/14): 상황(아기 사진 보며 '기억 안 나!') → 답(세 살 기억 9개: 여섯 살엔 6개, 아홉 살엔 3개. 녹음하면 폰에 남음)."""
from v5_answer import *
BG = (236, 232, 246); BED = (214, 204, 232)
MEM = [(246, 170, 160), (250, 206, 130), (160, 200, 230), (170, 214, 170), (226, 176, 220),
       (250, 186, 120), (150, 190, 214), (240, 160, 190), (190, 200, 150)]

def icon(d, x, y, r, k):
    c = (255, 255, 255); s = r*0.45
    if k % 3 == 0:    # 하트
        d.ellipse([x-s, y-s*0.7, x, y+s*0.2], fill=c); d.ellipse([x, y-s*0.7, x+s, y+s*0.2], fill=c)
        d.polygon([(x-s*0.95, y-s*0.1), (x+s*0.95, y-s*0.1), (x, y+s*0.9)], fill=c)
    elif k % 3 == 1:  # 별
        pts = [(x+math.cos(-math.pi/2+j*math.pi/5)*(s if j % 2 == 0 else s*0.45), y+math.sin(-math.pi/2+j*math.pi/5)*(s if j % 2 == 0 else s*0.45)) for j in range(10)]
        d.polygon(pts, fill=c)
    else:             # 케이크
        d.rectangle([x-s, y-s*0.1, x+s, y+s*0.8], fill=c); d.line([x, y-s*0.1, x, y-s*0.8], fill=c, width=max(3, int(r*0.12)))

def bubble_m(d, x, y, r, k):
    d.ellipse([x-r, y-r, x+r, y+r], fill=MEM[k]); icon(d, x, y, r, k)

def baby(d, cx, cy, s=1.0):
    d.ellipse([cx-70*s, cy-70*s, cx+70*s, cy+70*s], fill=SKIN)
    d.ellipse([cx-30*s, cy-8*s, cx-18*s, cy+4*s], fill=INK); d.ellipse([cx+18*s, cy-8*s, cx+30*s, cy+4*s], fill=INK)
    d.arc([cx-16*s, cy+16*s, cx+16*s, cy+36*s], 20, 160, fill=LIP, width=int(5*s))
    d.ellipse([cx-8*s, cy-82*s, cx+8*s, cy-62*s], fill=(150, 120, 100))

ME1 = int(5.5*F)
def me_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '아기 때 기억이 하나도 안 나!', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=BED)
    # 아기 사진 액자
    px, py = 700, 470
    d.rounded_rectangle([px-170, py-190, px+170, py+190], radius=20, fill=(255, 252, 244))
    d.rounded_rectangle([px-140, py-160, px+140, py+130], radius=10, fill=(214, 228, 240))
    baby(d, px, py-20, 1.2)
    kid(d, 300, 900, s=1.0)
    for k in range(3):   # 물음표
        a = ease((t-1.2-k*0.35)/0.4)
        if a > 0: d.text((300+(k-1)*70, 470-k*25-a*20), '?', font=FBW, fill=mix(BG, LM, a), anchor='mm')
    lab(im, '이게 나야?', (300, 380), LT, t, 2.6)
    return im

COLS = [(220, '세 살'), (540, '여섯 살'), (860, '아홉 살')]
KEEP6 = {0, 1, 2, 4, 6, 7}       # 6/9 ≈ 63~72%
KEEP9 = {1, 4, 7}                # 3/9 ≈ 35%
def grid(cx, k):
    r, c = divmod(k, 3); return cx+(c-1)*82, 300+r*82

ME2 = int(13*F)
def me_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '세 살 때 기억, 크면 어떻게 될까?', font=FBW, fill=TXT, anchor='mm')
    for j, (cx, name) in enumerate(COLS):
        d.text((cx, 190), name, font=FS, fill=TXT, anchor='mm')
        kid(d, cx, 980, s=0.62+0.14*j)
    # 세 살: 기억 9개
    for k in range(9):
        a = ease((t-0.2-k*0.08)/0.3)
        if a > 0: bubble_m(d, *grid(220, k), 34*a, k)
    # 여섯 살: 9개가 건너왔다가 3개가 날아감
    k6 = ease((t-1.6)/0.8); f6 = ease((t-3.0)/1.0)
    for k in range(9):
        if k6 <= 0: break
        x, y = grid(540, k)
        if k in KEEP6: bubble_m(d, x, y, 34*k6, k)
        elif f6 < 1:
            d = blend(im, lambda dd: (dd.ellipse([x-34, y-34-f6*120, x+34, y+34-f6*120], fill=MEM[k]+(int(255*(1-f6)),))))
    lab(im, '꽤 남아', (540, 610), LG, t, 3.8)
    # 아홉 살: 6개에서 3개가 더 날아감
    k9 = ease((t-5.0)/0.8); f9 = ease((t-6.2)/1.0)
    for k in range(9):
        if k9 <= 0 or k not in KEEP6: continue
        x, y = grid(860, k)
        if k in KEEP9: bubble_m(d, x, y, 34*k9, k)
        elif f9 < 1:
            d = blend(im, lambda dd: (dd.ellipse([x-34, y-34-f9*120, x+34, y+34-f9*120], fill=MEM[k]+(int(255*(1-f9)),))))
    lab(im, '3개 중 1개쯤', (860, 610), LT, t, 7.0)
    # 9초~: 여섯 살 때 폰에 녹음 → 폰 속에 6개가 그대로
    kp = ease((t-8.6)/0.6)
    if kp > 0:
        d = blend(im, lambda dd: dd.rectangle([0, 140, W, H], fill=BG+(int(225*kp),)))
        if kp > 0.6:
            px, py = 540, 520
            d.rounded_rectangle([px-150, py-250, px+150, py+250], radius=40, fill=(80, 84, 104))
            d.rounded_rectangle([px-128, py-224, px+128, py+224], radius=26, fill=(252, 248, 240))
            d.ellipse([px-26, py+150, px+26, py+202], fill=(232, 110, 110))   # 녹음 버튼
            kin = ease((t-9.2)/1.0)
            for m, k in enumerate(sorted(KEEP6)):
                r_, c_ = divmod(m, 2); tx, ty = px-62+c_*124, py-150+r_*100
                sx, sy = grid(540, k)
                x, y = sx+(tx-sx)*kin, sy+(ty-sy)*kin
                bubble_m(d, x, y, 40, k)
            lab(im, '오늘 밤 녹음하면, 그대로!', (540, 880), LT, t, 10.4)
    return im

if __name__ == '__main__':
    build('memory', me_s1, ME1, me_s2, ME2, sys.argv[1],
          preview=[(me_s1, int(4*F), ME1), (me_s2, int(4.6*F), ME2), (me_s2, int(8.2*F), ME2), (me_s2, int(12*F), ME2)])
