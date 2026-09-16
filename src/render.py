"""Procedural animation with Python and Pillow. Run: python src/render.py.

The base illustration is AI-generated. This script animates the rotor,
closed energy flow, core, gadgets and RGB bricks. The characters remain still.
The image-generation prompt is not included in the public project.
"""
from pathlib import Path
from math import sin, cos, pi
import argparse
import random
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[1]
W, H, FPS, N = 960, 540, 20, 120
TAU = 2 * pi
CX, CY = 480, 209

base = Image.open(ROOT / 'assets/scene.png').convert('RGB').resize((W, H), Image.Resampling.LANCZOS)
# Lift shadows and midtones while preserving highlight detail.
# Keep the original illustration unchanged; apply grading during rendering.
tone_curve = [round(255 * (value / 255) ** 0.68) for value in range(256)]
base = base.point(tone_curve * 3)
# Extract the textured rotor from the stationary outer housing.
R = 155
rotor = base.crop((CX-R, CY-R, CX+R, CY+R))
mask = Image.new('L', rotor.size)
md = ImageDraw.Draw(mask)
md.ellipse((4, 4, R*2-4, R*2-4), fill=255)
md.ellipse((44, 44, R*2-44, R*2-44), fill=0)
mask = mask.filter(ImageFilter.GaussianBlur(1.3))
rng = random.Random(365)
bricks = [(176,24,17,4), (239,54,13,5), (745,26,14,6),
          (790,26,17,5), (717,65,15,5), (273,39,19,5),
          (671,93,13,5), (216,19,16,5), (700,16,13,4)]
phases = [rng.random()*TAU for _ in bricks]

def frame(index):
    t = TAU * index / N
    out = base.copy()
    moving = rotor.rotate(-index*360/N, Image.Resampling.BICUBIC)
    out.paste(moving, (CX-R, CY-R), mask)
    light = Image.new('RGB', (W,H))
    d = ImageDraw.Draw(light)
    # Three light particles follow the same closed figure-eight path.
    def infinity(a):
        return (CX+86*cos(a)/(1+sin(a)**2), CY+86*sin(a)*cos(a)/(1+sin(a)**2))
    for k in range(3):
        for j in range(65):
            a = t+k*TAU/3-j*.008
            x,y = infinity(a)
            brightness = (1-j/65)**1.7
            color = tuple(int(c*brightness) for c in (90,211,238))
            radius = 1.1 if j else 2.1
            d.ellipse((x-radius,y-radius,x+radius,y+radius), fill=color)
    # Circular energy flow along the inner rim of the machine.
    for k in range(4):
        angle = t+k*pi/2
        for j in range(24):
            a=angle-j*.009
            x,y=CX+106*cos(a),CY+106*sin(a)
            b=(1-j/24)*.8
            d.ellipse((x-1,y-1,x+1,y+1),fill=tuple(int(c*b) for c in (60,210,240)))
    pulse = .5+.5*sin(t*2)
    d.ellipse((CX-3,CY-3,CX+3,CY+3),fill=(int(100+90*pulse),int(140+100*pulse),220))
    for (x,y,w,h), phase in zip(bricks,phases):
        intensity = .15+.85*((1+cos(t+phase))/2)**3
        channels = [max(0,cos(t+phase-c*TAU/3))**2 for c in range(3)]
        color=tuple(int(245*intensity*v) for v in channels)
        d.rounded_rectangle((x,y,x+w,y+h),radius=1,fill=color)
    # Gentle gadget pulses without abrupt flashes.
    for x,y,phase in [(190,314,0),(761,353,2),(843,170,4)]:
        b=.4+.3*sin(t+phase)
        d.ellipse((x-2,y-2,x+2,y+2),fill=(int(20*b),int(150*b),int(220*b)))
    bloom = light.filter(ImageFilter.GaussianBlur(5))
    out = ImageChops.add(out,bloom,scale=1,offset=0)
    out = ImageChops.add(out,light,scale=1,offset=0)
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames',type=Path,help='Optional PNG frame directory for FFmpeg')
    args=parser.parse_args()
    if args.frames:
        args.frames.mkdir(parents=True,exist_ok=True)
        for i in range(N):
            frame(i).save(args.frames/f'{i:04d}.png')
        print(f'Saved {N} frames to {args.frames}')
        return
    frames=[frame(i) for i in range(N)]
    # A shared palette keeps colors stable throughout the loop.
    sheet=Image.new('RGB',(W*3,H*2))
    for n,i in enumerate(range(0,N,20)):
        sheet.paste(frames[i],((n%3)*W,(n//3)*H))
    palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    dest=ROOT/'perpetuum.gif'
    indexed[0].save(dest,save_all=True,append_images=indexed[1:],duration=50,loop=0,optimize=True,disposal=1)
    # FFmpeg reduces file size without changing frame count or duration.
    ffmpeg = shutil.which('ffmpeg')
    if ffmpeg:
        with tempfile.TemporaryDirectory() as temp:
            optimized = Path(temp) / 'optimized.gif'
            subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-i',str(dest),
                '-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle',
                '-loop','0','-y',str(optimized)],check=True)
            shutil.copyfile(optimized,dest)
    frames[0].save(ROOT/'assets/poster.jpg',quality=94)
    print(f'Saved: {dest} ({dest.stat().st_size/1024/1024:.2f} MB)')

if __name__=='__main__':
    main()
