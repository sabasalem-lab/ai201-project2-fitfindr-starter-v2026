"""
The FitFindr planning loop.
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.
    """
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── parsing the query ──────────────────────────────────────────────────────────

_PRICE_RE = re.compile(r"(?:under|below|less than|max|up to)?\s*\$\s*(\d+(?:\.\d+)?)", re.I)
_SIZE_RE = re.compile(r"\bsize\s+([A-Za-z0-9/]+)\b", re.I)


def parse_query(query: str) -> dict:
    """
    Pull a description, a size and a price ceiling out of what the user typed.

    Regex rather than a model call: it costs nothing, it's deterministic (the
    same query always parses the same way, which matters for testing), and
    when it gets something wrong the reason is visible in the pattern.
    """
    text = query or ""

    max_price = None
    price_match = _PRICE_RE.search(text)
    if price_match:
        max_price = float(price_match.group(1))
        text = text[: price_match.start()] + " " + text[price_match.end():]

    size = None
    size_match = _SIZE_RE.search(text)
    if size_match:
        size = size_match.group(1).strip()
        text = text[: size_match.start()] + " " + text[size_match.end():]

    description = re.sub(r"[,\s]+", " ", text).strip(" ,")
    return {"description": description, "size": size, "max_price": max_price}


def _nothing_found_message(parsed: dict) -> str:
    """
    What to say when the search comes back empty. Names what the user
    actually controls, not just "no results."
    """
    tried = [f"description '{parsed['description']}'"]
    if parsed["size"]:
        tried.append(f"size {parsed['size']}")
    if parsed["max_price"] is not None:
        tried.append(f"under ${parsed['max_price']:g}")

    suggestions = ["try broader or different keywords"]
    if parsed["size"]:
        suggestions.append("drop the size filter, or try a neighbouring size")
    if parsed["max_price"] is not None:
        suggestions.append(f"raise the price ceiling above ${parsed['max_price']:g}")

    return (
        "Nothing in the listings matched " + ", ".join(tried) + ". "
        "Things to try: " + "; ".join(suggestions) + "."
    )


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Branch rule: if search_listings returns an empty list, put a message in
    session["error"] naming what the user could change, and return the
    session without calling suggest_outfit. Otherwise take the first result,
    put it in session["selected_item"], and continue through all three tools.
    """
    session = new_session(query, wardrobe)
    steps = 0

    steps += 1
    trace.check_iterations(steps)
    parsed = parse_query(query)
    session["parsed"] = parsed

    steps += 1
    trace.check_iterations(steps)
    results = search_listings(
        parsed["description"], parsed["size"], parsed["max_price"]
    )
    session["search_results"] = results

    # ── THE BRANCH ──────────────────────────────────────────────────────────
    if not results:
        session["error"] = _nothing_found_message(parsed)
        return session

    steps += 1
    trace.check_iterations(steps)
    session["selected_item"] = results[0]

    steps += 1
    trace.check_iterations(steps)
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    steps += 1
    trace.check_iterations(steps)
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )