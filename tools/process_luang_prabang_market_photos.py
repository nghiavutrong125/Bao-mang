#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process 26 photos of Luang Prabang Night Market:
- Convert to WebP Q=85, max 1600 bounding box
- Strip EXIF completely
- Generate cover.webp (1200x675)
- Sync to Cloudflare R2 bucket 'bao-mang' under '2026/11/luang-prabang-night-market/'
- Update data/photo-catalog.json
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageOps

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_DIR = Path("D:/My-small-app/bao-mang")
TEMP_DIR = PROJECT_DIR / "temp_luang_prabang"
ARTICLE_DIR = PROJECT_DIR / "src/content/articles/luang-prabang-night-market-slow-guide"
CATALOG_PATH = PROJECT_DIR / "data/photo-catalog.json"
R2_DEST = "r2-baomang:bao-mang/2026/11/luang-prabang-night-market/"
CDN_BASE = "https://pub-a444990dcfe849f3bdc97bf8dc4ca482.r2.dev/2026/11/luang-prabang-night-market"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
ARTICLE_DIR.mkdir(parents=True, exist_ok=True)

POSSIBLE_RCLONES = [
    Path("D:/My-small-app/rclone-v1.73.3-windows-amd64/rclone.exe"),
    Path("D:/My-small-app/xu-ly-anh/bin/rclone.exe"),
]
rclone_bin = None
for p in POSSIBLE_RCLONES:
    if p.exists():
        rclone_bin = str(p)
        break
if not rclone_bin:
    rclone_bin = shutil.which("rclone")

