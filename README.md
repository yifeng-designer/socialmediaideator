# socialmediaideator

Glimp social media scraper and ideator.

## Glimp Instagram Idea Generator

This project prepares grounded, non-repetitive Instagram post ideas for Glimp.

## Weekly workflow

1. Install dependencies: `python -m pip install -r requirements.txt`
2. Copy `.env.example` to `.env`, then add `APIFY_API_TOKEN`. The `.env` file is ignored by Git; an already-set environment variable takes precedence.
3. Run `powershell -ExecutionPolicy Bypass -File scripts/run_weekly.ps1`.
4. Ask Codex to follow `workflow_prompt.md` and create this week's ideas.

The preparation script fetches recent Instagram posts and builds a compact context file. Idea generation then uses source material, brand guidance, and the archive index while avoiding close repeats.

## Structure

- `workflow_prompt.md`: generation rules and output contract
- `sources.md`: source pool and how each account should be used
- `Style/`: editorial and image-prompt guidance
- `scripts/fetch_ig_data.py`: multi-account Instagram collection
- `scripts/build_idea_context.py`: source and archive synthesis
- `scripts/run_weekly.ps1`: one-command weekly preparation
- `scripts/recent_posts.json`: fetched source data, generated at runtime
- `scripts/idea_context.json`: compact generation context, generated at runtime
- `ideas/`: current ideas
- `ideas/used/`: archived ideas
- `ideas/used_ideas_index.json`: durable anti-repetition index

## Idea quality bar

Each idea must be useful without selling, specific enough to recognize oneself in, grounded in credible context, distinct from the archive, and paired with a production-ready image prompt. Product presence is optional and should never be forced.
