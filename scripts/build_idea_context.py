#!/usr/bin/env python3
"""Build compact source and archive context for weekly idea generation."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
POSTS_PATH = ROOT / "scripts" / "recent_posts.json"
INDEX_PATH = ROOT / "ideas" / "used_ideas_index.json"
OUTPUT_PATH = ROOT / "scripts" / "idea_context.json"
STOPWORDS = {
    "this", "that", "with", "from", "your", "you", "the", "and", "for", "are",
    "our", "can", "how", "more", "when", "what", "just", "have", "has", "het",
    "een", "van", "voor", "met", "dat", "die", "zijn", "yourself", "about",
}


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return fallback


def tokens(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{2,}|[\u4e00-\u9fff]{2,}", text.lower())
    return [word for word in words if word not in STOPWORDS and not word.startswith("http")]


def engagement(post: dict[str, Any]) -> int:
    return int(post.get("likes") or 0) + 3 * int(post.get("comments") or 0)


def main() -> int:
    source = load_json(POSTS_PATH, {"posts": []})
    archive = load_json(INDEX_PATH, {"ideas": []})
    posts = source.get("posts", [])
    by_account: dict[str, list[dict[str, Any]]] = defaultdict(list)
    word_counts: Counter[str] = Counter()
    for post in posts:
        by_account[post.get("account") or "unknown"].append(post)
        word_counts.update(tokens(post.get("caption") or ""))

    account_summary = {}
    for account, account_posts in sorted(by_account.items()):
        ranked = sorted(account_posts, key=engagement, reverse=True)
        account_summary[account] = {
            "post_count": len(account_posts),
            "top_posts": [
                {
                    "caption_excerpt": post.get("caption", "")[:320],
                    "url": post.get("url"),
                    "timestamp": post.get("timestamp"),
                    "engagement_signal": engagement(post),
                }
                for post in ranked[:3]
            ],
        }

    archived = archive.get("ideas", [])
    context = {
        "built_at": datetime.now(UTC).isoformat(),
        "source_fetched_at": source.get("fetched_at"),
        "source_post_count": len(posts),
        "accounts": account_summary,
        "frequent_terms": [word for word, _ in word_counts.most_common(30)],
        "archive_count": len(archived),
        "recent_archive": archived[-50:],
    }
    OUTPUT_PATH.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote context for {len(posts)} posts and {len(archived)} archived ideas to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
