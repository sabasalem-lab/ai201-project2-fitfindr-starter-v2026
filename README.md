# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user describes an item they're looking for in plain language - something
like "a vintage graphic tee under $30, size M". FitFindr searches real
secondhand listings for matches, works out what the found item would pair
well with from a small wardrobe, and writes a short caption someone could
actually post alongside it. If nothing in the listings matches, it stops
and tells the user what to change instead of guessing.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for items matching a text description, a requested size, and a maximum price.
- **Inputs:** `description` (str) — keywords to match against title, description, and style_tags; `size` (str) — the requested size, matched as a substring against the listing's size field; `max_price` (float) — the highest acceptable price, inclusive.
- **Returns:** A list of listing dicts. Each dict contains `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, `platform`.
- **When it has nothing:** An empty list `[]`.

### `suggest_outfit`

- **What it does:** Takes a found listing and a wardrobe, and asks the model for outfit pairing ideas using what's already owned.
- **Inputs:** `new_item` (dict) — a single listing dict, in the same shape `search_listings` returns; `wardrobe` (dict) — a dict with an `items` key holding a list of wardrobe item dicts, each with `id`, `name`, `category`, `colors`, `style_tags`, `notes`.
- **Returns:** A string containing 2–3 sentences of outfit suggestions, referencing specific wardrobe items by name where relevant.
- **When it has nothing:** If `wardrobe["items"]` is an empty list, returns general styling advice for the item instead of failing or returning an empty string.


### `create_fit_card`

- **What it does:** Writes a short, postable caption combining the new item and the suggested outfit.
- **Inputs:** `outfit` (str) — the outfit suggestion text from `suggest_outfit`; `new_item` (dict) — the same listing dict used above.
- **Returns:** A single string, 1–3 sentences, written in a casual, social-media-caption tone, mentioning the item by name.
- **When it has nothing:** If `outfit` is an empty string, returns a caption describing just the item on its own, without outfit pairing language.

## Planning Loop

**Branch rule:** If search_listings returns an empty list, the loop puts a message in session["error"] naming what the user could change (the description, size, and/or price ceiling that were in play) and returns the session without calling suggest_outfit. Otherwise, it takes the first result, puts it in session["selected_item"], and continues through suggest_outfit and create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. parse_query() in agent.py extracts a price ceiling (matching patterns like "under $30") and a size (matching "size M") from the plain-language query, leaving the remainder as the description. I chose regex over asking the model because it's free, deterministic (the same query always parses the same way, which matters for testing the state criterion), and any parsing mistake is visible in the pattern rather than hidden in a model's judgment.

**What moves through the session:** query → parsed (description/size/max_price) → search_results → selected_item → outfit_suggestion → fit_card. If the branch triggers early, error is set and outfit_suggestion/fit_card stay None.
---

## Sample Run

**One full query**

$ python agent.py
=== A query the data can match ===
found: Y2K Baby Tee — Butterfly Print — $18.0 on depop
outfit: Pair the Y2K butterfly baby tee with your baggy straight-leg jeans and chunky white sneakers for a classic, nostalgic streetwear look. Layer the black cropped zip hoodie over the tee and add the black crossbody bag to complete an easy, balanced outfit with your wide-leg khaki trousers.
fit card: Just scored this adorable Y2K butterfly baby tee on Depop for only $18! Obsessed with the ultimate nostalgic streetwear vibe. Already planning to wear it with baggy denim and chunky sneakers. 🦋✨

=== A query it can’t ===
stopped: Nothing in the listings matched description ‘designer ballgown’, size XXS, under $5. Things to try: try broader or different keywords; drop the size filter, or try a neighbouring size; raise the price ceiling above $5.
fit_card is None — it should still be None here


**The three tools, tested one at a time**

$ python test_tools.py
=== search_listings ===
Found 6 result(s)

Y2K Baby Tee — Butterfly Print ($18.0)
Graphic Tee — 2003 Tour Bootleg Style ($24.0)
Mesh Long-Sleeve Top — Black ($15.0)
Vintage Band Tee — Faded Grey ($19.0)
Low-Rise Cargo Pants — Khaki ($27.0)
Vintage Graphic Hoodie — Faded Black ($26.0)

=== suggest_outfit ===
Outfit 1: Casual Streetwear
Pair the vintage Levi’s 501 jeans with the white ribbed tank top and chunky white sneakers, layering the black cropped zip hoodie on top for an effortless, everyday look. Accessorize with the black crossbody bag to complete the casual aesthetic.

Outfit 2: Edgy Vintage
Combine the medium wash jeans with the oversized grey crewneck sweatshirt and black combat boots for a relaxed yet structured vibe. Throw on the vintage black denim jacket and thread the brown leather belt through the loops to tie the textures together.

=== create_fit_card ===
Found these vintage Levi’s 501 jeans for just $38 and I’m literally never taking them off. Obsessed with the medium wash for putting together that effortless, edgy streetwear vibe. Just listed them on my depop if you need a new go-to pair!


## How I Used AI

**Moment 1**

I asked Claude to implement search_listings, suggest_outfit, and create_fit_card based on my own Tool Inventory specs. It built a size-matching approach using whole-token comparison (so "M" matches "S/M" but doesn't falsely match inside "US 9"), which matched the exact warning in the tools.py docstring about naive substring matching.

**Moment 2**

Claude's first version of search_listings put `import re` inside an if-block, which caused an UnboundLocalError when the function reached a later line using `re` outside that block. I had Claude explain the bug and fix it by moving the import to the top of the file.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->


## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes, returns fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. State integrity (same item unchanged) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. 5 different captions, each names item + price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Fit card has name, price, size, fit recommendation | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |

**Real output from one try**, produced by `tools.py::create_fit_card` (criterion 5, try 1, before the fix):

Found this absolute dream of a cropped light wash denim jacket on Poshmark and I’m obsessed! It’s an XL, finished off with wide-leg khaki trousers. Giving major effortless-chic off-duty model vibes for spring. Grab it before I change my mind and keep it for myself! ✨

No size is mentioned anywhere in this caption, even though the selected listing's `size` field was `"S"`.

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes, returns fit card | 4/5 | MET | All 5 tries produced a complete session with a non-empty fit_card. |
| 2 | Impossible query stops before suggest_outfit | 5/5 | MET | All 5 tries triggered the branch and stopped with fit_card still None. |
| 3 | State integrity (same item unchanged) | 5/5 | MET | All 5 tries showed the exact same item dict in select_item's output and in suggest_outfit's and create_fit_card's inputs. |
| 4 | 5 different captions, each names item + price | 5/5 | MET | All 5 captions in the "fit card wording varies" scenario were distinct strings, and each mentioned the price ($22) and a recognizable reference to the item (e.g. "red and black flannel"). |
| 5 | Fit card has name, price, size, fit recommendation | 5/5 | MISSED (0/5) | None of the 5 fit cards mentioned the item's size, even though the listing data had a real size value ("S"). |

**Diagnoses**

Criterion 5 missed on 5 of 5 tries. The tool worked correctly — `search_listings` returned a listing with a real `size: "S"` field, and that field was available in `new_item` when `create_fit_card` ran. The failure was in `create_fit_card`'s prompt construction in `tools.py`: the prompt sent to the model only included `title`, `price`, `platform`, and the outfit suggestion — it never named `size` as a field to mention, and the fallback message (used when `outfit` is empty) also omitted it. The model had no way to know size mattered, since it was never told the size existed. This is a single, consistent cause across all 5 tries, not five separate problems.

## Loop Trace

**Happy path**

```
[1] parse_query
in: looking for a vintage graphic tee under $30
out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
in: dict with keys: description, size, max_price
out: 10 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, Graphic Tee — 2003 Tour Bootleg Style … +7 more
→ 10 match(es)
[3] select_item
out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
in: Y2K Baby Tee — Butterfly Print ($18.0, depop)
out: Pair the Y2K butterfly baby tee with your baggy straight-leg jeans and chunky white sneakers for a classic, no…
[5] create_fit_card
in: Y2K Baby Tee — Butterfly Print ($18.0, depop)
out: Just scored this adorable Y2K butterfly baby tee on Depop for only $18! Obsessed with the ultimate nostalgic s…
```

**Empty search**

```
[6] parse_query
in: designer ballgown size XXS under $5
out: dict with keys: description, size, max_price
[7] search_listings (via MCP)
in: dict with keys: description, size, max_price
out: [] (empty)
→ 0 match(es)
[8] branch
→ search returned []: stopping before suggest_outfit
```


The empty-search path is 3 trace steps; the happy path is 5. The branch is visibly doing work — it stops two steps early rather than running the full chain.

**On the MCP move:** I moved `search_listings` onto MCP, registering it in `mcp_server.py` with its name, a description written for a reader who can't see the code, and typed inputs matching my Tool Inventory. `agent.py::run_agent` now calls it through `mcp_client.call_tool()`, falling back to the direct function call if MCP is unreachable. One real behavior difference showed up: through MCP, `search_listings` returned 10 results for the same query that returned 6 through the direct call before the rewire. That difference is a genuine finding — it suggests the direct call path was applying `config.SEARCH_RESULT_LIMIT` in a way that isn't happening through the MCP path, or the two paths aren't using identical logic somewhere. I haven't tracked down the exact cause yet; the branch and downstream tools all still function correctly regardless of which count comes back, so this didn't block the rest of the loop, but it's a real inconsistency worth investigating further.

**All three failure modes, triggered and handled:**

1. **Empty search** — shown above in Loop Trace. The branch stops cleanly before `suggest_outfit`, with a message naming what to change.
2. **Empty wardrobe** — tested by running `suggest_outfit` with `get_empty_wardrobe()` instead of `get_example_wardrobe()`. The tool returned general styling advice instead of crashing or returning an empty string, and the rest of the pipeline continued normally.
3. **Model unavailable** — tested by temporarily corrupting `GEMINI_API_KEY` in `.env` and running a new, uncached query. The agent returned a clean error message, not a stack trace, and preserved the search results from before the failure.

---## The Improvement

**What I changed:** I added the item's `size` field to the prompt sent to the model in `create_fit_card`, and explicitly instructed the model to mention the item, the size, the price, and the platform. I also added size to the non-model fallback message used when `outfit` is empty.

**Which failure it was meant to fix:** Criterion 5 — the fit card was missing the size field entirely, 0 of 5 tries, because the prompt never told the model size was available or that it should be mentioned.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes, returns fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. State integrity (same item unchanged) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. 5 different captions, each names item + price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Fit card has name, price, size, fit recommendation | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes. Criterion 5 went from 0/5 to 5/5. Every fit card in the "fit card has all required fields" scenario now explicitly mentions the size (e.g. "It's a size S and only set me back $42.0"). This was a one-line cause with a one-line fix: the data was always there, the prompt just needed to ask for it.

---
## What's Still Broken

All 5 criteria are MET after the improvement. The one open item is the MCP result-count discrepancy noted under "On the MCP move" — the MCP path returns more results (10) than the direct call did (6) for the same query. It doesn't cause any criterion to fail and doesn't affect the branch logic, but it means the two code paths aren't behaving identically, which could matter if `SEARCH_RESULT_LIMIT` is meant to be a hard cap. I'd track this down by comparing `search_listings`'s direct return value against what comes back through `mcp_client.call_tool()` for the same inputs, to see where the counts diverge. 

═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