# 26 images mapping
PHOTOS = [
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_12 (3).jpg",
        "slug": "luang-prabang-night-market-entrance-sisavangvong.webp",
        "alt": "Pedestrians and tourists browsing woven straw bags and textiles at the illuminated entrance of Luang Prabang night market",
        "caption": "The entrance to Sisavangvong Road as twilight falls: blue awnings, soft lantern light, and rows of handmade straw totes",
        "tags": ["night-market", "street", "bags", "straw", "evening", "textiles"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_13 (3).jpg",
        "slug": "luang-prabang-night-market-beerlao-tshirt-vendors.webp",
        "alt": "A Lao vendor couple sitting calmly on the floor beneath glowing bulbs surrounded by colorful Beerlao and Lao graphic t-shirts",
        "caption": "A husband and wife sitting peacefully beneath warm lightbulbs surrounded by classic Beerlao and Lao graphic t-shirts",
        "tags": ["vendors", "t-shirts", "beerlao", "couple", "night-market"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_14 (3).jpg",
        "slug": "luang-prabang-night-market-hmong-embroidery-buying.webp",
        "alt": "A woman crouching on the ground counting Kip currency while purchasing handmade Hmong embroidered fabric pouches",
        "caption": "Crouching on the floor tarps to count Lao Kip banknotes for hand-stitched Hmong textile cosmetic bags",
        "tags": ["hmong", "embroidery", "pouches", "shopping", "kip", "money"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_15 (3).jpg",
        "slug": "luang-prabang-night-market-sa-paper-star-lanterns.webp",
        "alt": "Hanging star-shaped Sa paper lanterns decorated with pressed flower petals and leaves glowing over an artisan stall",
        "caption": "Handmade star lanterns sculpted from Mulberry Sa paper embedded with real pressed bougainvillea petals",
        "tags": ["lanterns", "sa-paper", "flowers", "artisan", "decor"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_16 (2).jpg",
        "slug": "luang-prabang-night-market-silk-ikat-textile-artisan.webp",
        "alt": "A Lao woman wearing a traditional lace-collared blouse sitting among intricate hand-woven silk and brocade textiles",
        "caption": "Intricate Lao silk brocades and diamond-patterned ikat table runners tended by an artisan weaver",
        "tags": ["silk", "textiles", "weaving", "brocade", "artisan", "hmong"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_17 (2).jpg",
        "slug": "luang-prabang-night-market-hmong-pleated-skirt-setup.webp",
        "alt": "A woman setting up a traditional crimson pleated Hmong embroidered skirt onto a display mannequin in the evening street",
        "caption": "Setting up at 5:00 PM: dressing a mannequin in a crimson hand-embroidered Hmong pleated skirt on the pavement",
        "tags": ["hmong", "skirt", "setup", "textiles", "embroidery"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_18.jpg",
        "slug": "luang-prabang-night-market-cement-bag-totes-pouches.webp",
        "alt": "A young female vendor on a wooden stool above handmade elephant motif pouches and upcycled Lao cement bag totes",
        "caption": "Upcycled craftsmanship: drawstring pouches and coin bags sewn from traditional fabric and repurposed Lao cement sacks",
        "tags": ["upcycled", "cement-bag", "pouches", "elephant", "totes"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_19.jpg",
        "slug": "luang-prabang-night-market-pensive-vendor-blanket.webp",
        "alt": "A young vendor resting her chin in her hand with a cozy blanket over her lap behind rows of embroidered fabric purses",
        "caption": "The quiet stillness of Luang Prabang: a vendor resting her chin in her hand as cool night air sets in",
        "tags": ["vendor", "portrait", "stillness", "embroidery", "evening"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_20.jpg",
        "slug": "luang-prabang-night-market-artisan-hand-stitching-embroidery.webp",
        "alt": "A craftswoman sitting on the ground carefully hand-stitching geometric embroidery onto fabric surrounded by wooden carvings",
        "caption": "Living heritage: stitching fine geometric needlework by hand under the streetlights beside hand-carved wooden elephants",
        "tags": ["embroidery", "hand-stitched", "needlework", "craftswoman", "wooden-elephants"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_21.jpg",
        "slug": "luang-prabang-night-market-artist-painting-wood-magnets.webp",
        "alt": "An artist sitting on a colorful striped mat painting watercolor scenes and wooden magnets on the street",
        "caption": "An artisan painting miniature Luang Prabang almsgiving scenes directly onto wood-slice magnets and handmade cards",
        "tags": ["artist", "painting", "magnets", "hand-painted", "watercolors"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_22.jpg",
        "slug": "luang-prabang-night-market-sa-paper-monk-paintings.webp",
        "alt": "A vendor unfolding a fine woven silk shawl behind piles of hand-painted Sa paper artworks of saffron-robed monks",
        "caption": "Fine woven white scarves and hand-painted Mulberry Sa paper artworks depicting monks walking under black parasols",
        "tags": ["sa-paper", "monks", "paintings", "scarf", "straw-hats"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_23.jpg",
        "slug": "luang-prabang-night-market-vendor-friends-eating-curbside.webp",
        "alt": "Young vendor friends sitting barefoot on the painted yellow curb sharing a meal together from a soup bowl",
        "caption": "Community over commerce: friends and stall neighbors sharing a steaming hot dinner bowl on the painted street curb",
        "tags": ["food", "friends", "community", "curbside", "dinner"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_24.jpg",
        "slug": "luang-prabang-night-market-girl-lying-mat-phone-pouches.webp",
        "alt": "A young girl lying comfortably barefoot on a straw mat tending rows of colorful geometric woven fabric pouches",
        "caption": "A daughter lying barefoot on woven reed mats tending her family’s spread of geometric textile purses",
        "tags": ["family", "child", "pouches", "textiles", "daily-life"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_25.jpg",
        "slug": "luang-prabang-night-market-central-aisle-stroll.webp",
        "alt": "Travelers and locals walking down the central paved aisle of Sisavangvong night market under red and blue tent canopies",
        "caption": "The unhurried rhythm of Sisavangvong Road: travelers strolling slowly beneath canvas awnings without anyone shouting",
        "tags": ["market-aisle", "stroll", "crowd", "unhurried", "night"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_26.jpg",
        "slug": "luang-prabang-night-market-street-shake-cart-cafe.webp",
        "alt": "A stainless steel mobile street cart selling fruit shakes and iced drinks illuminated under the trees outside a café",
        "caption": "A mobile fruit shake cart under leafy street trees outside a heritage shophouse café and bookstore",
        "tags": ["fruit-shakes", "street-food", "cart", "drinks", "cafe"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_11 (3).jpg",
        "slug": "luang-prabang-night-market-elderly-woman-thip-khao-baskets.webp",
        "alt": "An elderly Lao woman vendor packing textiles into a bag beside stacked bamboo Thip Khao sticky rice baskets",
        "caption": "An elder vendor in red packing purchases beside stacks of woven bamboo Thip Khao sticky rice containers",
        "tags": ["thip-khao", "sticky-rice", "baskets", "elderly-vendor", "textiles"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_02 (4).jpg",
        "slug": "luang-prabang-night-market-monks-admiring-paintings.webp",
        "alt": "Two saffron-robed Buddhist monks sitting barefoot on the asphalt admiring hand-painted artworks on floor mats",
        "caption": "One of Luang Prabang's most moving sights: young Buddhist monks sitting barefoot on the road admiring local paintings",
        "tags": ["monks", "buddhist", "paintings", "saffron-robes", "art"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_03 (4).jpg",
        "slug": "luang-prabang-night-market-artist-painting-gold-apsara.webp",
        "alt": "A male painter meticulously applying golden pigment with a fine brush onto textured handmade Sa paper",
        "caption": "Mastery in plain sight: an artist painting a golden celestial figure onto thick Mulberry Sa paper on the pavement",
        "tags": ["artist", "painting", "gold-apsara", "sa-paper", "craftsmanship"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_04 (4).jpg",
        "slug": "luang-prabang-night-market-tourist-girl-calculator-bargain.webp",
        "alt": "A Western traveler bending down to inspect wooden crafts while a young girl with a calculator politely shows them",
        "caption": "Gentle trade: a traveler examining carved wooden items while a young stallholder holds a calculator with a calm smile",
        "tags": ["tourist", "calculator", "wood-crafts", "bargaining", "polite"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_05 (4).jpg",
        "slug": "luang-prabang-night-market-walking-crowd-lanterns.webp",
        "alt": "A gentle crowd of travelers in summer clothes wandering past clothing and craft stalls beneath streetlamps",
        "caption": "Visitors and locals wandering side by side in the cool mountain twilight along the 300-meter market stretch",
        "tags": ["crowd", "evening", "walking", "night-market", "atmosphere"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_06 (4).jpg",
        "slug": "luang-prabang-night-market-girl-handmade-cloth-cups-coasters.webp",
        "alt": "A young girl sitting barefoot on a stool beside piles of hand-stitched cloth coasters and woven straw totes",
        "caption": "Handmade cloth cup coasters and woven straw bags tended by a quiet young vendor sitting barefoot",
        "tags": ["coasters", "straw-totes", "girl", "handmade", "stitching"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_07 (4).jpg",
        "slug": "luang-prabang-night-market-antique-bronze-buddhas-urns.webp",
        "alt": "Two women vendors sitting behind antique bronze Buddha statues, water urns, and vintage brass cookware",
        "caption": "Heritage treasures: antique bronze Buddha effigies, water urns, and brass cookers laid out on woven mats",
        "tags": ["antiques", "bronze-buddha", "urns", "brass", "vintage"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_08 (4).jpg",
        "slug": "luang-prabang-night-market-smiling-artist-sunset-paintings.webp",
        "alt": "A smiling young woman sitting cross-legged under bright bulbs surrounded by sunset landscape paintings of the Mekong River",
        "caption": "A radiant smile among glowing lanterns and vivid landscape paintings of longboats on the Mekong at sunset",
        "tags": ["smiling-vendor", "paintings", "mekong-sunset", "lanterns", "portrait"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_09 (3).jpg",
        "slug": "luang-prabang-night-market-hanging-lanterns-vendor-resting.webp",
        "alt": "Glowing geometric Sa paper box lanterns illuminated with pressed flower petals and silhouette paintings of elephants",
        "caption": "Geometric box lanterns made of Mulberry bark paper glowing warmly with pressed dried flowers and elephant silhouettes",
        "tags": ["lanterns", "illuminated", "pressed-flowers", "elephants", "sa-paper"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_10 (4).jpg",
        "slug": "luang-prabang-night-market-sisters-baguette-sinh-skirts.webp",
        "alt": "Two sisters sitting on the market floor: one eating a warm French baguette sandwich, surrounded by indigo sinh skirts",
        "caption": "French colonial echoes meet Lao tradition: enjoying a crusty baguette sandwich among woven indigo sinh skirts",
        "tags": ["sisters", "baguette", "sinh-skirts", "indigo", "daily-life"],
        "orientation": "vertical",
    },
    {
        "src": r"C:\Users\ADMIN\Downloads\folder anh tam thoi\photo_01 (4).jpg",
        "slug": "luang-prabang-night-market-wide-avenue-fruit-cart.webp",
        "alt": "Looking down the wide central street of Sisavangvong Road under twilight lanterns with a parked fruit cart and motorbike",
        "caption": "A grand perspective down Sisavangvong Road as night envelops the former royal capital",
        "tags": ["sisavangvong", "wide-street", "night", "lanterns", "fruit-cart"],
        "orientation": "vertical",
    },
]

print(f"Total photos to process: {len(PHOTOS)}")

# Process each photo
processed_items = []

for idx, p in enumerate(PHOTOS, 1):
    src_path = Path(p["src"])
    if not src_path.exists():
        print(f"Error: {src_path} does not exist!")
        continue
    
    out_name = p["slug"]
    out_path = TEMP_DIR / out_name
    
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        
        # Max bounding box 1600x1200 while preserving aspect ratio
        im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        im.save(out_path, "WEBP", quality=85, method=6)
        
        print(f"[{idx:02d}/26] Saved: {out_name} ({im.size[0]}x{im.size[1]})")

    item_id = f"la-lpq-nightmarket-{idx:02d}"
    r2_url = f"{CDN_BASE}/{out_name}"
    
    processed_items.append({
        "id": item_id,
        "url": r2_url,
        "country": "la",
        "city": "luang-prabang",
        "poi": "sisavangvong-night-market",
        "route_segment": "luang-prabang-night-market",
        "suggested_day": "evening",
        "tags": p["tags"],
        "caption": p["caption"],
        "orientation": p["orientation"],
        "filename": out_name,
        "alt": p["alt"]
    })

# Generate Hero Cover (1200x675) from photo_02 (4) (Monks admiring paintings) or photo_01 (4) (Wide street)
# Monks admiring paintings (photo_02 (4)) or wide street (photo_01 (4))
cover_src = Path(PHOTOS[16]["src"]) # photo_02 (4).jpg - Monks admiring paintings
cover_dest = ARTICLE_DIR / "cover.webp"

with Image.open(cover_src) as im:
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    # Crop to 16:9 (1200x675) centered on the monks and painter
    w, h = im.size
    target_ratio = 16 / 9
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        im_cropped = im.crop((offset, 0, offset + new_w, h))
    else:
        new_h = int(w / target_ratio)
        offset = int(h * 0.25) # focus slightly lower where monks sit
        if offset + new_h > h:
            offset = h - new_h
        im_cropped = im.crop((0, offset, w, offset + new_h))
        
    im_cover = im_cropped.resize((1200, 675), Image.Resampling.LANCZOS)
    im_cover.save(cover_dest, "WEBP", quality=85, method=6)
    print(f"Generated cover.webp: {cover_dest} (1200x675)")

# Sync to R2 via Rclone
if rclone_bin:
    print(f"Syncing to Cloudflare R2: {R2_DEST}")
    cmd = [rclone_bin, "copy", str(TEMP_DIR), R2_DEST, "--fast-list", "--transfers=8", "--checkers=16"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("R2 sync SUCCESSFUL!")
    else:
        print(f"R2 sync error: {res.stderr}")
else:
    print("Warning: rclone not found, cannot upload to R2.")

# Update data/photo-catalog.json
if CATALOG_PATH.exists():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
else:
    catalog = []

# Remove any existing lpq-nightmarket entries to prevent duplicates
catalog = [c for c in catalog if not c.get("id", "").startswith("la-lpq-nightmarket-")]

for item in processed_items:
    catalog.append({
        "id": item["id"],
        "url": item["url"],
        "country": item["country"],
        "city": item["city"],
        "poi": item["poi"],
        "route_segment": item["route_segment"],
        "suggested_day": item["suggested_day"],
        "tags": item["tags"],
        "caption": item["caption"],
        "orientation": item["orientation"]
    })

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Updated {CATALOG_PATH} with {len(processed_items)} items. Total in catalog: {len(catalog)}")

