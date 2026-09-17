"""Render a looping computer teleportation with Python, Pillow and NumPy.

The background and transparent computer are AI-generated artwork.
All motion, disintegration, reconstruction and lighting are procedural.
Private image-generation prompts are not included.
Run from any directory: python src/render_teleportation.py
FFmpeg is optional and recommended for smaller GIF files.
"""
from pathlib import Path
from math import sin, cos, pi
import argparse
import shutil
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'teleportation'
WIDTH, HEIGHT, FPS, FRAME_COUNT = 960, 540, 20, 160
CENTERS = (241, 719)
GROUND = 352
background = Image.open(ASSETS/'laboratory.png').convert('RGB').resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
computer = Image.open(ASSETS/'computer.png').convert('RGBA')
# Ignore near-transparent edge noise when aligning the hardware to the pad.
computer = computer.crop(computer.getchannel('A').point(lambda a:255 if a>10 else 0).getbbox())
computer.thumbnail((285,200),Image.Resampling.LANCZOS)
CW, CH = computer.size
pixels = np.asarray(computer).copy()
original_alpha = pixels[:,:,3].astype(np.float32)
rng = np.random.default_rng(36502)
blocks = rng.random(((CH+5)//6,(CW+5)//6))
noise = np.repeat(np.repeat(blocks,6,axis=0),6,axis=1)[:CH,:CW]
vertical = np.arange(CH,dtype=np.float32)[:,None]/max(1,CH-1)
threshold = .10+.80*(.68*vertical+.32*noise)
opaque = np.argwhere(original_alpha>200)
sample_points = opaque[rng.integers(0,len(opaque),220)]
particles = [(float(x),float(y),float(rng.random()),float(rng.uniform(-1,1))) for y,x in sample_points]

def clamp(v):
    return max(0.0,min(1.0,v))

def materialize(amount):
    """Scan and rebuild the silhouette with staggered pixel blocks."""
    if amount<=0:
        return Image.new('RGBA',computer.size)
    if amount>=1:
        return computer.copy()
    opacity = np.clip((amount-threshold)/.035+.5,0,1)
    edge = np.exp(-((amount-threshold)/.025)**2)*.8
    data = pixels.copy()
    data[:,:,:3] = np.clip(data[:,:,:3].astype(np.float32)+edge[:,:,None]*np.array([12,135,170]),0,255).astype(np.uint8)
    data[:,:,3] = np.round(original_alpha*opacity).astype(np.uint8)
    return Image.fromarray(data)

def frame(index):
    t=index/FPS
    half=int(t//4)%2
    u=t%4
    source,dest=half,1-half
    departure=clamp((u-.65)/1.15)
    arrival=clamp((u-1.5)/1.1)
    visibility=[0.0,0.0]
    visibility[source]=1-departure
    visibility[dest]=arrival
    out=background.convert('RGBA')
    # A subtle contact shadow anchors the hardware to each platform.
    shadow=Image.new('RGBA',(WIDTH,HEIGHT))
    sd=ImageDraw.Draw(shadow)
    for x,v in zip(CENTERS,visibility):
        sd.ellipse((x-131,GROUND-13,x+131,GROUND+4),fill=(0,5,8,round(115*v)))
    out=Image.alpha_composite(out,shadow.filter(ImageFilter.GaussianBlur(5)))
    for x,v in zip(CENTERS,visibility):
        layer=materialize(v)
        out.alpha_composite(layer,(x-CW//2,GROUND-CH))
        # A low-opacity reflection moves with the object and its scan mask.
        reflection=layer.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((CW,42),Image.Resampling.BILINEAR)
        alpha=np.asarray(reflection.getchannel('A'),dtype=np.float32)
        alpha*=np.linspace(.11,0,42)[:,None]
        reflection.putalpha(Image.fromarray(alpha.astype(np.uint8)))
        out.alpha_composite(reflection,(x-CW//2,GROUND+57))
    light=Image.new('RGB',(WIDTH,HEIGHT))
    d=ImageDraw.Draw(light)
    # Portal rim indicators rotate continuously and close exactly after 8s.
    for k,cx in enumerate(CENTERS):
        for j in range(3):
            angle=2*pi*(t/8)+j*2*pi/3+k*pi
            x=cx+128*cos(angle);y=193+126*sin(angle)
            d.ellipse((x-2,y-2,x+2,y+2),fill=(35,133,152))
        v=visibility[k]
        if 0<v<1:
            scan_y=GROUND-CH+CH*clamp((v-.1)/.8)
            d.line((cx-CW*.46,scan_y,cx+CW*.46,scan_y),fill=(70,190,210),width=1)
    # Particles carry the computer's sampled colors along curved trajectories.
    for px,py,offset,sway in particles:
        start=.68+offset*.68
        q=(u-start)/1.18
        if not 0<q<1:
            continue
        ease=q*q*(3-2*q)
        x=CENTERS[source]+px-CW/2+(CENTERS[dest]-CENTERS[source])*ease
        y=GROUND-CH+py-(78+35*sway)*sin(pi*q)
        x+=sin(pi*q)*sway*23
        fade=sin(pi*q)**.55
        radius=1.0+offset*1.1
        color=(round(70*fade),round((165+offset*75)*fade),round(245*fade))
        d.rectangle((x-radius,y-radius,x+radius,y+radius),fill=color)
    # RGB indicators are part of the generated wall; animate them gently.
    for n,(x,y) in enumerate([(108,55),(108,68),(108,80),(369,65),(369,78),(595,68),(831,67)]):
        b=.15+.22*(1+sin(2*pi*t/8+n*1.7))
        color=[0,0,0];color[n%3]=int(190*b)
        d.rectangle((x-2,y-2,x+2,y+2),fill=tuple(color))
    out=out.convert('RGB')
    out=ImageChops.add(out,light.filter(ImageFilter.GaussianBlur(4)))
    return ImageChops.add(out,light)

def render():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true',help='Only save the poster and contact sheet')
    args=parser.parse_args()
    frame(0).save(ASSETS/'poster.jpg',quality=95)
    if args.preview:
        sheet=Image.new('RGB',(960,810))
        for n,i in enumerate([0,26,43,67,106,130]):
            shot=frame(i).resize((480,270),Image.Resampling.LANCZOS)
            sheet.paste(shot,((n%2)*480,(n//2)*270))
        sheet.save(ASSETS/'preview.jpg',quality=94)
        return
    ffmpeg=shutil.which('ffmpeg')
    dest=ROOT/'teleportation.gif'
    if ffmpeg:
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            for i in range(FRAME_COUNT):
                frame(i).save(folder/f'{i:04d}.png')
            subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-framerate',str(FPS),
                '-i',str(folder/'%04d.png'),'-filter_complex',
                '[0:v]split[a][b];[a]palettegen=max_colors=224:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle',
                '-loop','0','-y',str(dest)],check=True)
    else:
        frames=[frame(i) for i in range(FRAME_COUNT)]
        sheet=Image.new('RGB',(WIDTH*4,HEIGHT*2))
        for n,i in enumerate(range(0,FRAME_COUNT,20)):
            sheet.paste(frames[i],((n%4)*WIDTH,(n//4)*HEIGHT))
        palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
        indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
        indexed[0].save(dest,save_all=True,append_images=indexed[1:],duration=50,loop=0,optimize=True,disposal=1)
    print(f'Saved {dest} ({dest.stat().st_size/1024/1024:.2f} MB)')

if __name__=='__main__':
    render()
