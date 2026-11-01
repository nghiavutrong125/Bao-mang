#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processing & Cloudflare R2 Sync Pipeline for Fifty Fifty Magazine
- Converts & optimizes to WebP (lossy Q=85, ultra fast, lightweight < 150KB)
- Strips 100% EXIF & technical metadata (No camera, GPS, device, or editing footprints)
- NO logo / NO watermark (clean, authentic editorial magazine style)
- SEO slug naming (e.g. ha-giang-loop-road-01.webp)
- Resizes to standard ratios:
    * 16:9 (1200x675) - Article hero cover & banners
    * 3:2  (1200x800) - Standard editorial cards
    * max  (Max 1600px width/height, keeps original aspect ratio)
- Syncs automatically to Cloudflare R2 bucket: bao-mang
- Returns Public CDN URLs (https://pub-a444990dcfe849f3bdc97bf8dc4ca482.r2.dev/...)
"""

import os
import sys
import json
import re
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageOps

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOCAL_BACKUP_ROOT = Path("D:/Anh_Cloud/fiftyfifty-data")
CDN_BASE_URL = "https://pub-a444990dcfe849f3bdc97bf8dc4ca482.r2.dev"
R2_REMOTE = "r2-baomang"
R2_BUCKET = "bao-mang"

# Detect Rclone binary
POSSIBLE_RCLONES = [
    Path("D:/My-small-app/rclone-v1.73.3-windows-amd64/rclone.exe"),
    Path("D:/My-small-app/xu-ly-anh/bin/rclone.exe"),
    Path("F:/Cac-Du-An-Lap-Trinh/Xu-ly-anh-v2/bin/rclone.exe"),
]

def get_rclone_exe():
    for p in POSSIBLE_RCLONES:
        if p.exists():
            return str(p)
    system_rclone = shutil.which("rclone")
    if system_rclone:
        return system_rclone
    return None

TARGET_ASPECTS = {
    "16:9": (1200, 675),    # Hero Banner / Article Cover
    "3:2": (1200, 800),     # Standard Card
    "2:3": (800, 1200),     # Portrait Mobile
    "1:1": (1000, 1000),    # Square
    "max": (1600, 1080),    # Keep original aspect, max bounding box
    "original": (1600, 1080)
}

def to_slug(text: str) -> str:
    """Converts Vietnamese or arbitrary strings into clean SEO-friendly English slug."""
    text = text.lower().strip()
    text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
    text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
    text = re.sub(r'[ìíịỉĩ]', 'i', text)
    text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
    text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
    text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
    text = re.sub(r'[đ]', 'd', text)
    text = re.sub(r'[^a-z0-9_-]+', '-', text)
    return text.strip('-')

def strip_exif_and_process(img: Image.Image, aspect: str = "max") -> Image.Image:
    """
    1. Transposes orientation according to EXIF (if any) before stripping.
    2. Resizes and crops to requested aspect ratio.
    3. Recreates a clean RGB image to guarantee 100% EXIF and metadata are eliminated.
    """
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Ensure RGB mode (discard RGBA alpha or palette if converting to standard RGB)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Aspect ratio processing
    if aspect in ("max", "original"):
        max_w, max_h = TARGET_ASPECTS["max"]
        processed = img.copy()
        processed.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    else:
        target_w, target_h = TARGET_ASPECTS.get(aspect, (1200, 800))
        target_ratio = target_w / target_h
        img_ratio = img.width / img.height

        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            offset = (img.width - new_width) // 2
            cropped = img.crop((offset, 0, offset + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            offset = (img.height - new_height) // 2
            cropped = img.crop((0, offset, img.width, offset + new_height))

        processed = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Recreate brand new Image object to ensure zero technical metadata persistence
    clean_img = Image.new('RGB', processed.size)
    clean_img.paste(processed, (0, 0))
    return clean_img

def sync_to_cloudflare_r2(local_folder: Path, remote_subfolder: str) -> tuple[bool, str]:
    """Syncs processed images to Cloudflare R2 bucket using rclone."""
    rclone = get_rclone_exe()
    if not rclone:
        return False, "Không tìm thấy rclone.exe trên hệ thống!"

    # Remote destination: r2-baomang:bao-mang/<remote_subfolder>
    dest = f"{R2_REMOTE}:{R2_BUCKET}/{remote_subfolder}".replace("\\", "/")

    cmd = [
        rclone, "sync", str(local_folder), dest,
        "--s3-no-check-bucket",
        "--transfers", "16", "--checkers", "32",
        "--fast-list", "--stats", "1s"
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, "Đồng bộ Cloudflare R2 thành công!"
    except subprocess.CalledProcessError as e:
        return False, f"Lỗi Rclone: {e.stderr}"

def process_and_upload(
    input_files: list[str],
    base_name: str,
    subfolder: str = "",
    aspect: str = "max",
    quality: int = 85
) -> dict:
    """
    Main pipeline execution:
    - Strips EXIF
    - Renames with SEO counter (e.g. ha-giang-loop-01.webp)
    - Saves locally to D:/Anh_Cloud/fiftyfifty-data/<subfolder>
    - Syncs to Cloudflare R2
    - Returns CDN URLs and Markdown code
    """
    if not subfolder:
        now = datetime.now()
        subfolder = f"{now.strftime('%Y/%m')}/{to_slug(base_name)}"

    local_out_dir = LOCAL_BACKUP_ROOT / subfolder
    local_out_dir.mkdir(parents=True, exist_ok=True)

    slug_name = to_slug(base_name)
    results = []

    valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".avif"}

    # Filter and sort files
    file_paths = []
    for item in input_files:
        p = Path(item)
        if p.is_dir():
            for f in sorted(p.iterdir()):
                if f.suffix.lower() in valid_extensions:
                    file_paths.append(f)
        elif p.is_file() and p.suffix.lower() in valid_extensions:
            file_paths.append(p)

    if not file_paths:
        return {"success": False, "error": "Không tìm thấy file ảnh hợp lệ!"}

    single_file = len(file_paths) == 1

    for idx, fpath in enumerate(file_paths, start=1):
        try:
            with Image.open(fpath) as img:
                clean_img = strip_exif_and_process(img, aspect=aspect)

                if single_file:
                    out_filename = f"{slug_name}.webp"
                else:
                    out_filename = f"{slug_name}-{idx:02d}.webp"

                out_path = local_out_dir / out_filename

                # Save as clean WebP without EXIF
                clean_img.save(
                    out_path,
                    format="WEBP",
                    quality=quality,
                    method=6
                )

                file_size_kb = out_path.stat().st_size / 1024
                rel_url_path = f"{subfolder}/{out_filename}".replace("\\", "/")
                cdn_url = f"{CDN_BASE_URL}/{rel_url_path}"

                results.append({
                    "original": str(fpath),
                    "filename": out_filename,
                    "local_path": str(out_path),
                    "cdn_url": cdn_url,
                    "markdown": f"![{slug_name.replace('-', ' ').title()}]({cdn_url})",
                    "width": clean_img.width,
                    "height": clean_img.height,
                    "size_kb": round(file_size_kb, 1)
                })
        except Exception as e:
            print(f"Lỗi khi xử lý file {fpath}: {e}", file=sys.stderr)

    if not results:
        return {"success": False, "error": "Không có ảnh nào được xử lý thành công."}

    # Sync to Cloudflare R2
    sync_ok, sync_msg = sync_to_cloudflare_r2(local_out_dir, subfolder)

    return {
        "success": True,
        "sync_status": sync_msg,
        "subfolder": subfolder,
        "total_images": len(results),
        "images": results
    }

def main():
    parser = argparse.ArgumentParser(description="Image Pipeline for Fifty Fifty Magazine")
    parser.add_argument("--input", "-i", nargs="+", required=True, help="Path to input image file(s) or folder")
    parser.add_argument("--name", "-n", required=True, help="Base SEO name (e.g. 'ha-giang-loop')")
    parser.add_argument("--subfolder", "-s", default="", help="Subfolder in R2 (defaults to YYYY/MM/<name>)")
    parser.add_argument("--aspect", "-a", default="max", choices=["16:9", "3:2", "2:3", "1:1", "max"], help="Aspect ratio")
    parser.add_argument("--quality", "-q", type=int, default=85, help="WebP quality (1-100, default 85)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    result = process_and_upload(
        input_files=args.input,
        base_name=args.name,
        subfolder=args.subfolder,
        aspect=args.aspect,
        quality=args.quality
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not result.get("success"):
            print(f"❌ THẤT BẠI: {result.get('error')}")
            sys.exit(1)

        print("\n=======================================================")
        print(f"✅ ĐÃ XỬ LÝ & ĐỒNG BỘ THÀNH CÔNG {result['total_images']} ẢNH!")
        print(f"📁 Thư mục R2: {result['subfolder']}")
        print(f"⚡ Trạng thái: {result['sync_status']}")
        print("=======================================================\n")
        print("🔗 DANH SÁCH LINK CDN SẴN SÀNG SỬ DỤNG:\n")
        for img in result["images"]:
            print(f"• File: {img['filename']} ({img['width']}x{img['height']}, {img['size_kb']} KB)")
            print(f"  URL:      {img['cdn_url']}")
            print(f"  Markdown: {img['markdown']}\n")

if __name__ == "__main__":
    main()

