# 50/FIFTY Magazine — Editorial Voice & Style Guide

**Brand Identity:** Bold, Curious, Honest, and Grounded.

**Editorial Philosophy:** We explore both sides of every travel experience. We celebrate what deserves attention, question what feels overrated, and help readers make better travel decisions.

---

## 1. Voice and Tone

- Write in modern, natural, international English.
- Sound like a knowledgeable, independent travel editor — not a tour salesperson, influencer, or academic researcher.
- Be confident but never arrogant.
- Be engaging without exaggeration.
- Use subtle wit and occasional skepticism where appropriate.
- Balance cultural storytelling with actionable travel information.
- Respect local communities, customs, and perspectives.

---

## 2. Writing Rules

1. **Start strong:** Start with an interesting observation, useful fact, compelling question, or meaningful contrast.
2. **Get to the point quickly:** Avoid lengthy, generic introductions.
3. **Pacing:** Prefer short and medium-length sentences. Vary sentence structure naturally.
4. **Restraint:** Use vivid descriptions selectively, not in every paragraph.
5. **Relevance:** Explain why information matters to the traveler.
6. **Balance:** Present advantages and disadvantages fairly.
7. **Integrity:** Distinguish verified facts, reported experiences, editorial opinions, and estimates.
8. **Authenticity:** Never fabricate interviews, quotations, statistics, sources, or first-hand experiences.
9. **Specificity:** Use specific examples, prices, locations, and practical details when verified.
10. **Honesty with flux:** Acknowledge uncertainty when information changes seasonally or is difficult to verify.
11. **Anti-filler:** Avoid repetitive SEO phrases, generic AI writing patterns, and unnecessary filler.
12. **Anti-clickbait:** Do not use sensationalist claims or misleading clickbait.
13. **NO Forced Jargon:** Never insert gimmicky labels like "The 50/50 Breakdown", "50% Good vs 50% Bad", or percentages into titles, headers, or body text. Balance is demonstrated through substance, not branding slogans.

---

## 3. Language to Avoid (BANNED CLICHÉS)

Strictly avoid excessive or unearned use of:

- ❌ `Breathtaking`
- ❌ `Hidden gem`
- ❌ `Unforgettable`
- ❌ `Ultimate`
- ❌ `Must-visit`
- ❌ `Nestled`
- ❌ `Vibrant tapestry`
- ❌ `Rich cultural heritage`
- ❌ `A paradise for travelers`
- ❌ `Once-in-a-lifetime experience`

*Rule:* Use these expressions only when genuinely justified by specific evidence or description. Prefer concrete, sensory words (e.g., "cool mountain air", "cracked red bricks", "20,000 Kip per plate") over generic hyperbole.

---

## 4. Editorial Article Structure

* **Opening:** Capture attention and establish the reader's main question or on-the-ground atmosphere.
* **Context:** Explain what makes the topic relevant or interesting.
* **Main Story:** Combine useful information, specific examples, cultural context, and critical observations.
* **Practical Perspective:** Include costs, logistics, transit, potential downsides, or recommendations where applicable.
* **The 50/FIFTY Verdict:** End with an honest, concise assessment. Explain who the experience is suitable for and who might prefer an alternative.

---

## 5. Category-Specific Editorial Ratios

- **Destinations:** 60% practical, 25% storytelling, 15% editorial perspective.
- **Honest Reviews:** 45% evaluation, 40% verified evidence and practical details, 15% storytelling.
- **Tips & Scams:** 70% practical guidance, 20% evidence and context, 10% storytelling.
- **Culture & Food:** 40% storytelling, 35% cultural explanation, 25% practical information.

---

## 6. Image & Media Standards (MANDATORY)

1. **Semantic Filenames for Image SEO:**
   - NEVER use generic filenames like `cover.webp`, `photo1.jpg`, or `IMG_1234.webp`.
   - Every file must use descriptive, hyphenated SEO slugs (e.g. `chiang-mai-inthakin-festival-wat-chedi-luang.webp`, `vientiane-year-end-dry-season-travel-guide.webp`).
2. **Mandatory Captions & Alt Text:**
   - Every single embedded image MUST feature `<figure class="my-6">`, `<img ... />` with keyword-rich `alt`, and `<figcaption class="text-xs text-center text-base-content/70 italic mt-2">` providing real geographic, cultural, and environmental context.
   - Google Image Search actively indexes `<figcaption>` text to determine visual search rankings.
3. **Pipeline Processing:**
   - Strip 100% of technical EXIF and camera metadata.
   - Compress to WebP Q=85, max bounding box 1600px.
   - Sync to Cloudflare R2 bucket `bao-mang` via `tools/image_pipeline.py`.
   - Update `data/photo-catalog.json`.

---

## 7. Pre-Publication Quality Checklist

Before publishing any article, the Agent must verify:

1. [ ] **Voice Check:** Does this sound like a knowledgeable, grounded 50/FIFTY travel editor?
2. [ ] **Cliché Audit:** Are all banned words (`breathtaking`, `hidden gem`, `unforgettable`, `ultimate`, `must-visit`, `nestled`, `tapestry`, `paradise`, etc.) removed?
3. [ ] **Utility Check:** Are specific prices, timings, transit options, and etiquette rules included?
4. [ ] **Factual Rigor:** Are opinions clearly distinguished from verified facts?
5. [ ] **Image SEO:** Are all image filenames descriptive, and does every image have a `<figcaption>` and descriptive `alt`?
6. [ ] **Schema Compliance:** Is the article title $\le 100$ characters and description $\le 160$ characters?
7. [ ] **Verdict:** Does it conclude with an honest, balanced assessment rather than promotional cheerleading?

**Our promise: Two sides of every journey. One honest perspective.**
