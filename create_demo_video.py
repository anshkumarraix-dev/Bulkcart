import os
import subprocess
import imageio_ffmpeg
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(BASE_DIR, "static", "demo_frames")
AUDIO_FILE = os.path.join(BASE_DIR, "static", "bulkcart_voiceover.wav")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "static", "bulkcart_demo_video.mp4")

# Target standard 1920x1080 Full HD
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

slides = [
    ("initial_storefront_1793040027480.png", 22.0),
    ("sample_round_loaded_1793040038314.png", 18.0),
    ("ai_analysis_populated_1793040053883.png", 15.0),
    ("quote_verdict_table_1793040059483.png", 20.0),
    ("quote_verdict_table_2_1793040064983.png", 17.0),
    ("pakka_bill_receipt_1793040078785.png", 16.0),
    ("final_pakka_bill_receipt_1793040093509.png", 15.5),
]

# 1. Normalize images to uniform 1920x1080 canvas with clean borders/padding
processed_frames = []
for idx, (filename, duration) in enumerate(slides):
    src_path = os.path.join(FRAMES_DIR, filename)
    img = Image.open(src_path).convert("RGB")
    
    # Calculate aspect-ratio preserving resize
    img_ratio = img.width / img.height
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT
    
    if img_ratio > target_ratio:
        new_w = TARGET_WIDTH
        new_h = int(TARGET_WIDTH / img_ratio)
    else:
        new_h = TARGET_HEIGHT
        new_w = int(TARGET_HEIGHT * img_ratio)
        
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create canvas with subtle warm background matching Retro Kirana theme (#f7f4ed)
    canvas = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), (247, 244, 237))
    offset_x = (TARGET_WIDTH - new_w) // 2
    offset_y = (TARGET_HEIGHT - new_h) // 2
    canvas.paste(resized_img, (offset_x, offset_y))
    
    norm_path = os.path.join(FRAMES_DIR, f"norm_slide_{idx}.png")
    canvas.save(norm_path, quality=95)
    processed_frames.append((norm_path, duration))

# 2. Build ffmpeg concat file
concat_txt = os.path.join(FRAMES_DIR, "concat.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    for norm_path, duration in processed_frames:
        # ffmpeg concat demuxer requires forward slashes
        clean_path = norm_path.replace("\\", "/")
        f.write(f"file '{clean_path}'\n")
        f.write(f"duration {duration}\n")
    # Repeat the last frame once without duration as required by concat demuxer
    last_path = processed_frames[-1][0].replace("\\", "/")
    f.write(f"file '{last_path}'\n")

# 3. Render video using imageio_ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg_exe, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt,
    "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
]

print("Running ffmpeg command:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("FFmpeg error:", result.stderr)
else:
    print(f"Demo video successfully created at: {OUTPUT_VIDEO}")
    print(f"Video file size: {os.path.getsize(OUTPUT_VIDEO):,} bytes")
