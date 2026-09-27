from common import *
FN=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',36,index=1)
FT=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26,index=1)
F=24
BODY=(150,130,110); WING=(206,186,150)
def caption(im,text,xy,alpha):
    if alpha<=0: return
    layer=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    w=d.textlength(text,font=FN); x,y=xy; x=min(max(x,w/2+40),W-w/2-40); a=int(255*alpha)
    d.rounded_rectangle([x-w/2-26,y-36,x+w/2+26,y+36],radius=36,fill=(255,255,255,a))
    d.text((x,y),text,font=FN,fill=TXT+(a,),anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB'))
def waves(d,cx,cy,k,col,a0,a1,n=3,step=40):
    for j in range(n):
        r=40+j*step+(k%14)*3
        d.arc([cx-r,cy-r,cx+r,cy+r],a0,a1,fill=col,width=7)
def cricket(d,cx,cy,s,wing_up=0):
    d.ellipse([cx-70*s,cy-26*s,cx+55*s,cy+26*s],fill=BODY)
    d.ellipse([cx+45*s,cy-24*s,cx+95*s,cy+20*s],fill=BODY)
    d.ellipse([cx+70*s,cy-10*s,cx+80*s,cy],fill=(90,80,70))
    lift=wing_up*8*s
    d.polygon([(cx-60*s,cy-16*s-lift),(cx+45*s,cy-22*s-lift),(cx+35*s,cy-2*s),(cx-70*s,cy+2*s)],fill=WING)
    for a in [(-45,22,-80,70),(0,22,-12,64),(35,20,60,58)]:
        d.line([cx+a[0]*s,cy+a[1]*s,cx+a[2]*s,cy+a[3]*s],fill=BODY,width=int(7*s))
    d.line([cx+88*s,cy-18*s,cx+175*s,cy-85*s],fill=BODY,width=int(3*s))
    d.line([cx+85*s,cy-20*s,cx+185*s,cy-50*s],fill=BODY,width=int(3*s))
def s1(i,n):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix((200,206,230),(236,230,242),y/H))
    d.ellipse([850,110,930,190],fill=(255,248,222))
    title(d,'귀뚤귀뚤, 어디서 나는 소리일까?')
    d.rectangle([0,800,W,H],fill=(196,220,196))
    import random; rnd=random.Random(2)
    for k in range(50):
        x=rnd.randint(0,W); h=rnd.randint(60,150)
        d.line([x,800,x+rnd.randint(-20,20),800-h],fill=(172,206,178),width=8)
    t=i/F
    cricket(d,470,700,2.6,wing_up=(1 if (i//4)%2 else 0) if t>2 else 0)
    if t>2 and (i//6)%2==0: waves(d,430,640,i,(150,160,210),-150,-30)
    if t>3.5: caption(im,'귀뚜라미는 입이 아니라 날개로 노래해',(540,960),min(1,(t-3.5)/0.8))
    return im
seg=[('a',3*F),('ah',2*F),('b',3*F),('bh',1*F),('c',3*F),('ch',2*F),('d',3*F),('end',4*F)]
N2=sum(n for _,n in seg)
def state(i):
    acc=0
    for nm,n in seg:
        if i<acc+n: return nm,(i-acc)/n,acc
        acc+=n
    return 'end',1,acc
CAPS={'a':'날개 한쪽엔 빗처럼 오돌토돌한 줄이 있어','b':'다른 날개 끝으로 싹싹 비비면','c':"톡톡톡 떨리면서 '귀뚤귀뚤' 소리가 나",'d':'그 소리는 다리로 들어*'}
GROUP={'a':'a','ah':'a','b':'b','bh':'b','c':'c','ch':'c','d':'d','end':'d'}
def starts():
    acc=0; st={}
    for nm,n in seg: st[nm]=acc; acc+=n
    return st
ST=starts()
def s2(i,n):
    nm,t,_=state(i); g=GROUP[nm]
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    title(d,'다리를 크게 보면' if g=='d' else '날개를 크게 보면')
    order=['a','b','c','d']; gi=order.index(g)
    if g in ('a','b','c'):
        # 아래 날개 (빗살 줄)
        d.rounded_rectangle([120,420,960,560],radius=50,fill=(226,210,180))
        teeth_t = ease(t) if nm=='a' else 1
        cnt=int(36*teeth_t)
        for k in range(cnt):
            x=160+k*22; d.polygon([(x,420),(x+11,388),(x+22,420)],fill=(186,160,140))
        # 위 날개 (긁개)
        if gi>=1:
            if nm=='b': tt=t
            elif nm in ('bh',): tt=1
            else: tt=(i-ST['c'])/(5*F)
            sx=180+int((0.5-0.5*math.cos(2*math.pi*tt*2))*680)
            d.rounded_rectangle([sx-110,230,sx+110,360],radius=40,fill=(240,228,204))
            d.polygon([(sx-14,360),(sx+14,360),(sx,392)],fill=(160,140,120))
            if gi>=2:
                if (i//4)%2==0:
                    d.line([sx-40,395,sx-60,410],fill=RED,width=5); d.line([sx+40,395,sx+60,410],fill=RED,width=5)
                waves(d,sx,300,i,(150,160,210),-150,-30,n=3,step=45)
    else:
        # 앞다리와 귀
        d.line([380,300,520,560],fill=BODY,width=40)
        d.line([520,560,470,760],fill=BODY,width=32)
        glow=0.5+0.5*math.sin(i/3)
        d.ellipse([430,380,500,450],fill=mix((255,248,222),(250,210,190),glow),outline=RED,width=6)
        waves(d,465,415,i,(150,160,210),150,210,n=3,step=50)
        d.text((W/2,1045),"*다리에 있는 얇은 막을 '고막'이라고 해요",font=FT,fill=(140,136,150),anchor='mm')
    loc=(i-ST[g])/F; alpha=min(1,loc/0.8)
    nxt={'a':'b','b':'c','c':'d','d':None}[g]
    if nxt: alpha=min(alpha,max(0,(ST[nxt]-i)/(0.5*F)))
    caption(im,CAPS[g],(540,860 if g!='d' else 900),alpha)
    return im
render('cricket2',[(8*F,s1),(N2,s2)],'/home/claude/work/cricket_silent.mp4')
from PIL import Image as I
fr=[s1(120,8*F)]+[s2(k,N2) for k in (90,170,330)]
c=I.new('RGB',(1080,1080))
for j,f in enumerate(fr): c.paste(f.resize((540,540)),((j%2)*540,(j//2)*540))
c.save('cr2.png')
