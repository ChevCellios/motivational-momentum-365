"""Emergence: procedural growth, energy traces and renewal.

AI-generated source artwork is animated with Python, Pillow and NumPy.
Private generation prompts are not included. FFmpeg is optional.
Run: python src/render_emergence.py
"""
from pathlib import Path
from math import sin, cos, pi
import argparse
import shutil
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'/'emergence'
WIDTH,HEIGHT,FPS,COUNT=960,540,20,200
CX,GROUND=480,373
background=Image.open(ASSETS/'rooftop.png').convert('RGB').resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
tree=Image.open(ASSETS/'tree.png').convert('RGBA')
tree=tree.crop(tree.getchannel('A').point(lambda a:255 if a>10 else 0).getbbox())
tree.thumbnail((410,304),Image.Resampling.LANCZOS)
TW,TH=tree.size
pixels=np.array(tree)
alpha=pixels[:,:,3].astype(np.float32)
rng=np.random.default_rng(36503)
noise=rng.random(((TH+4)//5,(TW+4)//5))
noise=np.repeat(np.repeat(noise,5,axis=0),5,axis=1)[:TH,:TW]
height=1-np.arange(TH)[:,None]/max(1,TH-1)
threshold=np.clip(height*.93+noise*.07,0,1)
leaf_points=np.argwhere((alpha>200)&(pixels[:,:,1]>pixels[:,:,0])&(np.arange(TH)[:,None]<TH*.72))
if not len(leaf_points):leaf_points=np.argwhere(alpha>200)
leaves=leaf_points[rng.integers(0,len(leaf_points),90)]
phases=rng.random(len(leaves))*2*pi

def clamp(v):return max(0.,min(1.,v))
def smooth(v):
    v=clamp(v)
    return v*v*(3-2*v)

def state(t):
    growth=smooth((t-.7)/4.5)
    renewal=smooth((t-7.5)/1.8)
    if t>=9.3:return 0.,0.
    return growth,renewal

def frame(index):
    t=index/FPS
    growth,renewal=state(t)
    out=background.convert('RGBA')
    light=Image.new('RGB',(WIDTH,HEIGHT))
    d=ImageDraw.Draw(light)
    root_brightness=.55+.22*sin(2*pi*t/10)
    d.ellipse((CX-4,GROUND-3,CX+4,GROUND+3),fill=(int(60*root_brightness),int(220*root_brightness),int(240*root_brightness)))
    if growth>0:
        extent=min(1,growth*1.16)
        reveal=np.clip((extent-threshold)/.04+.5,0,1)
        if growth>=.999:reveal=np.ones_like(alpha)
        # Renewal dissolves the crown toward the trunk, returning to the seed.
        if renewal>0:
            reveal*=np.clip(((1-renewal)-threshold)/.065+.5,0,1)
        data=pixels.copy()
        data[:,:,3]=np.round(alpha*reveal).astype(np.uint8)
        sx=.12+.88*growth
        sy=.16+.84*growth
        sw,sh=max(1,round(TW*sx)),max(1,round(TH*sy))
        layer=Image.fromarray(data).resize((sw,sh),Image.Resampling.LANCZOS)
        # Tiny anchored sway adds life without moving the rooted base.
        sway=sin(2*pi*t/10)*1.8*growth
        layer=layer.transform((sw,sh),Image.Transform.AFFINE,(1,-sway/max(1,sh),sway,0,1,0),Image.Resampling.BICUBIC)
        x0=CX-sw//2;y0=GROUND-sh
        shadow=Image.new('RGBA',(WIDTH,HEIGHT))
        sd=ImageDraw.Draw(shadow)
        sd.ellipse((CX-45*growth,GROUND-5,CX+46*growth,GROUND+11),fill=(0,15,12,int(70*growth*(1-renewal))))
        out=Image.alpha_composite(out,shadow.filter(ImageFilter.GaussianBlur(8)))
        out.alpha_composite(layer,(x0,y0))
        for n,(y,x) in enumerate(leaves):
            if reveal[y,x]<.5:continue
            px=x0+x*sx;py=y0+y*sy
            sparkle=max(0,sin(2*pi*t/2+phases[n]))**12
            brightness=sparkle*growth*(1-renewal)
            if brightness>.08:
                color=(int(120*brightness),int(205*brightness),int(150*brightness))
                d.ellipse((px-1,py-1,px+1,py+1),fill=color)
        # During renewal, leaf-colored fragments rise into the morning air.
        if renewal>0:
            for n,(y,x) in enumerate(leaves):
                trigger=(1-threshold[y,x])*.72
                q=(renewal-trigger)/.28
                if not 0<q<1:continue
                px=CX-TW/2+x+sin(phases[n]+q*3)*q*17
                py=GROUND-TH+y-q*40
                fade=sin(pi*q)*.8
                color=(int(125*fade),int(230*fade),int(155*fade))
                d.rectangle((px-1,py-1,px+1,py+1),fill=color)
    # Electrical impulses travel through the motherboard toward the seed.
    tracks=[[(292,443),(337,429),(372,429),(423,397),(480,373)],
            [(664,439),(614,423),(588,423),(533,392),(480,373)],
            [(479,456),(479,421),(464,409),(480,373)]]
    for n,track in enumerate(tracks):
        for k in range(2):
            q=(t/2.5+n*.21+k*.5)%1
            f=q*(len(track)-1);i=min(len(track)-2,int(f));r=f-i
            ax,ay=track[i];bx,by=track[i+1]
            px=ax+(bx-ax)*r;py=ay+(by-ay)*r
            d.ellipse((px-1.5,py-1.5,px+1.5,py+1.5),fill=(40,135,140))
    rgb_positions=[(338,358),(320,442),(558,414),(760,395),(637,327)]
    for n,(x,y) in enumerate(rgb_positions):
        amount=.3+.3*sin(2*pi*t/10+n)
        color=[0,0,0];color[n%3]=int(180*amount)
        d.rectangle((x-2,y-1,x+2,y+1),fill=tuple(color))
    out=out.convert('RGB')
    return ImageChops.add(ImageChops.add(out,light.filter(ImageFilter.GaussianBlur(4))),light)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    frame(120).save(ASSETS/'poster.jpg',quality=95)
    if args.preview:
        sheet=Image.new('RGB',(960,810))
        for n,i in enumerate([0,45,70,100,140,172]):
            sheet.paste(frame(i).resize((480,270),Image.Resampling.LANCZOS),((n%2)*480,(n//2)*270))
        sheet.save(ASSETS/'preview.jpg',quality=95)
        return
    dest=ROOT/'emergence.gif'
    ffmpeg=shutil.which('ffmpeg')
    if ffmpeg:
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            for i in range(COUNT):frame(i).save(folder/f'{i:04d}.png')
            subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.png'),
                '-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
                '-loop','0','-y',str(dest)],check=True)
    else:
        frames=[frame(i) for i in range(COUNT)]
        sheet=Image.new('RGB',(WIDTH*4,HEIGHT*2))
        for n,i in enumerate(range(0,COUNT,25)):sheet.paste(frames[i],((n%4)*WIDTH,(n//4)*HEIGHT))
        palette=sheet.quantize(colors=256)
        indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
        indexed[0].save(dest,save_all=True,append_images=indexed[1:],duration=50,loop=0,optimize=True,disposal=1)
    print(f'Saved {dest} ({dest.stat().st_size/1024/1024:.2f} MB)')

if __name__=='__main__':main()
