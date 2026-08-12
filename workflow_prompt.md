# Weekly Instagram Idea Generation Prompt

Create 5 new Instagram post ideas for Glimp. Write in clear, natural Chinese unless the user requests another language.

## Read first

Read all of the following before writing:

1. `README.md`
2. `sources.md`
3. every relevant file in `Style/`
4. `scripts/idea_context.json`
5. `scripts/recent_posts.json` when more source detail is needed
6. `ideas/used_ideas_index.json`

If generated context files are missing, run `scripts/run_weekly.ps1` first. If fetching is unavailable, continue using the archive and brand files, and explicitly mark source grounding as limited.

## Selection rules

- Start from a recognizable moment, body sensation, tension, or small behavior, not a generic wellness theme.
- Synthesize source signals; do not translate or closely paraphrase a source post.
- Avoid titles, scenarios, mechanisms, and emotional turns already present in the archive.
- Across five ideas, use at least three source accounts and two source groups.
- Vary formats: carousel, single-image editorial post, short reel, or simple exercise. Do not use one format more than twice.
- Vary contexts and emotional states. Avoid producing five versions of stress relief.
- Product integration is optional. Mention or show Glimp in no more than two of five ideas unless the brief is explicitly product-led.
- Do not make medical claims, promise outcomes, or present breathwork as treatment.

## Required file output

Create one file per idea in `ideas/` named `idea-YYYY-MM-DD-NN.md`. Continue numbering if files for that date already exist.

Each file must contain:

```markdown
# [Title]

- Date:
- Format:
- Primary audience/moment:
- Source signals: [accounts and concise signal; no copied wording]
- Why this is distinct:

## Core idea

[2-4 sentences]

## Hook

[On-post opening line]

## Content outline

[Slide/scene/caption structure]

## Caption direction

[Voice, message, CTA]

## Product role

[None / subtle / central, with rationale]

## Image Prompt

[Production-ready English prompt describing subject, action, environment, composition, light, palette, texture, mood, aspect ratio, and important exclusions]

## Image Prompt Notes

- Search keywords:
- What must remain visible:
- Avoid:
```

## Image-prompt rules

- Prompt for one coherent frame, not a mood-board list.
- Describe a believable human action and physical detail.
- Specify where negative space belongs if text may be overlaid.
- Default to vertical Instagram `4:5` unless the format requires otherwise.
- Match Glimp's warm, intimate, editorial realism; avoid glossy stock-photo wellness imagery.
- If the product appears, describe its shape, grip, scale, and visibility precisely. Do not invent product details.

## Final checks

Before finishing, compare every idea against the archive for semantic similarity, verify source diversity, verify format diversity, and append a compact entry for every new file to `ideas/used_ideas_index.json`.
