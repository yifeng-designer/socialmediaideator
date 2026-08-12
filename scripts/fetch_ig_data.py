#!/usr/bin/env python3
"""Fetch recent Instagram posts from a diversified reference pool via Apify."""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping

from apify_client import ApifyClient


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "recent_posts.json"
TARGET_ACCOUNTS = [
    "thebreathworkmovement",
    "glimp.health",
    "moonbird.life",
    "somnox.sleep",
    "kaspersfocus",
    "headspace",
    "calm",
    "breathwrk",
]
ACTOR_ID = os.getenv("APIFY_INSTAGRAM_ACTOR", "apify/instagram-scraper")
LOOKBACK_DAYS = int(os.getenv("IG_LOOKBACK_DAYS", "45"))
RESULTS_PER_ACCOUNT = int(os.getenv("IG_RESULTS_PER_ACCOUNT", "12"))


def parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def normalize(item: dict[str, Any]) -> dict[str, Any]:
    owner = item.get("ownerUsername") or item.get("username") or item.get("owner", {}).get("username")
    caption = item.get("caption") or item.get("text") or ""
    return {
        "account": owner,
        "timestamp": item.get("timestamp") or item.get("takenAt"),
        "caption": caption.strip(),
        "url": item.get("url") or item.get("shortCodeUrl") or item.get("displayUrl"),
        "type": item.get("type") or item.get("productType"),
        "likes": item.get("likesCount") or item.get("likes") or 0,
        "comments": item.get("commentsCount") or item.get("comments") or 0,
    }


def default_dataset_id(run: Any) -> str:
    """Return the default dataset ID from Apify client v2 or v3 run results."""
    if isinstance(run, Mapping):
        dataset_id = run.get("defaultDatasetId")
    else:
        dataset_id = getattr(run, "default_dataset_id", None)
    if not dataset_id:
        raise RuntimeError("Apify run did not provide a default dataset ID.")
    return str(dataset_id)


def main() -> int:
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        print("APIFY_API_TOKEN is required.", file=sys.stderr)
        return 2

    client = ApifyClient(token)
    run_input = {
        "directUrls": [f"https://www.instagram.com/{account}/" for account in TARGET_ACCOUNTS],
        "resultsType": "posts",
        "resultsLimit": RESULTS_PER_ACCOUNT,
        "searchType": "user",
        "searchLimit": len(TARGET_ACCOUNTS),
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    cutoff = datetime.now(UTC) - timedelta(days=LOOKBACK_DAYS)
    posts = []
    for raw in client.dataset(default_dataset_id(run)).iterate_items():
        post = normalize(raw)
        timestamp = parse_timestamp(post["timestamp"])
        if post["account"] and post["caption"] and (timestamp is None or timestamp >= cutoff):
            posts.append(post)

    posts.sort(key=lambda post: post.get("timestamp") or "", reverse=True)
    payload = {
        "fetched_at": datetime.now(UTC).isoformat(),
        "lookback_days": LOOKBACK_DAYS,
        "target_accounts": TARGET_ACCOUNTS,
        "post_count": len(posts),
        "posts": posts,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(posts)} posts to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
