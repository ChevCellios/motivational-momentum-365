# ⚡ Motivational Momentum 365

[![Perpetuum — an animated cyberpunk laboratory with human characters and RGB bricks](perpetuum.gif)](https://chevcellios.github.io/motivational-momentum-365/)

![Language](https://img.shields.io/badge/language-English-green)
![Animation](https://img.shields.io/badge/animation-GIF-blueviolet)
![Code](https://img.shields.io/badge/code-Python-orange)
![Duration](https://img.shields.io/badge/loop-6%20seconds-00b8c4)
![Resolution](https://img.shields.io/badge/resolution-960%20%C3%97%20540-blue)

Motivational Momentum 365 is a collection of motivational visual experiments combining artificial intelligence, programming and creative expression. The idea is simple: create something every day, explore a new idea and keep moving forward.

## 🔗 Explore the animation

- [Perpetuum — live page](https://chevcellios.github.io/motivational-momentum-365/)
- [Open the GIF](perpetuum.gif)
- [Animation source code](src/render.py)

The GIF appears directly below the repository title. There is no need to open the HTML source. Autoplay on GitHub depends on each viewer's motion preferences; the standalone page starts the animation immediately and includes a pause button.

## ✨ Features

- photorealistic computer-generated human characters with futuristic gadgets
- a cyberpunk laboratory with detailed metal machinery and neon lighting
- a rotating inner ring animated through code
- light particles following a closed figure-eight path
- RGB bricks with gradual color changes and staggered lighting cycles
- brighter faces, clothing and mechanical details
- a six-second animation that loops continuously
- a responsive page for desktop and mobile devices
- English descriptions, documentation and interface

## ♾️ First creation — Perpetuum

> Every ending sets a new beginning in motion.

Two people observe a machine symbolizing continuous motion and creative momentum. Energy follows a closed path, the rotor turns and the laboratory lights change color.

Perpetual motion is an artistic concept here. The human characters remain still; the rotor, energy, gadgets and RGB bricks are animated.

## 🎨 How it is made

1. The base illustration is generated with AI assistance.
2. Python code lifts shadows and midtones and isolates the rotor.
3. Motion, light trails and RGB color changes are calculated for each frame.
4. Pillow assembles 120 frames into a continuously looping GIF.
5. When available, FFmpeg reduces the GIF file size.
6. The README displays the GIF, while a separate HTML page adds playback controls.

## 🔒 Creative process

The finished artwork, base illustration and animation code are included in the repository. Prompts and private working notes are not shared.

## ⚙️ Technologies

- Python and Pillow — frame generation and GIF export
- FFmpeg — optional file size optimization
- HTML, CSS and JavaScript — standalone animation page
- GitHub Markdown — repository homepage presentation
- GitHub Pages — website hosting

Pillow and FFmpeg are open-source tools. Rebuilding the animation from the included illustration requires no paid service or API key. The base illustration was previously created using an AI tool.

## 🚀 Run locally

Open `index.html` in a browser to view the animation. No installation is required.

To rebuild the GIF, use a Python version compatible with the pinned Pillow release:

```sh
python -m pip install -r requirements.txt
python src/render.py
```

The script saves `perpetuum.gif` and a still preview at `assets/poster.jpg`. If FFmpeg is installed and available on your system PATH, GIF optimization runs automatically.

## 📁 Project structure

```text
motivational-momentum-365/
├── README.md
├── index.html
├── perpetuum.gif
├── requirements.txt
├── assets/
│   ├── scene.png
│   └── poster.jpg
└── src/
    └── render.py
```

## 🗺️ Future creations

- more motivational visuals and animations
- a gallery with a title, date and message for each creation
- further experiments with light, motion and computer-generated scenes

## 🤝 Feedback

Suggestions and bug reports are welcome through [GitHub Issues](https://github.com/ChevCellios/motivational-momentum-365/issues).

## 📬 Contact

- GitHub: [ChevCellios](https://github.com/ChevCellios)
- Project: [Motivational Momentum 365](https://github.com/ChevCellios/motivational-momentum-365)
