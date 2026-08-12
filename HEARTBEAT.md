# Weekly Idea Heartbeat

When the weekly content heartbeat runs:

1. Run `powershell -ExecutionPolicy Bypass -File scripts/run_weekly.ps1`.
2. Read `workflow_prompt.md` and all context it requires.
3. Generate the requested number of idea files.
4. Update `ideas/used_ideas_index.json`.
5. Report source coverage, generated filenames, and any fetch limitations.

Do not silently reuse old `scripts/recent_posts.json` if fetching fails. State its timestamp and whether the batch relies on stale context.
