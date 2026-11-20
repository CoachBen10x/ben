---
name: easy-video-editing
description: Edit talking-head videos and reels with ffmpeg: transcribe speech (English/Malay), burn in pop-up or plain captions, face-tracked 9:16 vertical crop, cut silent pauses, trim, join clips, add background music, speed up, shrink for WhatsApp, grab a cover photo. Use when the person uploads a video and asks for any of these.
---

# Easy video editing

Talk to the person in simple words. Don't show commands unless they ask.

## 0. Make sure the tools are there (seconds if already installed)

```bash
S=$(find /home /root -path "*/.claude/skills/easy-video-editing/scripts" -type d 2>/dev/null | head -1)
mkdir -p ~/easy-edit && cp -n "$S"/*.py ~/easy-edit/ 2>/dev/null
python3 -c "import faster_whisper, cv2" 2>/dev/null || {
  apt-get update -q >/dev/null || true
  command -v ffmpeg >/dev/null || apt-get install -y -q ffmpeg
  apt-get install -y -q fonts-montserrat >/dev/null 2>&1 || true
  pip install --break-system-packages -q faster-whisper "av<19" "opencv-contrib-python-headless<5" numpy; }
```
(`av<19`: newer PyAV breaks faster-whisper. `opencv<5`: v5 drops the face-detector file.)
The speech model downloads from Hugging Face on first use. If it is blocked, tell the person:
"Speech-to-text needs the Hugging Face sites allowed. Start the session on the **ben-video** environment."
Everything else still works.

## 1. Workflow

- Uploads: Claude Code cloud puts them in `/root/.claude/uploads/<id>/`; claude.ai in `/mnt/user-data/uploads/`.
- Never touch the original. Work on a copy, name outputs clearly (`reel-captions.mp4`), and save results
  in the working directory or scratchpad so the person can open them.
- After every edit, check your work: contact sheet
  `ffmpeg -i out.mp4 -vf "fps=1/3,scale=270:-1,tile=6x1" -frames:v 1 sheet.jpg`, look at it, and check length with `ffprobe`.
- Reels: 1080x1920 (9:16), H.264 + AAC, `-pix_fmt yuv420p`, `-movflags +faststart`.
- If something fails, say what failed in one line and try the next simplest way.

## 2. Recipes

**Transcribe / captions**
```bash
python3 ~/easy-edit/transcribe.py in.mp4 --lang en
python3 ~/easy-edit/transcribe.py in.mp4 --lang ms --model medium --prompt "names, brand words"   # Malay
```
Gives `in.srt` + `in_words.json`. Show the person the text; fix wrong names in the .srt by hand.

**Pop-up captions burned in** (video must already be 1080x1920; lower-middle, clear of TikTok/IG buttons)
```bash
python3 ~/easy-edit/popcaps.py in.srt caps.ass --accent "FREE,WEIGHT"
ffmpeg -i in.mp4 -vf "ass=caps.ass" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart out.mp4
```

**Plain captions burned in**
```bash
ffmpeg -i in.mp4 -vf "subtitles=in.srt:force_style='FontName=Montserrat,FontSize=14,Bold=1,Outline=2,MarginV=60'" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out.mp4
```

**Face tracking to vertical** (follows the speaker even with sunglasses / side-on; ignores one-off false hits)
```bash
python3 ~/easy-edit/facetrack.py in.mp4 out.mp4      # calmer: --smooth 0.04, faster: --every 5
python3 ~/easy-edit/facetrack.py in.mp4 out.mp4 --zoom 1.8 --facey 0.3 --every 2   # full-body/stage shot -> upper body
```
`--zoom` punches in (works on vertical videos too); `--facey` = where the face sits from the top (0.3 shows more body).
4K 60fps: ~10 s of work per 1 s of video.

**Fun captions**: for short hooks, write the .ass by hand from `in_words.json`: 1-3 words per line,
key words bigger + yellow (`Montserrat Black`, `\frz-4`, scale-down "slam"), the rest white pop-in.

**Cut pauses**
```bash
python3 ~/easy-edit/cutpauses.py in.mp4 out.mp4 --min 0.35
```

**Trim** (both times before `-i` = real times in the original)
```bash
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac out.mp4
```

**Join clips** (re-encodes, so clips from different phones still join)
```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0];[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```
More clips: add inputs and `[v2][2:a]`, set `n=`. A clip with no sound needs a silent track first (`-f lavfi -i anullsrc`).

**9:16 with blurred background**
```bash
ffmpeg -i in.mp4 -filter_complex "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out.mp4
```

**Music under the voice** (music ~15%, fades out at the end; `normalize=0` keeps the voice at full volume)
```bash
ffmpeg -i in.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.15,afade=t=out:st=DUR-2:d=2[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4
```
Replace DUR with the video length from ffprobe. Only music the person owns or that is royalty-free. Never put song lyrics on screen.

**Speed up 1.2x**
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=PTS/1.2[v];[0:a]atempo=1.2[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```

**Smaller for WhatsApp** (longest side max 1280, works for vertical and landscape)
```bash
ffmpeg -i in.mp4 -vf "scale='if(gt(iw,ih),min(1280,iw),-2)':'if(gt(iw,ih),-2,min(1280,ih))'" -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart small.mp4
```

**Cover photo**
```bash
ffmpeg -ss 00:00:03 -i in.mp4 -frames:v 1 -q:v 2 cover.jpg
```
