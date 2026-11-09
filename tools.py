"""
The three FitFindr tools.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.
    """
    listings = load_listings()

    results = []
    for item in listings:
        if max_price is not None and item["price"] > max_price:
            continue

        if size is not None:
            item_size = (item.get("size") or "").strip().lower()
            query_size = size.strip().lower()
            tokens = re.split(r"[^a-z0-9]+", item_size)
            if query_size not in tokens:
                continue

        results.append(item)

    keywords = set(re.split(r"\W+", description.lower())) if description else set()
    keywords.discard("")

    scored = []
    for item in results:
        haystack = " ".join([
            item.get("title", ""),
            item.get("description", ""),
            " ".join(item.get("style_tags", []) or []),
        ]).lower()
        haystack_words = set(re.split(r"\W+", haystack))
        score = len(keywords & haystack_words)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    limit = getattr(config, "SEARCH_RESULT_LIMIT", 5)
    return [item for _, item in scored[:limit]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """
    items = wardrobe.get("items") or []

    item_desc = f"{new_item.get('title', 'this item')} ({new_item.get('category', 'clothing')}, colors: {', '.join(new_item.get('colors', []) or [])})"

    if not items:
        prompt = (
            f"Someone is considering buying this secondhand item: {item_desc}. "
            f"They have no wardrobe info available. Suggest 1-2 general outfit "
            f"ideas or styling tips for this item, in 2-3 sentences."
        )
    else:
        wardrobe_desc = "\n".join(
            f"- {w.get('name', 'item')} ({w.get('category', '')}, colors: {', '.join(w.get('colors', []) or [])})"
            for w in items
        )
        prompt = (
            f"Someone is considering buying this secondhand item: {item_desc}.\n\n"
            f"Here is their existing wardrobe:\n{wardrobe_desc}\n\n"
            f"Suggest 1-2 specific outfit combinations using the new item and "
            f"pieces they already own. Name the wardrobe pieces by name. "
            f"Keep it to 2-3 sentences."
        )

    response = generate(prompt)
    return response.strip() if response else "No specific outfit ideas available right now."


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────
def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.
    """
    title = new_item.get("title", "this item")
    price = new_item.get("price", "?")
    platform = new_item.get("platform", "a resale app")
    size = new_item.get("size", "")

    if not outfit or not outfit.strip():
        return f"Found this: {title}, size {size}, for ${price} on {platform}. No outfit pairing yet, but it's a solid find on its own."

    prompt = (
        f"Write a short, casual social-media caption (2-4 sentences) for a "
        f"thrifted item someone just found. Write it like a real post, not a "
        f"product description.\n\n"
        f"Item: {title}\n"
        f"Size: {size}\n"
        f"Price: ${price}\n"
        f"Platform: {platform}\n"
        f"Outfit idea: {outfit}\n\n"
        f"Mention the item, the size, the price, and the platform once each, "
        f"and be specific about the vibe. Keep it casual and postable."
    )

    response = generate(prompt)
    return response.strip() if response else f"Just scored {title}, size {size}, for ${price} on {platform}!"