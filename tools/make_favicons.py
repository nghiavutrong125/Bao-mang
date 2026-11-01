import base64
import io
from pathlib import Path
from PIL import Image

src_path = Path(r"D:\My-small-app\bao-mang\public\favicon.png")
src_img = Image.open(src_path).convert("RGBA")

pub_dir = Path(r"D:\My-small-app\bao-mang\public")

# 1. Generate favicon-96x96.png
ico_96 = src_img.resize((96, 96), Image.Resampling.LANCZOS)
ico_96.save(pub_dir / "favicon-96x96.png", "PNG")

# 2. Generate apple-touch-icon.png (180x180)
ico_180 = src_img.resize((180, 180), Image.Resampling.LANCZOS)
ico_180.save(pub_dir / "apple-touch-icon.png", "PNG")

# 3. Generate web-app-manifest-192x192.png
ico_192 = src_img.resize((192, 192), Image.Resampling.LANCZOS)
ico_192.save(pub_dir / "web-app-manifest-192x192.png", "PNG")

# 4. Generate web-app-manifest-512x512.png
ico_512 = src_img.resize((512, 512), Image.Resampling.LANCZOS)
ico_512.save(pub_dir / "web-app-manifest-512x512.png", "PNG")

# 5. Generate favicon.ico (multi-resolution 16, 32, 48)
ico_16 = src_img.resize((16, 16), Image.Resampling.LANCZOS)
ico_32 = src_img.resize((32, 32), Image.Resampling.LANCZOS)
ico_48 = src_img.resize((48, 48), Image.Resampling.LANCZOS)
ico_48.save(
    pub_dir / "favicon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)],
)

# 6. Generate favicon.svg (embedded high-res PNG inside SVG viewBox)
buffer = io.BytesIO()
ico_512.save(buffer, format="PNG")
b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <image width="512" height="512" href="data:image/png;base64,{b64}"/>
</svg>"""

with open(pub_dir / "favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Successfully generated all favicons from official logo!")
