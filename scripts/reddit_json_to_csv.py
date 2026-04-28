import json
import csv
import os
from typing import Any, Dict, List, Optional


def flatten_comments(children: List[Dict[str, Any]], rows: List[Dict[str, Any]], default_link_id: Optional[str] = None, depth: int = 0) -> None:
    for child in children:
        if child.get("kind") != "t1":
            continue
        data = child.get("data", {})
        # Extract fields with sensible defaults
        row = {
            "id": data.get("id"),
            "author": data.get("author"),
            "is_submitter": data.get("is_submitter"),
            "score": data.get("score"),
            "ups": data.get("ups"),
            "downs": data.get("downs"),
            "created_utc": data.get("created_utc"),
            "permalink": data.get("permalink"),
            "parent_id": data.get("parent_id"),
            "link_id": data.get("link_id") or default_link_id,
            "depth": data.get("depth", depth),
            "subreddit_name_prefixed": data.get("subreddit_name_prefixed"),
            "body": data.get("body"),
        }
        rows.append(row)

        # Recurse into replies if present
        replies = data.get("replies")
        if isinstance(replies, dict):
            replies_data = replies.get("data", {})
            replies_children = replies_data.get("children", [])
            flatten_comments(
                replies_children,
                rows,
                default_link_id=row["link_id"],
                depth=row["depth"] + 1 if isinstance(row["depth"], int) else depth + 1,
            )


def main() -> None:
    project_root = "/Users/zacharygeleott/Downloads/TakeOff - LandTrust"
    input_path = os.path.join(project_root, "Miscellaneous Reports", "Reddit_Beginning_of_the_End.json")
    output_path = os.path.join(project_root, "Miscellaneous Reports", "Reddit_Beginning_of_the_End_comments.csv")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Expect top-level list: [post Listing, comments Listing]
    link_id = None
    if isinstance(data, list) and len(data) >= 1:
        # Try to read post id to set link_id
        try:
            post_children = data[0]["data"]["children"]
            if post_children and post_children[0]["kind"] == "t3":
                link_id = post_children[0]["data"].get("name")  # e.g., t3_1c2a0xd
        except Exception:
            link_id = None

    comment_listing = None
    if isinstance(data, list) and len(data) >= 2:
        comment_listing = data[1]
    elif isinstance(data, list) and len(data) == 1:
        comment_listing = data[0]

    rows: List[Dict[str, Any]] = []
    if comment_listing:
        try:
            children = comment_listing["data"]["children"]
        except Exception:
            children = []
        flatten_comments(children, rows, default_link_id=link_id, depth=0)

    fieldnames = [
        "id",
        "author",
        "is_submitter",
        "score",
        "ups",
        "downs",
        "created_utc",
        "permalink",
        "parent_id",
        "link_id",
        "depth",
        "subreddit_name_prefixed",
        "body",
    ]

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} comments to {output_path}")


if __name__ == "__main__":
    main()


