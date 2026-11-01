# Fifty Fifty Magazine - AI Editorial & Writing Guidelines

## 1. Brand Identity & Naming
* **Publication Name:** Fifty Fifty Magazine (The brand name on the header, footer, and about page).
* **Author Identity:** Team 50/50 (The Editorial Collective).
* **Tone:** Objective, honest, field-tested travel journalism (BBC Travel / National Geographic / Lonely Planet style).

## 2. STRICT Editorial Writing Rules (MANDATORY)
* **DO NOT force the phrase "The 50/50", "The 50/50 Breakdown", or percentages ("50% Hype vs 50% Reality") into article titles, headings, or body text.**
* Write completely natural, professional travel journalism. 
* Present both sides (the beauty vs. the challenges, the highlights vs. the travel traps) organically through narrative, data tables, and bullet points — without tagging them with gimmicky "50/50" labels.
* Use clear, natural section headings:
  - Good: "Winter Realities: Highland Solitude vs. Mountain Chill"
  - Good: "Weather Conditions & What to Expect"
  - Good: "Essential Rules for Safe Winter Riding"
  - FORBIDDEN: "The 50/50 Reality Check", "The 50/50 Breakdown", "50% Magic / 50% Grind".

## 3. Image SEO & Captioning Policy (MANDATORY)
* **Every image MUST have a descriptive ALT tag and a visible editorial caption (`<figcaption>` or markdown italic caption).**
* Captions provide vital context for Google Image Search, indexing keywords (e.g. location name, specific pass, season, landmarks).
* Standard HTML format inside articles:
  ```html
  <figure class="my-6">
    <img src="..." alt="Detailed descriptive keywords" class="w-full rounded-lg shadow-sm" loading="lazy" />
    <figcaption class="text-xs text-center text-base-content/70 italic mt-2">
      Contextual caption describing the scene, location, and conditions.
    </figcaption>
  </figure>
  ```
* All article photos must go through `tools/image_pipeline.py`:
  - 100% EXIF & metadata stripped.
  - No watermarks or logos.
  - Converted to WebP format.
  - Synced to Cloudflare R2 bucket `bao-mang`.
  - Served via public CDN: `https://pub-a444990dcfe849f3bdc97bf8dc4ca482.r2.dev/...`
