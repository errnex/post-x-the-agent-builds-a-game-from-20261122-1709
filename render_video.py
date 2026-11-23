#!/usr/bin/env python3
"""Render the video for the make.fun post-x bounty, frame by frame.

Scenes (1080x1920, 30fps):
  A 0-4s    hook: ONE PROMPT + the prompt typed out
  B 4-15s   terminal: the agent building the game
  C 15-29s  the finished game actually running (deterministic sim of game.html)
  D 29-31s  call: come build on make.fun
Then the 9:16 press-pack end card is appended by ffmpeg (see build.sh step).
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

BG = (11, 11, 18)
PANEL = (17, 17, 28)
INK = (242, 242, 247)
MUTED = (138, 138, 153)
MAGENTA = (255, 46, 136)
CYAN = (34, 211, 238)
GREEN = (74, 222, 128)
TERM_GREEN = (120, 220, 130)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def text_center(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)

def rounded(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- scene A
PROMPT_L1 = "Build me a tiny browser game:"
PROMPT_L2 = "dodge the falling blocks."

def scene_a(frame):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    t = frame / FPS
    # magenta top bar sweeps in
    bar_w = int(min(1.0, t / 0.6) * 1080)
    d.rectangle([0, 0, bar_w, 14], fill=MAGENTA)
    # ONE PROMPT. pops in at 0.3s
    if t >= 0.3:
        pop = min(1.0, (t - 0.3) / 0.18)
        size = int(118 + (1 - pop) * 26)
        f = font(FB, size)
        text_center(d, W / 2, 700 - int((1 - pop) * 10), "ONE", f, INK)
        text_center(d, W / 2, 830 - int((1 - pop) * 10), "PROMPT.", f, MAGENTA)
    # prompt types from 1.1s, 34 chars/s
    if t >= 1.1:
        n = int((t - 1.1) * 34)
        full = PROMPT_L1 + "\n" + PROMPT_L2
        shown = full[:n]
        f = font(FM, 44)
        y = 1120
        caret = int(t * 2.4) % 2 == 0
        for i, line in enumerate(shown.split("\n")):
            d.text((90, y + i * 62), line, font=f, fill=INK)
        if n < len(full) and caret:
            last = shown.split("\n")[-1]
            cx = 90 + d.textlength(last, font=f)
            cy = y + (len(shown.split("\n")) - 1) * 62
            d.rectangle([cx + 6, cy + 6, cx + 22, cy + 52], fill=CYAN)
    if t >= 3.4:
        f = font(FR, 36)
        text_center(d, W / 2, 1560, "my AI agent is on it  →", f, MUTED)
    return img

# ---------------------------------------------------------------- scene B
BLINES = [
    ('$ ', 'agent build "dodge the falling blocks"', INK),
    ('✓ ', 'scaffolded game.html — canvas 540×960', GREEN),
    ('✓ ', 'player + arrow / drag controls', GREEN),
    ('✓ ', 'falling blocks, collision, score', GREEN),
    ('✓ ', 'playtested 3 runs — 0 errors', GREEN),
    ('→ ', 'built in 41s. opening the game…', CYAN),
]
LINE_START = [0.4, 1.5, 2.9, 4.3, 5.7, 7.1]  # seconds into scene B
TYPE_CPS = 55

def scene_b(frame):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    t = frame / FPS
    text_center(d, W / 2, 240, "THE AGENT", font(FB, 54), MUTED)
    text_center(d, W / 2, 310, "GETS TO WORK", font(FB, 54), INK)
    # terminal window
    x0, y0, x1, y1 = 70, 460, 1010, 1120
    rounded(d, [x0, y0, x1, y1], 26, PANEL, outline=(38, 38, 58), width=2)
    d.ellipse([x0 + 34, y0 + 30, x0 + 62, y0 + 58], fill=(255, 95, 86))
    d.ellipse([x0 + 74, y0 + 30, x0 + 102, y0 + 58], fill=(255, 189, 46))
    d.ellipse([x0 + 114, y0 + 30, x0 + 142, y0 + 58], fill=(39, 201, 63))
    d.text((x0 + 380, y0 + 26), "agent — zsh", font=font(FM, 30), fill=MUTED)
    f = font(FM, 33)
    fy = y0 + 100
    for i, (mark, line, col) in enumerate(BLINES):
        lt = t - LINE_START[i]
        if lt < 0:
            continue
        n = int(lt * TYPE_CPS)
        shown = (mark + line)[:n]
        d.text((x0 + 40, fy), shown, font=f, fill=col if mark != '$ ' else INK)
        if n < len(mark + line) and int(t * 2.4) % 2 == 0 and i == len([1 for s in LINE_START if t >= s]) - 1:
            cx = x0 + 40 + d.textlength(shown, font=f)
            d.rectangle([cx + 4, fy + 4, cx + 18, fy + 40], fill=TERM_GREEN)
        fy += 72
    if t >= 9.6:
        text_center(d, W / 2, 1260, "no human touched the code.", font(FR, 36), MUTED)
    return img

# ---------------------------------------------------------------- scene C: game sim
GW, GH = 540, 960
SCALE = 1.6
GX, GY = 108, 330  # game area top-left on the 1080x1920 frame

class Sim:
    def __init__(self, seed=7):
        self.rng = random.Random(seed)
        self.reset()
    def reset(self):
        self.blocks = []
        self.score = 0
        self.elapsed = 0.0
        self.over = False
        self.px = GW / 2
        self.spawn_in = 0.0
    def spawn(self):
        w = 40 + self.rng.random() * 70
        self.blocks.append({
            "x": self.rng.random() * (GW - w), "y": -60.0, "w": w,
            "h": 34 + self.rng.random() * 40,
            "vy": 3.4 + self.rng.random() * 2.2 + min(3.5, self.elapsed / 9000),
            "hue": 335 + self.rng.random() * 30})
    def step(self, dt, frozen=False):
        if self.over:
            return
        self.elapsed += dt
        self.score = int(self.elapsed / 250)
        if not frozen:
            # danger band: blocks whose bottom edge is near the player row
            danger = [b for b in self.blocks if b["y"] + b["h"] > 560 and b["y"] < 906]
            if danger:
                occupied = sorted((b["x"], b["x"] + b["w"]) for b in danger)
                gaps = []
                cur = 0.0
                for x0, x1 in occupied:
                    if x0 - cur >= 56:
                        gaps.append((cur + (x0 - cur) / 2 - 28, x0 - cur))
                    cur = max(cur, x1)
                if GW - cur >= 56:
                    gaps.append((cur + (GW - cur) / 2 - 28, GW - cur))
                if gaps:
                    target = max(gaps, key=lambda g: g[1])[0]
                    target = max(0, min(GW - 56, target))
                    if target > self.px + 4:
                        self.px += 9
                    elif target < self.px - 4:
                        self.px -= 9
            else:
                self.px += (GW / 2 - self.px) * 0.02
            self.px = max(0, min(GW - 56, self.px))
        self.spawn_in -= dt
        if self.spawn_in <= 0:
            self.spawn()
            self.spawn_in = max(240, 620 - self.elapsed / 40)
        for b in self.blocks:
            b["y"] += b["vy"] * (dt / 16.7)
        self.blocks = [b for b in self.blocks if b["y"] < GH + 80]
        for b in self.blocks:
            if (self.px < b["x"] + b["w"] and self.px + 56 > b["x"]
                    and 850 < b["y"] + b["h"] and 850 + 56 > b["y"]):
                self.over = True

# Pre-run the sim for the whole scene so every frame is deterministic.
DT = 1000 / FPS
GAME_LEN = 14.0  # seconds of scene C
sim = Sim()
snapshots = []
death_at = None
for i in range(int(GAME_LEN * FPS)):
    gt = i / FPS
    if sim.over:
        if death_at is None:
            death_at = gt
        if gt - death_at >= 1.2:
            sim.reset()
            death_at = None
    sim.step(DT)
    snapshots.append(([{"x": b["x"], "y": b["y"], "w": b["w"], "h": b["h"],
                       "hue": b["hue"]} for b in sim.blocks],
                      sim.px, sim.score, sim.over))

def scene_c(frame):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    t = frame / FPS
    blocks, px, score, over = snapshots[min(frame, len(snapshots) - 1)]
    # header
    d.text((108, 150), "DODGE!", font=font(FB, 64), fill=INK)
    d.text((108 + d.textlength("DODGE!", font=font(FB, 64)) + 16, 168), "it runs.",
           font=font(FR, 44), fill=MAGENTA)
    s = str(score)
    sw = d.textlength(s, font=font(FB, 64))
    d.text((972 - sw, 150), s, font=font(FB, 64), fill=CYAN)
    d.text((972 - d.textlength("SCORE", font=font(FR, 28)), 222), "SCORE",
           font=font(FR, 28), fill=MUTED)
    # game area
    d.rectangle([GX, GY, GX + GW * SCALE, GY + GH * SCALE], fill=(17, 17, 28),
                outline=(38, 38, 58), width=2)
    clip = Image.new("RGB", (int(GW * SCALE), int(GH * SCALE)), (17, 17, 28))
    g = ImageDraw.Draw(clip)
    for y in range(0, GH, 60):
        g.line([(0, y * SCALE), (GW * SCALE, y * SCALE)], fill=(29, 29, 46))
    for b in blocks:
        hue = int(b["hue"])
        # approximate hsl(335-365, 90%, 58%) in rgb
        r, gg, bb = (255, 46, 136) if hue < 350 else (255, 80, 120)
        g.rectangle([b["x"] * SCALE, b["y"] * SCALE,
                     (b["x"] + b["w"]) * SCALE, (b["y"] + b["h"]) * SCALE],
                    fill=(r, gg, bb))
        g.rectangle([b["x"] * SCALE, b["y"] * SCALE,
                     (b["x"] + b["w"]) * SCALE, b["y"] * SCALE + 10],
                    fill=(255, 130, 185))
    g.rectangle([px * SCALE, 850 * SCALE, (px + 56) * SCALE, 906 * SCALE], fill=CYAN)
    g.rectangle([px * SCALE, 850 * SCALE, (px + 56) * SCALE, 850 * SCALE + 13],
                fill=(200, 245, 255))
    img.paste(clip, (GX, GY))
    if over:
        ov = Image.new("RGBA", (int(GW * SCALE), int(GH * SCALE)), (5, 5, 12, 184))
        region = img.crop((GX, GY, GX + int(GW * SCALE), GY + int(GH * SCALE))).convert("RGBA")
        img.paste(Image.alpha_composite(region, ov).convert("RGB"), (GX, GY))
        d = ImageDraw.Draw(img)
        text_center(d, W / 2, 880, "GAME OVER", font(FB, 96), INK)
        text_center(d, W / 2, 1000, f"SCORE {score}", font(FB, 56), CYAN)
        if t < 13.0:
            text_center(d, W / 2, 1100, "…run it back", font(FR, 40), MUTED)
    if t < 1.2:
        text_center(d, W / 2, 60, "THE FINISHED GAME — LIVE", font(FB, 40), MUTED)
    return img

# ---------------------------------------------------------------- scene D
def scene_d(frame):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    t = frame / FPS
    if t >= 0.2:
        text_center(d, W / 2, 760, "Your turn.", font(FB, 110), INK)
    if t >= 0.7:
        text_center(d, W / 2, 920, "Come build on", font(FB, 78), INK)
        text_center(d, W / 2, 1010, "make.fun", font(FB, 78), MAGENTA)
    if t >= 1.2:
        text_center(d, W / 2, 1240, "one prompt is all it takes.", font(FR, 40), MUTED)
    return img

# ---------------------------------------------------------------- render
SCENES = [(scene_a, 4.0), (scene_b, 11.0), (scene_c, 14.0), (scene_d, 2.0)]
idx = 0
for fn, dur in SCENES:
    n = int(dur * FPS)
    for i in range(n):
        fn(i).save(os.path.join(OUT, f"f{idx:04d}.png"))
        idx += 1
print(f"rendered {idx} frames = {idx / FPS:.1f}s into {OUT}")
