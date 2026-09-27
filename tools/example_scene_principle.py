from PIL import Image, ImageDraw, ImageFont
import math
W=H=1080; N=168
fB=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc',54,index=1)
fS=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',36,index=1)
BG=(240,238,246); ROAD=(218,212,204); TXT=(96,92,110)
TREE=(160,200,170); MOON=(255,244,205); CAR=(246,214,140)
LT=(232,150,120); LM=(140,160,210)
TX,TY=540,640   # tree near the road
RY=820          # road center
def pill(d,text,xy,col):
    w=d.textlength(text,font=fS); x,y=xy
    d.rounded_rectangle([x-w/2-22,y-30,x+w/2+22,y+30],radius=30,fill=(255,255,255),outline=col,width=4)
    d.text((x,y),text,font=fS,fill=TXT,anchor='mm')
def dashed(d,p,q,col,w=6,dash=22,gap=14):
    L=math.dist(p,q); n=int(L//(dash+gap))+1
    for k in range(n):
        a=k*(dash+gap)/L; b=min(1,(k*(dash+gap)+dash)/L)
        d.line([p[0]+(q[0]-p[0])*a,p[1]+(q[1]-p[1])*a,p[0]+(q[0]-p[0])*b,p[1]+(q[1]-p[1])*b],fill=col,width=w)
for i in range(N):
    t=min(1,i/(N-36))                      # move, then hold ~1.5s
    cx=220+(860-220)*(0.5-0.5*math.cos(math.pi*t))
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((W/2,70),'위에서 내려다보면',font=fB,fill=TXT,anchor='mm')
    # road
    d.rectangle([0,RY-70,W,RY+70],fill=ROAD)
    for k in range(10): d.rectangle([k*120+20,RY-4,k*120+80,RY+4],fill=(250,248,240))
    # moon direction: far away, sight line always straight up
    d.ellipse([W/2-60,150,W/2+60,270],fill=MOON,outline=(236,222,180),width=3)
    pill(d,'달은 여기보다 훨씬훨씬 멀리',(W/2,315),LM)
    dashed(d,(cx,RY-30),(cx,380),LM)
    # 지나온 자리의 시선을 흐리게 남겨서 '방향 변화'가 보이게
    for j in range(0,i,20):
        tj=min(1,j/(N-36)); px=220+(860-220)*(0.5-0.5*math.cos(math.pi*tj))
        d.line([px,RY-30,px,380],fill=(214,220,238),width=4)
        d.line([px,RY-30,TX,TY],fill=(244,214,200),width=4)
        d.ellipse([px-8,RY-38,px+8,RY-22],fill=(236,222,190))
    # tree (top view: circle)
    d.ellipse([TX-55,TY-55,TX+55,TY+55],fill=TREE,outline=(140,184,152),width=4)
    dashed(d,(cx,RY-30),(TX,TY),LT)
    # car (top view)
    d.rounded_rectangle([cx-70,RY-40,cx+70,RY+40],radius=22,fill=CAR)
    d.rounded_rectangle([cx-30,RY-30,cx+40,RY+30],radius=12,fill=(214,232,244))
    # angle readout: tree direction in degrees from straight up
    ang=math.degrees(math.atan2(TX-cx,(RY-30)-TY))
    pill(d,'나무 쪽: 휙 돌아감',(250,560),LT)
    pill(d,'달 쪽: 늘 똑같은 방향',(820,500),LM)
    # small compass-like dial for tree line vs moon line near car
    im.save(f't{i:03d}.png')
