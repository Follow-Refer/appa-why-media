from common import *
import random
random.seed(7)
FN=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',34,index=1)
FT=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26,index=1)
# big leaf, horizontal lens, stalk to the right
LX0,LX1,LY,LH=170,830,380,190
def inside(x,y):
    t=(x-(LX0+LX1)/2)/((LX1-LX0)/2)
    return abs(t)<1 and abs(y-LY)< LH*(1-t*t)
dots=[]
while len(dots)<260:
    x=random.uniform(LX0,LX1); y=random.uniform(LY-LH,LY+LH)
    if inside(x,y): dots.append((x,y,random.random()<0.45))
def leaf_outline(d):
    pts=[]
    for k in range(61):
        t=-1+2*k/60; x=(LX0+LX1)/2+t*(LX1-LX0)/2; pts.append((x,LY-LH*(1-t*t)))
    for k in range(60,-1,-1):
        t=-1+2*k/60; x=(LX0+LX1)/2+t*(LX1-LX0)/2; pts.append((x,LY+LH*(1-t*t)))
    d.polygon(pts,fill=(252,248,236),outline=(214,206,190))
    d.line([LX0+20,LY,LX1-10,LY],fill=(214,200,180),width=4)
def stalk(d,close):
    d.line([LX1-5,LY,LX1+130,LY+65],fill=BROWN,width=18)
    if close>0:
        # 잎자루 시작점에 생기는 막(문)
        a=close
        d.rounded_rectangle([LX1+14,LY-40,LX1+38,LY+60],radius=10,fill=mix((252,248,236),RED,a))
DROPS=[(620+k*38, LY-40+(k%3)*40) for k in range(5)]
def drops(d,phase,t):
    # 단물 방울: 'c' 단계에서 잎자루 쪽으로 가다가 막에 막혀 되돌아옴
    for k,(x0,y0) in enumerate(DROPS):
        if phase=='c':
            u=(t*2+k*0.15)%1
            x=x0+(LX1+10-x0)*math.sin(math.pi*u)
        else:
            x=x0
        d.ellipse([x-17,y0-20,x+17,y0+14],fill=(255,255,255),outline=(222,140,110),width=4)
    d.text((DROPS[0][0]-10,DROPS[0][1]-50),'단물',font=FN,fill=(200,120,95),anchor='mm')
STEPS=['밤이 길어지면 초록이 빠져요','그러면 숨어 있던 노랑이 보여요','잎자루에 문이 닫혀요*','갇힌 단물로 빨강을 새로 만들어요']
CAP_POS=[(540,660),(540,660),(760,640),(540,660)]
def caption(im,text,xy,alpha):
    if alpha<=0: return
    layer=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    w=d.textlength(text,font=FN); x,y=xy
    x=min(max(x,w/2+40),W-w/2-40)
    a=int(255*alpha)
    d.rounded_rectangle([x-w/2-26,y-34,x+w/2+26,y+34],radius=34,fill=(255,255,255,a))
    d.text((x,y),text,font=FN,fill=TXT+(a,),anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB'))
# timeline (frames @24fps)
F=24
seg=[('g',3*F),('hold1',2*F),('y',1*F),('hold2',2*F),('c',2*F),('hold3',2*F),('r',3*F),('end',4*F)]
def s2_state(i):
    acc=0
    for name,n in seg:
        if i<acc+n: return name,(i-acc)/n
        acc+=n
    return 'end',1
N2=sum(n for _,n in seg)
def s2(i,n):
    name,t=s2_state(i)
    order=[s for s,_ in seg]; idx=order.index(name)
    green = 1-ease(t) if name=='g' else (1 if idx<0 else 0)
    if name=='g': green=1-ease(t)
    else: green=0
    close = ease(min(1,t*3)) if name=='c' else (1 if idx>order.index('c') else 0)
    dim = 0.55 if name in ('c','hold3') else 0
    red = ease(t) if name=='r' else (1 if name=='end' else 0)
    active={'g':0,'hold1':0,'y':1,'hold2':1,'c':2,'hold3':2,'r':3,'end':3}[name]
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    title(d,'잎 속에서 일어나는 일')
    # sun
    d.ellipse([60,110,150,200],fill=YEL)
    leaf_outline(d)
    for (x,y,isred) in dots:
        r=13
        col=YEL
        if isred and red>0: col=mix(YEL,RED,red)
        if dim: col=mix(col,(252,248,236),dim)
        d.ellipse([x-r,y-r,x+r,y+r],fill=col)
        if green>0:
            g=mix((252,248,236),GREEN_D,green)
            d.ellipse([x-r-3,y-r-3,x+r+3,y+r+3],fill=g) if green>0.02 else None
    stalk(d,close)
    if name in ('c','hold3'): drops(d,'c' if name=='c' else 'hold',t)
    if idx>=order.index('c'):
        d.text((540,1045),"*잎자루 끝에 생기는 이 막을 '떨켜'라고 해요",font=FT,fill=(140,136,150),anchor='mm')
    # 한 번에 한 문장만, 그림 가까이에 부드럽게 나타났다 사라짐
    first={'g':'g','hold1':'g','y':'y','hold2':'y','c':'c','hold3':'c','r':'r','end':'r'}[name]
    acc=0; start=0
    for nm,nn in seg:
        if nm==first: start=acc; break
        acc+=nn
    local=(i-start)/F
    alpha=min(1,local/0.8)
    nxt={'g':'y','y':'c','c':'r','r':None}[first]
    if nxt:
        acc=0
        for nm,nn in seg:
            if nm==nxt: nstart=acc; break
            acc+=nn
        alpha=min(alpha,max(0,(nstart-i)/(0.5*F)))
    caption(im,STEPS[active].replace('*','*') ,CAP_POS[active],alpha)
    return im
def s1(i,n):
    t=ease(i/(5*F))
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    title(d,'여름엔 초록, 가을엔 노랑·빨강')
    d.rectangle([0,860,W,H],fill=(214,226,206))
    d.rectangle([520,560,560,870],fill=BROWN)
    d.ellipse([280,230,800,650],fill=mix((180,214,186),(236,228,200),t))
    rnd=random.Random(3)
    for k in range(40):
        x=rnd.randint(330,750); y=rnd.randint(280,600); tgt=YEL if k%2 else RED
        c=mix(GREEN_D,tgt,t); d.ellipse([x-22,y-14,x+22,y+14],fill=c)
    pill(d,'여름' if t<0.5 else '가을',(540,960))
    return im
render('leaves2',[(7*F,s1),(N2,s2)],'/home/claude/appa-why-media/media/20260927-autumn-leaves-steps.mp4')
from PIL import Image as I
fr=[s2(k,N2) for k in (60,130,230,N2-1)]
c=I.new('RGB',(1080,1080))
for j,f in enumerate(fr): c.paste(f.resize((540,540)),((j%2)*540,(j//2)*540))
c.save('lv2.png')
