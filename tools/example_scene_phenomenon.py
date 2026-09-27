from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
W=H=1080; N=192
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
fB=ImageFont.truetype(F,54,index=1)  # KR
fS=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',38,index=1)
SKY=(28,34,64); STAR=(255,255,255)
random.seed(3)
stars=[(random.randint(0,W),random.randint(40,560),random.choice([2,2,3])) for _ in range(70)]
# base layers
bg=Image.new('RGB',(W,H),SKY); d=ImageDraw.Draw(bg)
for y in range(H):  # gradient
    t=y/H; c=tuple(int(a+(b-a)*t) for a,b in zip((196,208,232),(236,230,242))); d.line([(0,y),(W,y)],fill=c)
for x,y,r in stars: d.ellipse([x-r,y-r,x+r,y+r],fill=STAR)
# moon with glow
MX,MY=790,230
mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).ellipse([MX-130,MY-130,MX+130,MY+130],fill=140)
mask=mask.filter(ImageFilter.GaussianBlur(45))
bg.paste(Image.new('RGB',(W,H),(255,250,232)),(0,0),mask); d=ImageDraw.Draw(bg)
d.ellipse([MX-78,MY-78,MX+78,MY+78],fill=(255,248,222))
for cx,cy,r in [(-25,-15,16),(22,20,12),(10,-35,8)]: d.ellipse([MX+cx-r,MY+cy-r,MX+cx+r,MY+cy+r],fill=(242,232,200))
def mountains(off):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); m=ImageDraw.Draw(im)
    P=720
    for k in range(-1,3):
        b=k*P-off
        pts=[(b,760),(b+120,560),(b+260,700),(b+400,520),(b+560,690),(b+720,760)]
        m.polygon(pts+[(b+720,800),(b,800)],fill=(176,190,219))
    m.rectangle([0,760,W,800],fill=(176,190,219))
    return im
def trees(off):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); t=ImageDraw.Draw(im)
    S=360
    for k in range(-1,5):
        x=k*S-off%S+60
        t.rectangle([x-12,780,x+12,880],fill=(186,160,140))
        t.ellipse([x-80,610,x+80,800],fill=(160,200,170))
        t.ellipse([x-55,580,x+55,700],fill=(178,214,186))
    return im
def car(fr):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); c=ImageDraw.Draw(im)
    x0,y0=330,860; bob=2*math.sin(fr*0.9)
    c.rounded_rectangle([x0,y0-70+bob,x0+420,y0+40+bob],radius=34,fill=(246,214,140))
    c.rounded_rectangle([x0+80,y0-140+bob,x0+320,y0-50+bob],radius=36,fill=(246,214,140))
    c.rounded_rectangle([x0+105,y0-122+bob,x0+190,y0-62+bob],radius=14,fill=(214,232,244))
    c.rounded_rectangle([x0+210,y0-122+bob,x0+298,y0-62+bob],radius=14,fill=(214,232,244))
    # kid face in back window looking at moon
    c.ellipse([x0+228,y0-112+bob,x0+272,y0-68+bob],fill=(255,220,190))
    for wx in (x0+95,x0+325):
        c.ellipse([wx-44,y0-4,wx+44,y0+84],fill=(130,126,140)); c.ellipse([wx-20,y0+20,wx+20,y0+60],fill=(220,218,226))
        a=-fr*0.6
        c.line([wx,y0+40,wx+20*math.cos(a),y0+40+20*math.sin(a)],fill=(120,118,130),width=6)
    return im
def label(img,text,xy,col):
    d=ImageDraw.Draw(img); w=d.textlength(text,font=fS); x,y=xy
    d.rounded_rectangle([x-w/2-22,y-30,x+w/2+22,y+32],radius=30,fill=col)
    d.text((x,y),text,font=fS,fill=(90,88,100),anchor='mm')
frames=[]
for i in range(N):
    im=bg.copy().convert('RGBA')
    im.alpha_composite(mountains((i*720//N)%720))
    ImageDraw.Draw(im).rectangle([0,880,W,H],fill=(214,208,200))
    for k in range(-1,12):  # road dashes fast
        x=k*120-(i*24*240//N)%120; ImageDraw.Draw(im).rectangle([x,985,x+60,995],fill=(250,248,240))
    im.alpha_composite(trees(i*1920*3//N))
    im.alpha_composite(car(i))
    label(im,'달: 그대로',(MX,MY+135),(255,255,255))
    label(im,'산: 천천히',(170,500),(255,255,255))
    label(im,'나무: 휙휙',(900,560),(255,255,255))
    d=ImageDraw.Draw(im); d.text((W/2,80),'왜 달만 따라올까?',font=fB,fill=(96,92,110),anchor='mm')
    frames.append(im.convert('RGB'))
for i,f in enumerate(frames): f.save(f'f{i:03d}.png')
