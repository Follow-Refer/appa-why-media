import sys, math, os, shutil, subprocess
sys.path.insert(0, '/home/claude/appa-why-media/tools')
from common import *
import numpy as np, wave
F = 24
FN = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 38, index=1)
FT = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 26, index=1)
FNM = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
SKIN = (250, 226, 200); INK = (110, 104, 126); LIP = (226, 150, 140)

def caption(im, text, xy, alpha):
    if alpha <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=FN); x, y = xy; x = min(max(x, w/2+40), W-w/2-40); a = int(255*alpha)
    d.rounded_rectangle([x-w/2-26, y-36, x+w/2+26, y+36], radius=36, fill=(255, 255, 255, a))
    d.text((x, y), text, font=FN, fill=TXT+(a,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))

def footnote(d, text):
    d.text((W/2, 1045), text, font=FT, fill=(140, 136, 150), anchor='mm')

class Seq:
    """seg: [(name, seconds)] → state(i) = (name, t_in_seg_sec, start_frame)"""
    def __init__(self, seg):
        self.seg = [(n, int(s*F)) for n, s in seg]; self.N = sum(n for _, n in self.seg)
        self.ST = {}; acc = 0
        for nm, n in self.seg: self.ST[nm] = acc; acc += n
        self.order = [n for n, _ in self.seg]
    def state(self, i):
        acc = 0
        for nm, n in self.seg:
            if i < acc+n: return nm, (i-acc)/F
            acc += n
        return self.order[-1], self.seg[-1][1]/F
    def cap_alpha(self, i, nm):
        t = (i-self.ST[nm])/F; a = min(1, t/0.8)
        k = self.order.index(nm)
        if k+1 < len(self.order):
            nxt = self.order[k+1]; a = min(a, max(0, (self.ST[nxt]-i)/(0.5*F)))
        return a

def env(sr, n, a=0.05, r=0.2):
    e = np.ones(n); na = max(1, int(sr*a)); nr = max(1, int(sr*r))
    e[:na] = np.linspace(0, 1, na); e[-nr:] = np.linspace(1, 0, nr); return e

def write_wav(path, y, sr=44100):
    y = np.clip(y, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype('<i2').tobytes())

def build(name, s1, n1, s2, n2, out, sounds=None, preview=None):
    """sounds: fn(total_seconds, sr) -> np.array or None. preview: list of (scene_fn, frame, n) saved as 2x2."""
    tmp = f'/tmp/claude-0/fr_{name}'; shutil.rmtree(tmp, ignore_errors=True)
    for k, (n, fn) in enumerate([(n1, s1), (n2, s2)]):
        dd = f'{tmp}/{k}'; os.makedirs(dd)
        for i in range(n): fn(i, n).save(f'{dd}/{i:03d}.png')
    off = n1/F - 1.0; total = n1/F + n2/F - 1.0
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{tmp}/0/%03d.png', '-framerate', '24', '-i', f'{tmp}/1/%03d.png']
    fc = f'[0:v]scale=720:720,setsar=1[a];[1:v]scale=720:720,setsar=1[b];[a][b]xfade=transition=fade:duration=1.0:offset={off},format=yuv420p[v]'
    maps = ['-map', '[v]']
    if sounds:
        sr = 44100; y = sounds(total, sr); write_wav(f'{tmp}/a.wav', y, sr)
        cmd += ['-i', f'{tmp}/a.wav']; maps += ['-map', '2:a', '-c:a', 'aac', '-b:a', '64k', '-shortest']
    cmd += ['-filter_complex', fc] + maps + ['-c:v', 'libx264', '-crf', '24', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    if preview:
        c = Image.new('RGB', (1080, 1080))
        for j, (fn, i, n) in enumerate(preview[:4]): c.paste(fn(i, n).resize((540, 540)), ((j % 2)*540, (j//2)*540))
        c.save(preview_path(name))
    print(out, total, 's')

def preview_path(name):
    return f'/tmp/claude-0/-home-claude-appa-why-media/bc34e63d-c70f-528b-9801-e509676f70f6/scratchpad/{name}_preview.png'
