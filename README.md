# ⚡ Motivational Momentum 365

[![Beyond the Horizon — a luminous probe explores a holographic orbit above a futuristic city](horizon.gif)](https://chevcellios.github.io/motivational-momentum-365/)

![Language](https://img.shields.io/badge/language-English-green)
![Animation](https://img.shields.io/badge/animation-GIF-blueviolet)
![Code](https://img.shields.io/badge/code-Python-orange)
![Loop](https://img.shields.io/badge/loop-10%20seconds-00b8c4)
![Resolution](https://img.shields.io/badge/resolution-960%20%C3%97%20540-blue)

One idea. One creation. Keep moving. Motivational Momentum 365 brings together AI-assisted artwork, code and daily creative experiments.

## 🔗 Watch the collection

| Creation | Page | GIF |
| --- | --- | --- |
| 004 — Beyond the Horizon | [Watch](https://chevcellios.github.io/motivational-momentum-365/) | [GIF](horizon.gif) |
| 003 — Emergence | [Watch](https://chevcellios.github.io/motivational-momentum-365/emergence.html) | [GIF](emergence.gif) |
| 002 — Teleportation | [Watch](https://chevcellios.github.io/motivational-momentum-365/teleportation.html) | [GIF](teleportation.gif) |
| 001 — Perpetuum | [Watch](https://chevcellios.github.io/motivational-momentum-365/perpetuum.html) | [GIF](perpetuum.gif) |

## 🛰️ Latest creation — Beyond the Horizon

> Progress begins where certainty ends.

A small luminous probe launches from an old motherboard. A holographic navigation globe emerges above it, and the probe follows an orbital path before returning home. The cycle starts again: exploration becomes a practice, not a single leap.

This new animation shares the sunrise rooftop artwork from Emergence. The probe, solar wings, orbital trail, navigation grid, launch rings and RGB indicators are animated through code. The city and human observers remain still.

## ✨ Features

- a bright cyberpunk city at sunrise
- a metallic probe with small animated solar wings
- smooth launch, orbital flight and return
- a rotating holographic globe with navigation marks
- light trails, motherboard impulses and RGB status lights
- ten seconds, 200 frames and continuous looping
- responsive pages with pause controls
- all three previous creations preserved

GitHub may pause GIFs according to the viewer's accessibility settings. The standalone pages start automatically and provide pause controls.

## 🎨 Creative process

The background illustration was generated with AI assistance for Emergence and is reused here. The new animation is rendered locally using Python and open-source tools; no new image generation is needed. Image-generation prompts and private working notes are not included.

## ⚙️ Technologies

- Python and Pillow — frame rendering and compositing
- NumPy — frame analysis and earlier animation effects
- FFmpeg — GIF palette optimization and export
- HTML, CSS and JavaScript — standalone viewing pages
- GitHub Markdown and GitHub Pages — presentation and hosting

## 🚀 Run locally

Open `index.html` in a browser. To rebuild the latest animation, install Python dependencies and ensure FFmpeg is available on PATH:

```sh
python -m pip install -r requirements.txt
python src/render_horizon.py
```

The script reads `assets/emergence/rooftop.png`, writes `horizon.gif` and saves a poster to `assets/horizon/poster.jpg`.

Earlier renderers are included as `src/render_emergence.py`, `src/render_teleportation.py` and `src/render.py`.

## 📁 Project structure

```text
motivational-momentum-365/
├── README.md
├── index.html
├── emergence.html
├── teleportation.html
├── perpetuum.html
├── horizon.gif
├── emergence.gif
├── teleportation.gif
├── perpetuum.gif
├── requirements.txt
├── assets/
│   ├── horizon/
│   ├── emergence/
│   └── teleportation/
└── src/
    ├── render_horizon.py
    ├── render_emergence.py
    ├── render_teleportation.py
    └── render.py
```

## 🤝 Feedback

Ideas and bug reports are welcome through [GitHub Issues](https://github.com/ChevCellios/motivational-momentum-365/issues).

## 📬 Contact

- GitHub: [ChevCellios](https://github.com/ChevCellios)
- Project: [Motivational Momentum 365](https://github.com/ChevCellios/motivational-momentum-365)
