# ⚡ Motivational Momentum 365

[![Teleportation — a desktop computer dissolves into light and reappears on another platform](teleportation.gif)](https://chevcellios.github.io/motivational-momentum-365/)

![Language](https://img.shields.io/badge/language-English-green)
![Animation](https://img.shields.io/badge/animation-GIF-blueviolet)
![Code](https://img.shields.io/badge/code-Python-orange)
![Duration](https://img.shields.io/badge/loop-8%20seconds-00b8c4)
![Resolution](https://img.shields.io/badge/resolution-960%20%C3%97%20540-blue)

Motivational Momentum 365 is a collection of motivational visual experiments combining artificial intelligence, programming and creative expression. One idea. One creation. Keep moving.

## 🔗 Explore the animations

- [002 — Teleportation](https://chevcellios.github.io/motivational-momentum-365/)
- [001 — Perpetuum](https://chevcellios.github.io/motivational-momentum-365/perpetuum.html)
- [Open the latest GIF](teleportation.gif)
- [Teleportation source code](src/render_teleportation.py)

The latest GIF appears directly below the repository title. Autoplay on GitHub depends on each viewer's motion preferences. The standalone pages start immediately and include pause controls.

## 🌀 Latest creation — Teleportation

> Your next breakthrough is closer than you think.

A desktop computer stands on a transfer platform. A scanning field breaks it into luminous fragments, carries them across the laboratory and reconstructs the same computer on the opposite platform. The sequence then reverses, completing an eight-second loop.

Teleportation is a fictional visual concept. The computer's disappearance, reconstruction, particle paths, reflections and portal indicators are animated through code. The researchers in the background remain still.

## ✨ Features

- photorealistic cyberpunk laboratory with two transfer platforms
- an isolated desktop computer, monitor and keyboard
- progressive disintegration and reconstruction using pixel masks
- curved particle paths carrying light between the portals
- contact shadows and subtle reflections that follow the transfer
- rotating portal lights and RGB wall indicators
- clear lighting and visible hardware details
- a seamless eight-second loop at 20 frames per second
- English documentation and a responsive website
- the first creation, Perpetuum, remains available

## 🎨 How it is made

1. AI tools generate the laboratory and a separate computer with a transparent background.
2. Python places the computer on a platform and calculates a staggered scan mask.
3. Pillow and NumPy animate disappearance, reconstruction, particles and lighting for each frame.
4. FFmpeg, when available, exports an optimized looping GIF; Pillow provides a fallback.
5. GitHub Markdown displays the GIF, while the standalone page provides playback controls.

## 🗂️ Previous creation — Perpetuum

[![Perpetuum — the first visual experiment](assets/poster.jpg)](https://chevcellios.github.io/motivational-momentum-365/perpetuum.html)

> Every ending sets a new beginning in motion.

Two researchers observe an imagined perpetual motion machine. The rotor turns, energy follows a closed figure-eight path and RGB bricks change color. The six-second animation is preserved as [perpetuum.gif](perpetuum.gif), with its [original rendering script](src/render.py).

## 🔒 Creative process

Finished artwork, source assets and animation code are included. Image-generation prompts and private working notes are not shared.

## ⚙️ Technologies

- Python, Pillow and NumPy — procedural animation and frame compositing
- FFmpeg — optional GIF optimization
- HTML, CSS and JavaScript — standalone pages
- GitHub Markdown and GitHub Pages — presentation and hosting

The animation tools are free and open source. Rebuilding either animation from the included assets requires no paid service or API key. The source illustrations were previously created using an AI tool.

## 🚀 Run locally

Open `index.html` in a browser to watch Teleportation, or `perpetuum.html` to watch Perpetuum.

To rebuild the animations, use a Python version compatible with the pinned dependencies:

```sh
python -m pip install -r requirements.txt
python src/render_teleportation.py
```

To rebuild the first creation:

```sh
python src/render.py
```

FFmpeg is detected automatically when installed and available on your system PATH. Without it, Pillow exports the GIF; the resulting file may be larger.

## 📁 Project structure

```text
motivational-momentum-365/
├── README.md
├── index.html
├── perpetuum.html
├── teleportation.gif
├── perpetuum.gif
├── requirements.txt
├── assets/
│   ├── scene.png
│   ├── poster.jpg
│   └── teleportation/
│       ├── laboratory.png
│       ├── computer.png
│       └── poster.jpg
└── src/
    ├── render.py
    └── render_teleportation.py
```

## 🗺️ Future creations

- new motivational visuals and animations
- further experiments with movement, transformation and light
- a growing collection of daily creative ideas

## 🤝 Feedback

Suggestions and bug reports are welcome through [GitHub Issues](https://github.com/ChevCellios/motivational-momentum-365/issues).

## 📬 Contact

- GitHub: [ChevCellios](https://github.com/ChevCellios)
- Project: [Motivational Momentum 365](https://github.com/ChevCellios/motivational-momentum-365)
