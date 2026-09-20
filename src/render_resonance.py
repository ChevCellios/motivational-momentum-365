"""Render Resonance: programmatic light waves from an AI-created scene."""
from pathlib import Path
from math import sin, cos, pi
import shutil, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,N=960,540,20,160
CX,CY=480,350
base=Image.open(ROOT/'assets/resonance/base.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)

def frame(index):
    t=index/FPS
    out=base.copy()
    light=Image.new('RGB',(W,H));d=ImageDraw.Draw(light)
    # Waves complete exact cycles in eight seconds for a seamless loop.
    for ring in range(6):
        p=(t*.72-ring/6)%1
        r=18+p*300
        alpha=(1-p)**2
        color=(int(35*alpha),int(175*alpha),int(225*alpha))
        d.ellipse((CX-r,CY-r*.20,CX+r,CY+r*.20),outline=color,width=max(1,round(2*alpha)))
    # A vertical pulse is synchronised to the rings, forming an audio-like equalizer.
    for x in range(286,675,13):
        wave=(sin(t*4.52+(x-286)*.09)+1)/2
        h=8+wave*34
        d.rounded_rectangle((x,CY-h,x+5,CY),radius=2,fill=(int(26+22*wave),int(110+105*wave),int(130+110*wave)))
    # Two gentle energy paths run through the board toward the emitter.
    for sx,sy,phase in ((180,446,0),(785,445,pi)):
        q=(t/2+phase/pi)%1
        x=sx+(CX-sx)*q;y=sy+(CY-sy)*q
        d.ellipse((x-2,y-2,x+2,y+2),fill=(40,180,215))
    core=.6+.4*sin(t*4.52)**2
    d.ellipse((CX-5,CY-5,CX+5,CY+5),fill=(int(80*core),int(215*core),int(255*core)))
    for n,(x,y) in enumerate(((305,394),(348,418),(611,420),(695,393),(758,457))):
        brightness=.25+.75*max(0,sin(t*4.52+n*1.6))**4
        channels=[0,0,0];channels[n%3]=int(180*brightness)
        d.rectangle((x-2,y-1,x+2,y+1),fill=tuple(channels))
    return ImageChops.add(ImageChops.add(out,light.filter(ImageFilter.GaussianBlur(5))),light)

def main():
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg:raise SystemExit('FFmpeg is required.')
    (ROOT/'assets/resonance').mkdir(parents=True,exist_ok=True)
    frame(40).save(ROOT/'assets/resonance/poster.jpg',quality=95)
    with tempfile.TemporaryDirectory() as folder:
        folder=Path(folder)
        for i in range(N):frame(i).save(folder/f'{i:04d}.png')
        subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle','-loop','0','-y',str(ROOT/'resonance.gif')],check=True)
    print('Saved resonance.gif')
if __name__=='__main__':main()
