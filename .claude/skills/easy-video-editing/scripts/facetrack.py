#!/usr/bin/env python3
"""Face tracking: turn any video into a 9:16 reel that follows the speaker's face.
The crop moves smoothly (no shaking). Keeps the original sound.
--zoom 1.6 punches in (e.g. full-body stage shot -> upper body), also works on vertical videos.
Usage: python3 facetrack.py in.mp4 out.mp4 [--zoom 1.0] [--smooth 0.08] [--every 3] [--facey 0.4]"""
import argparse, subprocess, sys, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--zoom", type=float, default=1.0, help="1 = widest 9:16 crop; 1.5-2 = closer on the face")
ap.add_argument("--smooth", type=float, default=0.08, help="lower = slower, calmer camera (0.02-0.3)")
ap.add_argument("--every", type=int, default=3, help="look for the face every N frames (speed)")
ap.add_argument("--facey", type=float, default=0.4, help="where the face sits, from the top (0.3 = more body)")
a = ap.parse_args()

cap = cv2.VideoCapture(a.inp)
ok, fr = cap.read()
if not ok: sys.exit("Could not read the video.")
H, W = fr.shape[:2]                      # from a real frame: phone videos with rotation tags report the wrong size
fps = cap.get(cv2.CAP_PROP_FPS) or 30
cw = int(min(W, H * 9 / 16) / max(a.zoom, 1)) // 2 * 2; ch = int(cw * 16 / 9) // 2 * 2   # 9:16 crop size
ch = min(ch, H // 2 * 2)
hc = cv2.data.haarcascades
front = cv2.CascadeClassifier(hc + "haarcascade_frontalface_default.xml")
alt = cv2.CascadeClassifier(hc + "haarcascade_frontalface_alt2.xml")
prof = cv2.CascadeClassifier(hc + "haarcascade_profileface.xml")
sc = min(1.0, 960 / max(W, H))           # detect on a ~960 px image (fast, works for 4K too)

def detect(img):   # every face-like spot from all detectors (front, front-alt, profile both ways)
    g = cv2.equalizeHist(cv2.cvtColor(cv2.resize(img, None, fx=sc, fy=sc), cv2.COLOR_BGR2GRAY))
    m, out = max(20, int(min(g.shape) * 0.03)), []
    for c, flip in ((front, 0), (alt, 0), (prof, 0), (prof, 1)):
        gi = cv2.flip(g, 1) if flip else g
        for x, y, w, h in c.detectMultiScale(gi, 1.1, 5, minSize=(m, m)):
            if flip: x = gi.shape[1] - x - w
            out.append(((x + w / 2) / sc, (y + h / 2) / sc))
    return out

# pass 1: face candidates on sampled frames
cand, i = {}, 0
while ok:
    if i % a.every == 0:
        d = detect(fr)
        if d: cand[i] = np.array(d)
    i += 1
    ok, fr = cap.read()
cap.release(); n = i

# follow the speaker: start at the spot that shows up most often, then each step take the
# candidate closest to the last one (ignores one-off false hits like hands, shirts, posters)
R = 0.12 * max(W, H)
k, v = [], []
if cand:
    allp = np.concatenate(list(cand.values()))
    last = max(allp, key=lambda q: (np.hypot(*(allp - q).T) < R).sum())
    for j in sorted(cand):
        dist = np.hypot(*(cand[j] - last).T)
        if dist.min() < R: last = cand[j][dist.argmin()]; k.append(j); v.append(last)
    print(f"face found in {len(k)} of {len(range(0, n, a.every))} checks")
if not k:
    print("no face found: keeping the centre"); p = np.tile([W / 2, H / 2], (n, 1))
else:   # fill the gaps between detections in a straight line
    k, v = np.array(k), np.array(v, float)
    p = np.stack([np.interp(np.arange(n), k, v[:, 0]), np.interp(np.arange(n), k, v[:, 1])], 1)

# smooth the camera path both ways so it glides instead of jumping
for j in range(1, n): p[j] = p[j - 1] + a.smooth * (p[j] - p[j - 1])
for j in range(n - 2, -1, -1): p[j] = p[j + 1] + a.smooth * (p[j] - p[j + 1])
p[:, 0] = np.clip(p[:, 0] - cw / 2, 0, W - cw); p[:, 1] = np.clip(p[:, 1] - ch * a.facey, 0, H - ch)

# pass 2: crop each frame, scale to 1080x1920, add the original audio back
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
    "-s", "1080x1920", "-r", str(fps), "-i", "-", "-i", a.inp, "-map", "0:v", "-map", "1:a?",
    "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart", "-shortest", a.out], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(a.inp); j = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    x, y = p[min(j, n - 1)].astype(int)
    enc.stdin.write(cv2.resize(fr[y:y + ch, x:x + cw], (1080, 1920), interpolation=cv2.INTER_AREA).tobytes()); j += 1
enc.stdin.close(); enc.wait()
if enc.returncode: sys.exit("ffmpeg failed while writing the reel.")
print(f"{j} frames, crop {cw}x{ch} following the face -> {a.out}")
