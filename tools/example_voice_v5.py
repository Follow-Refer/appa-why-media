"""목소리(10/5): 상황(폰에서 자기 목소리 듣고 찡그림) → 답(내 귀엔 공기+뼈 두 길, 남한텐 공기 한 길)."""
from v5_answer import *
AIR = (140, 170, 220); BONE = (236, 150, 110)

def wave(d, x0, y, x1, amp, wl, col, w, ph):
    pts = [(x, y + amp*math.sin((x-x0)/wl*2*math.pi - ph)) for x in range(int(x0), int(x1), 4)]
    if len(pts) > 1: d.line(pts, fill=col, width=w)

def side_head(d, cx, cy, s=1.0, mouth_open=0.0):
    """옆얼굴(오른쪽 보는): 머리, 귀, 입. 팔다리 없음."""
    d.ellipse([cx-150*s, cy-160*s, cx+150*s, cy+150*s], fill=SKIN)
    d.chord([cx-160*s, cy-175*s, cx+150*s, cy+40*s], 180, 360, fill=(120, 96, 80))      # 머리카락
    d.ellipse([cx+60*s, cy-30*s, cx+82*s, cy-8*s], fill=INK)                              # 눈
    d.ellipse([cx-70*s, cy-20*s, cx-20*s, cy+50*s], fill=(240, 206, 180))                 # 귀
    d.ellipse([cx-55*s, cy, cx-35*s, cy+30*s], fill=(214, 170, 150))
    mo = mouth_open
    d.ellipse([cx+110*s, cy+60*s-8*s*mo, cx+140*s, cy+70*s+10*s*mo], fill=MOUTH_IN if mo > 0.2 else LIP)

VO1 = int(6.5*F)
def vo_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (238, 232, 244)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '이거 내 목소리 아니야!', font=FBW, fill=TXT, anchor='mm')
    # 폰: 오른쪽, 소리 물결이 아이 쪽으로
    px, py = 760, 520
    d.rounded_rectangle([px-90, py-170, px+90, py+170], radius=30, fill=(80, 84, 104))
    d.rounded_rectangle([px-76, py-150, px+76, py+150], radius=20, fill=(200, 214, 236))
    d.ellipse([px-30, py-60, px+30, py], fill=SKIN); d.rounded_rectangle([px-40, py+4, px+40, py+70], radius=20, fill=(180, 200, 230))
    if t > 1.0:
        for k in range(3):
            r = 60 + ((t*90 + k*60) % 180)
            d.arc([px-90-r, py-r, px-90+r, py+r], 140, 220, fill=AIR, width=8)
    kid(d, 300, 900, s=1.0)
    hy = 900-290
    if t > 2.6:   # 찡그림: 눈썹 기울기
        d.line([300-40, hy-34, 300-16, hy-26], fill=INK, width=6); d.line([300+16, hy-26, 300+40, hy-34], fill=INK, width=6)
    lab(im, '내 목소리?', (620, 820), LT, t, 2.8)
    return im

VO2 = int(11*F)
def vo_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), (238, 232, 244)); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '내 귀엔 두 길로 와', font=FBW, fill=TXT, anchor='mm')
    cx, cy = 420, 470
    talk = 0.5+0.5*math.sin(t*9)
    side_head(d, cx, cy, 1.25, talk)
    mouth = (cx+160, cy+82); ear = (cx-56, cy+18)
    # 공기 길: 입 → 밖으로 돌아 → 귀 (얇은 파랑)
    k1 = ease((t-0.6)/1.0)
    if k1 > 0:
        S=1.25
        ctrl=[mouth,(cx+250,cy+90),(cx+260,cy-120),(cx+120,cy-290),(cx-140,cy-290),(cx-260,cy-120),(cx-250,cy+60),(ear[0]-40,ear[1]+10),ear]
        def cr(p0,p1,p2,p3,u):
            return tuple(0.5*((2*p1[k])+(-p0[k]+p2[k])*u+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*u*u+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*u**3) for k in (0,1))
        cp=[ctrl[0]]+ctrl+[ctrl[-1]]
        pts=[]
        for j in range(1,len(cp)-2):
            for q in range(10): pts.append(cr(cp[j-1],cp[j],cp[j+1],cp[j+2],q/10))
        pts.append(ear)
        m = int(len(pts)*k1)
        if m > 1: d.line(pts[:m], fill=AIR, width=10)
        for q in range(3):
            u = ((t*0.5) + q/3) % 1
            if u < k1:
                x, y = pts[int(u*(len(pts)-1))]; d.ellipse([x-12, y-12, x+12, y+12], fill=AIR)
    # 뼈 길: 머리 속을 직선으로 (굵은 주황, 맥박)
    k2 = ease((t-2.6)/1.0)
    if k2 > 0:
        bx = lerp_(mouth[0]-40, ear[0]+20, k2)
        d = blend(im, lambda dd: dd.line([(mouth[0]-40, mouth[1]-10), (bx, ear[1]+6)], fill=BONE+(int(200),), width=int(22+6*talk)))
    lab(im, '공기 길', (cx+300, 190), LM, t, 1.2, 6.0)
    lab(im, '뼈 길: 굵게', (cx+40, cy+260), LT, t, 3.0, 6.0)
    # 6초~: 비교 — 내 귀(굵은 파도) vs 엄마 귀·녹음(얇은 파도)
    k3 = ease((t-6.0)/0.6)
    if k3 > 0:
        d = blend(im, lambda dd: dd.rectangle([0, 130, W, H], fill=(238, 232, 244, int(235*k3))))
        if k3 > 0.5:
            d.rounded_rectangle([90, 220, 990, 560], radius=30, fill=(252, 244, 236))
            d.rounded_rectangle([90, 620, 990, 960], radius=30, fill=(236, 242, 252))
            d.text((150, 270), '내가 듣는 내 목소리', font=FS, fill=TXT, anchor='lm')
            d.text((150, 670), '엄마·녹음이 듣는 내 목소리', font=FS, fill=TXT, anchor='lm')
            ph = t*6
            wave(d, 150, 420, 930, 70, 260, BONE, 16, ph); wave(d, 150, 420, 930, 30, 120, AIR, 6, ph*1.3)
            wave(d, 150, 820, 930, 30, 120, AIR, 8, ph*1.3)
            lab(im, '공기 + 뼈', (800, 270), LT, t, 6.6)
            lab(im, '공기만', (820, 670), LM, t, 7.4)
    return im

if __name__ == '__main__':
    build('voice', vo_s1, VO1, vo_s2, VO2, sys.argv[1], preview=[(vo_s1, int(4*F), VO1), (vo_s2, int(2*F), VO2), (vo_s2, int(4.5*F), VO2), (vo_s2, int(9*F), VO2)])
