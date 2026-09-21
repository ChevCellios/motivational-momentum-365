from pathlib import Path
from math import sin,cos,pi
import subprocess,tempfile,shutil
from PIL import Image,ImageDraw,ImageFilter,ImageChops

ROOT=Path(__file__).resolve().parents[1]; W,H,N=960,540,160
base=Image.open(ROOT/'assets/signal/base.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
def frame(i):
 t=i/20; phase=2*pi*t/8
 out=base.copy(); light=Image.new('RGB',(W,H));d=ImageDraw.Draw(light)
 # Beacon pulses across the dark sky in a continuous, looping signal.
 for n in range(4):
  r=42+n*105+(t*86)%105
  alpha=(1-(r%105)/105)**2
  box=(480-r,257-r*.52,480+r,257+r*.52)
  d.ellipse(box,outline=(int(34*alpha),int(185*alpha),int(220*alpha)),width=1)
 for n in range(60):
  x=(n*79+i*17)%W; y=(n*43+i*29)%H
  if 190<y<430: d.point((x,y),fill=(18,55,65))
 pulse=.55+.45*sin(phase)
 d.ellipse((475,249,485,265),fill=(int(100*pulse),int(230*pulse),255))
 d.rectangle((477,316,483,378),fill=(int(30*pulse),int(170*pulse),int(210*pulse)))
 for n in range(14):
  a=phase+n*2*pi/14; x=480+118*cos(a);y=406+32*sin(a)
  d.ellipse((x-1,y-1,x+1,y+1),fill=(20,90,105))
 return ImageChops.add(ImageChops.add(out,light.filter(ImageFilter.GaussianBlur(4))),light)
def main():
 (ROOT/'assets/signal').mkdir(exist_ok=True)
 frame(42).save(ROOT/'assets/signal/poster.jpg',quality=94)
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp)
  for i in range(N):frame(i).save(p/f'{i:04d}.png')
  subprocess.run([shutil.which('ffmpeg'),' -hide_banner'.strip(),'-loglevel','error','-framerate','20','-i',str(p/'%04d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3','-loop','0','-y',str(ROOT/'signal.gif')],check=True)
if __name__=='__main__':main()
