"""appa say(영어) 영상 공용 도구: 영어 음성(Kokoro TTS, 내려받는 모델) + 한 장면 + 영어 문장 카드.
준비(한 번): pip install --break-system-packages kokoro-onnx soundfile
  모델은 setup()이 /home/claude/tts 에 GitHub 릴리스에서 내려받는다(huggingface는 막혀 있음).
목소리: 아빠 am_michael, 엄마 af_heart. 천천히 한 번(speed 0.8) → 보통 속도로 한 번(1.0).
"""
import os, subprocess, shutil, math
import numpy as np, wave
from PIL import Image, ImageDraw, ImageFont

W = H = 1080; F = 24
TTS_DIR = '/home/claude/tts'
REL = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
FEN = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 92, index=1)
FKO = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 44, index=1)
FTI = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc', 52, index=1)
TXT = (96, 92, 110); SUB = (130, 126, 142)
DAD = 'am_michael'; MOM = 'af_heart'
SR = 24000
_k = None


def setup():
    os.makedirs(TTS_DIR, exist_ok=True)
    for f in ('kokoro-v1.0.int8.onnx', 'voices-v1.0.bin'):
        p = f'{TTS_DIR}/{f}'
        if not os.path.exists(p) or os.path.getsize(p) < 1e6:
            subprocess.run(['curl', '-sL', '-o', p, REL+f], check=True)


def tts(text, voice=DAD, speed=1.0):
    global _k
    if _k is None:
        setup()
        from kokoro_onnx import Kokoro
        _k = Kokoro(f'{TTS_DIR}/kokoro-v1.0.int8.onnx', f'{TTS_DIR}/voices-v1.0.bin')
    s, sr = _k.create(text, voice=voice, speed=speed, lang='en-us')
    assert sr == SR
    return np.asarray(s, dtype=np.float32)


def timeline(clips, total):
    """clips: [(start_sec, samples)] → 전체 오디오(-1~1), 끝 0.3초 페이드."""
    y = np.zeros(int(total*SR)+1, dtype=np.float32)
    for t0, s in clips:
        a = int(t0*SR); b = min(len(y), a+len(s)); y[a:b] += s[:b-a]
    peak = np.abs(y).max() or 1; y = y/peak*0.8
    n = int(0.3*SR); y[-n:] *= np.linspace(1, 0, n)
    return y


def write_wav(path, y):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1)*32767).astype('<i2').tobytes())


def ease(t): t = max(0, min(1, t)); return 0.5-0.5*math.cos(math.pi*t)


def card(im, en, ko, cy, a_en, a_ko, col=(140, 160, 210)):
    """영어 문장(크게, 흰 카드) + 한국어 뜻(작게, 아래). a_* 는 0~1 불투명도."""
    if a_en <= 0: return
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(en, font=FEN); A = int(255*a_en)
    d.rounded_rectangle([W/2-w/2-46, cy-78, W/2+w/2+46, cy+78], radius=78, fill=(255, 255, 255, A), outline=col+(A,), width=7)
    d.text((W/2, cy), en, font=FEN, fill=TXT+(A,), anchor='mm')
    if a_ko > 0:
        B = int(255*a_ko); wk = d.textlength(ko, font=FKO)
        d.rounded_rectangle([W/2-wk/2-26, cy+100, W/2+wk/2+26, cy+164], radius=32, fill=(255, 255, 255, int(B*0.85)))
        d.text((W/2, cy+132), ko, font=FKO, fill=SUB+(B,), anchor='mm')
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def speak_mark(d, x, y, t, on, off):
    """말하는 사람 옆 작은 소리 물결(말하는 동안만)."""
    if not (on <= t <= off): return
    for j in range(3):
        r = 18+j*16+6*math.sin((t-on)*8-j)
        d.arc([x-r, y-r, x+r, y+r], -40, 40, fill=(232, 150, 120), width=6)


def build(name, scene, total, clips, out, preview=None, preview_times=(1.5, 4.5, 8.0, None)):
    """scene(t)->Image(1080). clips: [(start, samples)]. 720x720 24fps H.264 + AAC."""
    tmp = f'/tmp/claude-0/say_{name}'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    N = int(total*F)
    for i in range(N): scene(i/F).save(f'{tmp}/{i:04d}.png')
    write_wav(f'{tmp}/a.wav', timeline(clips, total))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(F), '-i', f'{tmp}/%04d.png', '-i', f'{tmp}/a.wav',
                    '-vf', 'scale=720:720,setsar=1,format=yuv420p', '-c:v', 'libx264', '-crf', '24',
                    '-c:a', 'aac', '-b:a', '64k', '-shortest', '-movflags', '+faststart', out], check=True)
    if preview:
        ts = [x if x is not None else total-0.5 for x in preview_times]
        c = Image.new('RGB', (1080, 1080))
        for j, tt in enumerate(ts[:4]): c.paste(scene(tt).resize((540, 540)), ((j % 2)*540, (j//2)*540))
        c.save(preview)
    print(out, round(total, 2), 's')
