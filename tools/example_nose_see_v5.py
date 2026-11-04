"""내 코가 보여(11/5): 상황(한쪽 눈 감은 아이 '내 코가 보여!') → 답(아이 눈에 보이는 장면: 한 눈이면 흐릿한 코 → 두 눈이면 투명 → 머리가 지워 줘)."""
from v5_answer import *
from PIL import ImageFilter
BG = (236, 232, 246); SEAT = (190, 200, 226); SEAT_D = (170, 180, 210)
NOSE = (240, 196, 172)
SK_T = (196, 214, 238); SK_B = (236, 238, 246); GRASS = (176, 210, 160)

def face(d, cx, cy, s, left_closed=False, right_closed=False):
    """정면 얼굴. left/right는 보는 사람 기준."""
    d.ellipse([cx-90*s, cy-90*s, cx+90*s, cy+90*s], fill=SKIN)
    d.chord([cx-92*s, cy-96*s, cx+92*s, cy+40*s], 180, 360, fill=(120, 96, 82))   # 머리카락
    for ex, closed in ((cx-36*s, left_closed), (cx+36*s, right_closed)):
        if closed: d.arc([ex-15*s, cy-2*s, ex+15*s, cy+20*s], 200, 340, fill=INK, width=max(3, int(6*s)))
        else: d.ellipse([ex-9*s, cy+0*s, ex+9*s, cy+18*s], fill=INK)
    d.ellipse([cx-12*s, cy+22*s, cx+12*s, cy+44*s], fill=NOSE)
    d.arc([cx-22*s, cy+46*s, cx+22*s, cy+72*s], 20, 160, fill=LIP, width=max(3, int(5*s)))

NS1 = int(5*F)
def ns_s1(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '아빠, 내 코가 보여!', font=FBW, fill=TXT, anchor='mm')
    # 차 뒷자리 좌석 + 창문
    d.rounded_rectangle([140, 230, 940, 1000], radius=80, fill=SEAT)
    d.rounded_rectangle([200, 300, 880, 560], radius=40, fill=(214, 232, 244))
    for k in range(4):                                  # 창밖 나무가 지나감
        x = (k*240 - t*160) % 900 + 160
        if 230 < x < 850:
            d.ellipse([x-46, 380, x+46, 470], fill=GREEN); d.rectangle([x-8, 470, x+8, 540], fill=BROWN)
    d.rounded_rectangle([140, 640, 940, 1000], radius=60, fill=SEAT_D)
    wink = t > 1.2
    face(d, 540, 640, 1.9, right_closed=wink)
    d.rounded_rectangle([540-150, 640+160, 540+150, 1080], radius=70, fill=(246, 200, 150))   # 몸
    for k in range(2):
        a = ease((t-1.8-k*0.4)/0.4)
        if a > 0: d.text((790+k*56, 640-k*40-a*16), '!' if k == 0 else '?', font=FBW, fill=mix(SEAT, LT, a), anchor='mm')
    return im

# 아이 눈에 보이는 장면
VX0, VY0, VX1, VY1 = 90, 170, 990, 900
def view_scene():
    v = Image.new('RGB', (VX1-VX0, VY1-VY0)); d = ImageDraw.Draw(v)
    vw, vh = v.size
    for y in range(vh): d.line([(0, y), (vw, y)], fill=mix(SK_T, SK_B, y/vh))
    d.rectangle([0, int(vh*0.66), vw, vh], fill=GRASS)
    d.ellipse([vw-190, 50, vw-90, 150], fill=(255, 220, 140))
    for x, s in ((170, 1.0), (430, 0.8), (690, 1.1)):
        gy = int(vh*0.68)
        d.rectangle([x-10*s, gy-120*s, x+10*s, gy], fill=BROWN)
        d.ellipse([x-80*s, gy-260*s, x+80*s, gy-100*s], fill=GREEN)
    d.rounded_rectangle([520, int(vh*0.66)-60, 640, int(vh*0.66)+10], radius=14, fill=(250, 190, 180))   # 공
    d.ellipse([350, int(vh*0.66)+40, 410, int(vh*0.66)+100], fill=(250, 214, 120))
    return v
SCENE = view_scene()

def nose_layer(side, alpha):
    """side: 'L' 오른쪽 눈만 뜰 때 코는 왼쪽에. 흐릿한 살색 덩어리."""
    vw, vh = SCENE.size
    m = Image.new('L', (vw, vh), 0); d = ImageDraw.Draw(m)
    if side == 'L': d.polygon([(-40, vh+40), (-40, vh*0.18), (vw*0.20, vh*0.42), (vw*0.34, vh+40)], fill=255)
    else: d.polygon([(vw+40, vh+40), (vw+40, vh*0.18), (vw*0.84, vh*0.45), (vw*0.70, vh+40)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(34)).point(lambda p: int(p*alpha))
    return m

MASK = Image.new('L', SCENE.size, 0); ImageDraw.Draw(MASK).rounded_rectangle([0, 0, SCENE.size[0]-1, SCENE.size[1]-1], radius=60, fill=255)
NS2 = int(13*F)
def ns_s2(i, n):
    t = i/F; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W/2, 80), '내 눈에 보이는 것', font=FBW, fill=TXT, anchor='mm')
    # 0~4s 한쪽 눈(보는 사람 기준 오른쪽 눈 감음 = 아이 왼눈 감음) → 코가 왼쪽에 흐릿하게
    # 4.5~7s 두 눈 뜨면 코가 투명해짐  / 7.5~ 머리가 지워 줘
    show = ease((t-0.4)/1.0)
    fade = ease((t-4.6)/2.2)
    a = show*(1-0.9*fade)
    v = SCENE.copy()
    nm = nose_layer('L', a)
    v.paste(Image.new('RGB', v.size, NOSE), (0, 0), nm)
    im.paste(v, (VX0, VY0), MASK); d = ImageDraw.Draw(im)
    d.rounded_rectangle([VX0, VY0, VX1, VY1], radius=60, outline=(255, 255, 255), width=10)
    # 오른쪽 아래 작은 얼굴: 지금 몇 눈으로 보는지
    both = t > 4.3
    d.ellipse([800, 800, 1040, 1040], fill=(255, 255, 255))
    face(d, 920, 910, 0.95, right_closed=not both)
    lab(im, '코: 늘 보여', (430, 600), LT, t, 1.4, 4.4)
    lab(im, '두 눈: 투명!', (330, 330), LM, t, 5.0, 8.0)
    lab(im, '머리가 지워 줘', (330, 330), LG, t, 8.4)
    return im

if __name__ == '__main__':
    build('nose', ns_s1, NS1, ns_s2, NS2, sys.argv[1],
          preview=[(ns_s1, int(3*F), NS1), (ns_s2, int(3*F), NS2), (ns_s2, int(6*F), NS2), (ns_s2, int(11*F), NS2)])
