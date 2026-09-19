"""Beyond the Horizon: a procedural orbital beacon over an AI-created skyline.
Run: python src/render_horizon.py. Requires Pillow, NumPy and FFmpeg on PATH.
The original background is shared with Emergence. No private prompts included.
"""
from pathlib import Path
from math import sin, cos, pi
import tempfile, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,N=960,540,20,200
BASE=Image.open(ROOT/'assets/emergence/rooftop.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
TAU=2*pi

def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def position(t):
    if t<2.2:
        u=smooth(t/2.2)
        return (480,373-190*u)
    if t<7.8:
        a=-pi/2+TAU*smooth((t-2.2)/5.6)
        return (480+178*cos(a),231+48*sin(a))
    u=smooth((t-7.8)/2.2)
    return (480,183+190*u)

def frame(i):
    t=i/FPS;phase=TAU*t/10
    activation=sin(pi*t/10)**2
    out=BASE.copy()
    light=Image.new('RGB',(W,H));d=ImageDraw.Draw(light)
    def line(points,color,width=1):d.line(points,fill=color,width=width)
    # Three evolving launch-pad rings; integer cycle counts close the loop.
    for n in range(3):
        r=17+n*9+sin(phase+n)*2
        points=[(480+r*cos(a*TAU/120),373+r*.27*sin(a*TAU/120)) for a in range(121)]
        line(points,(12,70+int(65*activation),90),1)
    # Thin projection lines rise from a physical socket on the motherboard.
    for dx in (-92,92):
        line([(480,373),(480+dx,249)],(3,int(22*activation),int(29*activation)),1)
    # Tilted spherical navigation globe with longitudinal and latitude arcs.
    for meridian in range(6):
        a=meridian*pi/6+phase*.5
        points=[]
        for j in range(81):
            b=-pi/2+j*pi/80
            x=78*cos(b)*cos(a); y=78*sin(b);z=78*cos(b)*sin(a)
            points.append((480+x,232+y*.85+z*.32))
        line(points,(int(8*activation),int(62*activation),int(73*activation)),1)
    for latitude in (-.66,-.33,0,.33,.66):
        r=78*(1-latitude**2)**.5
        points=[(480+r*cos(j*TAU/100),232+latitude*66+r*.32*sin(j*TAU/100)) for j in range(101)]
        line(points,(int(8*activation),int(55*activation),int(70*activation)),1)
    orbit=[(480+178*cos(j*TAU/180),231+48*sin(j*TAU/180)) for j in range(181)]
    line(orbit,(int(20*activation),int(110*activation),int(140*activation)),1)
    for n in range(36):
        a=n*TAU/36
        x,y=480+178*cos(a),231+48*sin(a)
        line([(x,y),(x+cos(a)*4,y+sin(a)*3)],(int(25*activation),int(105*activation),int(130*activation)))
    # A finite trail follows the same periodic path; no discontinuity at wrap.
    for n in range(75,0,-1):
        p=position((t-n*.012)%10)
        q=position((t-(n-1)*.012)%10)
        b=(1-n/76)**2
        line([p,q],(int(110*b),int(220*b),int(245*b)),2)
    x,y=position(t)
    # Metallic diamond-shaped probe with small articulated solar wings.
    wing=5+2*sin(phase)**2
    d.polygon([(x-4,y),(x,y-8),(x+4,y),(x,y+8)],fill=(180,222,225))
    d.polygon([(x,y-8),(x+4,y),(x,y+8)],fill=(62,121,144))
    d.polygon([(x-4,y-2),(x-wing-6,y-5),(x-wing-6,y+3),(x-4,y+3)],fill=(35,130,160))
    d.polygon([(x+4,y-2),(x+wing+6,y-5),(x+wing+6,y+3),(x+4,y+3)],fill=(35,130,160))
    d.ellipse((x-1,y-1,x+1,y+1),fill=(240,235,185))
    # Traveling impulses and gradually shifting RGB status lights.
    for n,(sx,sy) in enumerate([(286,444),(670,439),(481,460)]):
        u=(t/2.5+n/3)%1
        px=sx+(480-sx)*u;py=sy+(373-sy)*u
        d.ellipse((px-1,py-1,px+1,py+1),fill=(35,110,135))
    for n,(bx,by) in enumerate([(338,358),(320,442),(558,414),(760,395)]):
        color=tuple(int(80*max(0,sin(phase+n-c*TAU/3))) for c in range(3))
        d.rectangle((bx-2,by-1,bx+2,by+1),fill=color)
    return ImageChops.add(ImageChops.add(out,light.filter(ImageFilter.GaussianBlur(5))),light)

def main():
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg:raise SystemExit('Install FFmpeg and add it to PATH before rendering.')
    (ROOT/'assets/horizon').mkdir(parents=True,exist_ok=True)
    frame(92).save(ROOT/'assets/horizon/poster.jpg',quality=95)
    with tempfile.TemporaryDirectory() as folder:
        folder=Path(folder)
        for i in range(N):frame(i).save(folder/f'{i:04d}.png')
        subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.png'),
            '-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
            '-loop','0','-y',str(ROOT/'horizon.gif')],check=True)
    print('Saved horizon.gif and assets/horizon/poster.jpg')

if __name__=='__main__':main()
