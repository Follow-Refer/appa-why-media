"""여왕벌(주간 1편): 상황(그림책 속 큰 여왕벌, '왜 혼자만 커?') → 답(같은 알 두 개, 처음엔 같은 밥 → 한쪽은 여왕 밥 계속, 한쪽은 꿀·꽃가루 밥 → 여왕벌/일벌)."""
from v5_answer import *
BG = (246, 240, 226); WAX = (240, 206, 130); WAX_D = (214, 176, 100); CELL_IN = (252, 236, 196)
JELLY = (255, 255, 250); POLLEN = (240, 180, 70)
BODY = (246, 196, 90); STRIPE = (120, 90, 70); WING = (226, 236, 246)

def bee(d, cx, cy, s=1.0, queen=False, flap=0.0):
    L = 1.55 if queen else 1.0
    w1 = 20*s*(1+0.15*flap)
    d.ellipse([cx-46*s, cy-58*s-w1, cx+6*s, cy-6*s], fill=WING)          # 날개
    d.ellipse([cx-6*s, cy-58*s-w1, cx+46*s, cy-6*s], fill=WING)
    d.ellipse([cx-34*s, cy-30*s, cx+34*s, cy+28*s], fill=BODY)            # 가슴
    ab = 70*s*L
    d.ellipse([cx-38*s, cy+10*s, cx+38*s, cy+10*s+ab], fill=BODY)         # 배
    for k in range(1, 4):
        y = cy+10*s+ab*k/4.2
        d.line([cx-34*s, y, cx+34*s, y], fill=STRIPE, width=int(10*s))
    d.ellipse([cx-26*s, cy-70*s, cx+26*s, cy-22*s], fill=STRIPE)          # 머리
    d.ellipse([cx-14*s, cy-56*s, cx-6*s, cy-48*s], fill=(255, 255, 255)); d.ellipse([cx+6*s, cy-56*s, cx+14*s, cy-48*s], fill=(255, 255, 255))

def hexagon(d, cx, cy, r, fill, outline=None):
    pts = [(cx+r*math.cos(math.pi/6+k*math.pi/3), cy+r*math.sin(math.pi/6+k*math.pi/3)) for k in range(6)]
    d.polygon(pts, fill=fill, outline=outline)

BE1 = int(5.5*F)
def be_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (236, 232, 246)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '여왕벌은 왜 혼자만 커?', font=FBW, fill=TXT, anchor='mm')
    d.rectangle([0, 860, W, H], fill=(214, 204, 232))
    # 펼친 그림책
    d.rounded_rectangle([430, 250, 1010, 700], radius=24, fill=(255, 252, 244))
    d.line([720, 260, 720, 690], fill=(226, 216, 200), width=6)
    bee(d, 580, 470, 1.25, queen=True, flap=math.sin(t*10))
    for k, (x, y) in enumerate([(820, 360), (900, 470), (810, 580)]):
        bee(d, x, y, 0.6, flap=math.sin(t*10+k))
    kid(d, 230, 900, s=1.0)
    for k in range(3):
        a = ease((t-1.4-k*0.35)/0.4)
        if a > 0: d.text((330+k*60, 330-k*36-a*20), '?', font=FBW, fill=mix((236, 232, 246), LM, a), anchor='mm')
    return im

LX, RX, CY = 330, 750, 470
BE2 = int(15*F)
def be_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '같은 알, 다른 밥', font=FBW, fill=TXT, anchor='mm')
    # 0~2s 같은 방 두 개, 같은 알
    grow = ease((t-5.2)/1.6)                       # 왼쪽 방이 길쭉해짐(여왕 방)
    for cx, q in [(LX, True), (RX, False)]:
        if q and grow > 0:
            d.rounded_rectangle([cx-120, CY-120, cx+120, CY+120+200*grow], radius=int(110), fill=WAX)
            d.rounded_rectangle([cx-96, CY-96, cx+96, CY+96+200*grow], radius=int(90), fill=CELL_IN)
        else:
            hexagon(d, cx, CY, 130, WAX); hexagon(d, cx, CY, 104, CELL_IN)
    fo = ease((t-10.6)/1.2)
    if fo > 0: d = blend(im, lambda dd: dd.rectangle([0, 140, W, H], fill=BG+(int(200*fo),)))
    hatch = ease((t-1.2)/0.8)
    morph = ease((t-9.0)/1.4)                      # 애벌레 → 벌
    for cx, q in [(LX, True), (RX, False)]:
        cy = CY + (100*grow if q else 0)
        if morph < 1:
            a = 1-morph
            if hatch < 1:                          # 알
                d.ellipse([cx-18, cy-40, cx+18, cy+40], fill=mix(CELL_IN, (255, 255, 255), a))
            if hatch > 0:                          # 애벌레(C자)
                sz = 1 + (0.6 if q else 0.25)*ease((t-5.5)/3)
                r = 46*sz*hatch
                d.arc([cx-r, cy-r, cx+r, cy+r], 40, 320, fill=mix(CELL_IN, (226, 206, 168), a), width=int(36*sz*hatch))
                d.arc([cx-r, cy-r, cx+r, cy+r], 44, 316, fill=mix(CELL_IN, (255, 255, 255), a), width=int(26*sz*hatch))
        if morph > 0:
            out = ease((t-10.6)/1.2)          # 방에서 나와 크기 비교
            bx = cx; by = cy-10 + (CY+60-(cy-10))*out
            sc = (0.95 + (0.55 if q else 0.0)*out)*morph
            bee(d, bx, by, sc, queen=q, flap=math.sin(t*10))
    # 2~5s 같은 밥(흰 젤리) 두 쪽 모두
    def drops(cx, col, t0, t1):
        if t0 < t < t1:
            for k in range(3):
                u = ((t-t0)*0.9 + k/3) % 1
                y = CY-260+u*170
                d.ellipse([cx-14, y-14, cx+14, y+14], fill=col, outline=(220, 210, 190))
    drops(LX, JELLY, 2.2, 8.6); drops(RX, JELLY, 2.2, 5.0); drops(RX, POLLEN, 5.4, 8.6)
    for k in range(3):
        a = ease((t-2.4-k*0.8)/0.3)*(1-ease((t-5.0)/0.4))
        if a > 0: d.text((W/2, 180), f'{k+1}일째', font=FS, fill=mix(BG, TXT, a), anchor='mm')
    lab(im, '여왕 밥 계속', (LX, 880), LT, t, 5.6, 8.8)
    lab(im, '꿀·꽃가루 밥', (RX, 880), LM, t, 5.6, 8.8)
    lab(im, '여왕벌', (LX, 880), LT, t, 11.6)
    lab(im, '일벌', (RX, 880), LM, t, 11.8)
    return im

if __name__ == '__main__':
    build('bee', be_s1, BE1, be_s2, BE2, sys.argv[1],
          preview=[(be_s1, int(4*F), BE1), (be_s2, int(3.5*F), BE2), (be_s2, int(7*F), BE2), (be_s2, int(13.5*F), BE2)])
