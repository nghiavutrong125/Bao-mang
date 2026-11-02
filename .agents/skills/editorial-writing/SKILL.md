---
name: editorial-writing
description: Master Editorial Voice, Style Guide, and Quality Standards for drafting, reviewing, and publishing articles for Fifty Fifty Magazine.
---

# Editorial Writing Skill — Fifty Fifty Magazine

Use this skill whenever drafting, reviewing, editing, or formatting travel articles for Fifty Fifty Magazine.

## 1. Brand Identity & Editorial Philosophy
- **Brand Identity:** Bold, Curious, Honest, and Grounded.
- **Publication Name:** Fifty Fifty Magazine
- **Author Identity:** Team 50/50 (`team-50-50`)
- **Editorial Philosophy:** We explore both sides of every travel experience. We celebrate what deserves attention, question what feels overrated, and help readers make better travel decisions.
- **Core Promise:** *Two sides of every journey. One honest perspective.*

## 2. Voice and Tone
- Write in modern, natural, international English.
- Sound like a knowledgeable, independent travel editor — not a tour salesperson, influencer, or academic researcher.
- Be confident but never arrogant.
- Be engaging without exaggeration.
- Use subtle wit and occasional skepticism where appropriate.
- Balance cultural storytelling with actionable travel information.
- Respect local communities, customs, and perspectives.

## 3. Writing Rules
1. **Start strong:** Start with an interesting observation, useful fact, compelling question, or meaningful contrast. Avoid lengthy, generic introductions.
2. **Pacing:** Prefer short and medium-length sentences. Vary sentence structure naturally.
3. **Restraint:** Use vivid descriptions selectively, not in every paragraph.
4. **Utility:** Explain why information matters to the traveler.
5. **Fair balance:** Present advantages and disadvantages fairly. Never force gimmicky jargon like "The 50/50 Breakdown" or percentages into titles or prose.
6. **Integrity & Authenticity:** Distinguish verified facts from editorial opinions. Never fabricate interviews, quotations, statistics, or first-hand experiences.
7. **Specificity:** Include specific local prices (in local currency & USD), exact street names, verified timing windows, and transit details.
8. **Anti-filler:** Avoid repetitive SEO phrases, generic AI writing patterns, and unnecessary fluff.
9. **Anti-clickbait:** Titles must be accurate, compelling, and under 100 characters.

## 4. Language to Avoid (Banned Words)
Strictly avoid excessive or unearned use of:
- `breathtaking`
- `hidden gem`
- `unforgettable`
- `ultimate`
- `must-visit`
- `nestled`
- `vibrant tapestry`
- `rich cultural heritage`
- `a paradise for travelers`
- `once-in-a-lifetime experience`

*Rule:* Use concrete, grounded nouns and active verbs instead of empty superlatives.

## 5. Article Structure
- **Opening:** Capture attention and establish the central tension or atmosphere.
- **Context:** Why this destination/tradition matters right now.
- **Main Narrative:** Grounded reportage, cultural context, and sensory observations.
- **Practical Field Guide:** Costs, navigation, timing, common pitfalls, and respectful local etiquette.
- **The Verdict:** A concise, clear assessment of who this trip is genuinely for and who should skip it.

## 6. Category Weightings
- **Destinations:** 60% practical, 25% storytelling, 15% editorial perspective.
- **Honest Reviews:** 45% evaluation, 40% verified evidence and practical details, 15% storytelling.
- **Tips & Scams:** 70% practical guidance, 20% evidence and context, 10% storytelling.
- **Culture & Food:** 40% storytelling, 35% cultural explanation, 25% practical information.

## 7. Mandatory Image SEO & Standards
1. **Descriptive Filenames:** Never use `cover.webp` or `photo1.jpg`. Every image must use a descriptive hyphenated SEO slug (e.g. `chiang-mai-inthakin-festival-wat-chedi-luang.webp`).
2. **Captions & Alt:** Every image must be wrapped in `<figure>` with descriptive `alt` and `<figcaption>` containing concrete geographic and cultural context.
3. **Pipeline:** Process through `tools/image_pipeline.py` (strip 100% EXIF, convert to WebP Q=85, sync to Cloudflare R2 bucket `bao-mang`, update `data/photo-catalog.json`).

## 8. Agent Pre-Publication Checklist
Before committing any new article:
1. Does it sound like an independent, experienced editor?
2. Are all banned buzzwords eliminated?
3. Are all prices, timings, and transit notes accurate and verified?
4. Are all image files named with SEO slugs and captioned with `<figcaption>`?
5. Does the frontmatter pass Astro schema (`title <= 100`, `description <= 160`)?
6. Does `npm run build` succeed with 0 errors?
