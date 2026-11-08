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

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

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
