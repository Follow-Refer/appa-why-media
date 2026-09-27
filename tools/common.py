from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess, shutil
W=H=1080
FB=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc',54,index=1)
FS=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',36,index=1)
FL=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc',150,index=1)
BG=(240,238,246); TXT=(96,92,110); GREEN=(160,200,170); GREEN_D=(130,176,146)
YEL=(246,214,140); RED=(232,150,120); BLUE=(140,160,210); SKY=(214,232,244); BROWN=(186,160,140)
def ease(t): t=max(0,min(1,t)); return 0.5-0.5*math.cos(math.pi*t)
def mix(a,b,t): return tuple(int(x+(y-x)*t) for x,y in zip(a,b))
def title(d,t): d.text((W/2,80),t,font=FB,fill=TXT,anchor='mm')
def pill(d,text,xy,col=(255,255,255),outline=None):
    w=d.textlength(text,font=FS); x,y=xy
    d.rounded_rectangle([x-w/2-22,y-30,x+w/2+22,y+30],radius=30,fill=col,outline=outline,width=4 if outline else 0)
    d.text((x,y),text,font=FS,fill=TXT,anchor='mm')
def render(name, scenes, out):
    """scenes: list of (nframes, fn(i,n)->Image)"""
    tmp=f'/tmp/claude-0/fr_{name}'; shutil.rmtree(tmp,ignore_errors=True)
    parts=[]
    for k,(n,fn) in enumerate(scenes):
        dd=f'{tmp}/{k}'; os.makedirs(dd)
        for i in range(n): fn(i,n).save(f'{dd}/{i:03d}.png')
        parts.append((dd,n))
    (d0,n0),(d1,n1)=parts
    off=n0/24-0.6
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','24','-i',f'{d0}/%03d.png','-framerate','24','-i',f'{d1}/%03d.png',
      '-filter_complex',f'[0:v]scale=720:720,setsar=1[a];[1:v]scale=720:720,setsar=1[b];[a][b]xfade=transition=fade:duration=0.6:offset={off},format=yuv420p[v]',
      '-map','[v]','-c:v','libx264','-crf','24','-movflags','+faststart',out],check=True)
    return tmp
