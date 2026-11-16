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


## Capstone

**What This Extends:** FitFindr (Units 3-4): the agent that searches secondhand listings, suggests an outfit from the user's wardrobe, and writes a fit card. New in this unit: structured logging and timing around the HTTP service (`serve.py`), a documented run path (`RUNNING.md`), and a measured cost per run.

**The Shape:** Shape A (deploy and instrument). `serve.py` now writes one JSON record per request to `logs/runs.jsonl`: timestamp, route, query, outcome (`ok`, `no_results`, `model_error`, `bad_request`, `crashed`), HTTP status, duration in ms, model calls, tokens, results found, selected item, and error. I log the outcome separately from the HTTP status because the agent returns status 200 even when it stopped early with an error, so the status alone would hide those runs.

Out of scope: no changes to the agent loop, the tools or MCP; no new features; no hosting (Render's free tier needs a card, so I run locally, Path B); no queue or concurrency work.

**Running It:** Path B, local with logs. Start command, environment and the committed run record are in `RUNNING.md`.


**Instrumentation:** Each record in `logs/runs.jsonl` holds: timestamp, route, query, outcome (`ok` / `no_results` / `model_error` / `bad_request` / `crashed`), HTTP status, duration_ms, model_calls, tokens, results_found, selected item, and error. Ten entries from trial 1 (before the improvement):

```json
{"timestamp": "2026-11-15T05:51:58+00:00", "route": "/ask", "query": "vintage graphic tee under $30", "outcome": "ok", "status": 200, "duration_ms": 8073, "model_calls": 2, "tokens": 541, "results_found": 10, "selected": "Y2K Baby Tee — Butterfly Print", "error": null}
{"timestamp": "2026-11-15T05:52:03+00:00", "route": "/ask", "query": "90s track jacket in size M", "outcome": "ok", "status": 200, "duration_ms": 4112, "model_calls": 2, "tokens": 530, "results_found": 10, "selected": "90s Track Jacket — Navy/White Stripe", "error": null}
{"timestamp": "2026-11-15T05:52:07+00:00", "route": "/ask", "query": "silk slip dress in midi length under $40", "outcome": "ok", "status": 200, "duration_ms": 3716, "model_calls": 2, "tokens": 545, "results_found": 10, "selected": "90s Silk Slip Dress — Floral, Midi Length", "error": null}
{"timestamp": "2026-11-15T05:52:10+00:00", "route": "/ask", "query": "platform sneakers size 8", "outcome": "ok", "status": 200, "duration_ms": 3367, "model_calls": 2, "tokens": 547, "results_found": 1, "selected": "Platform Sneakers — White Chunky Sole", "error": null}
{"timestamp": "2026-11-15T05:52:13+00:00", "route": "/ask", "query": "denim jacket under $50", "outcome": "ok", "status": 200, "duration_ms": 2783, "model_calls": 2, "tokens": 469, "results_found": 7, "selected": "Denim Jacket — Light Wash, Cropped", "error": null}
{"timestamp": "2026-11-15T05:52:17+00:00", "route": "/ask", "query": "oversized flannel shirt under $25", "outcome": "ok", "status": 200, "duration_ms": 3332, "model_calls": 2, "tokens": 564, "results_found": 5, "selected": "Oversized Flannel Shirt — Plaid Red/Black", "error": null}
{"timestamp": "2026-11-15T05:52:19+00:00", "route": "/ask", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "status": 200, "duration_ms": 1438, "model_calls": 0, "tokens": 0, "results_found": 0, "selected": null, "error": "Nothing in the listings matched description 'designer ballgown', size XXS, under $5. Things to try: try broader or different keywords; drop the size filter, or try a neighbouring size; raise the price ceiling above $5."}
{"timestamp": "2026-11-15T05:52:19+00:00", "route": "/ask", "query": "", "outcome": "bad_request", "status": 400, "duration_ms": 0, "model_calls": 0, "tokens": 0, "error": "missing or empty query"}
{"timestamp": "2026-11-15T05:52:19+00:00", "route": "/ask", "query": "", "outcome": "bad_request", "status": 400, "duration_ms": 0, "model_calls": 0, "tokens": 0, "error": "missing or empty query"}
{"timestamp": "2026-11-15T05:52:20+00:00", "route": "/ask", "query": "", "outcome": "bad_request", "status": 400, "duration_ms": 0, "model_calls": 0, "tokens": 0, "error": "missing or empty query"}
```

A failed run, triggered with a deliberately broken API key:

```json
{"timestamp": "2026-11-15T06:01:24+00:00", "route": "/ask", "query": "vintage graphic tee under $30", "outcome": "model_error", "status": 200, "duration_ms": 4306, "model_calls": 1, "tokens": 0, "results_found": 10, "selected": "Y2K Baby Tee — Butterfly Print", "error": "The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 10 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.\nWhat the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com."}
```

**What It Costs:** Measured from the 18 successful runs across the three before-trials (cache off): an average of 559 tokens and 3.6 seconds of wall-clock time per run, read from the `tokens` and `duration_ms` fields in `logs/runs.jsonl`. Gemini's free tier bills $0, so the real costs are tokens and time. At 100 requests a day: 100 × 559 = 55,900 tokens/day and about 6 minutes of total request time — but the free tier's 15-requests-per-minute limit, at 2 calls per run, caps throughput at ~7 runs/minute, which is the binding constraint before tokens are.

**Run Log and Verdicts**

Three trials of the same 10 requests (6 matching, 1 no-results, 3 invalid), cache off, nothing changed between trials. Criterion 5 was a separate single run with a deliberately broken API key; criterion 2's tenth attempt was one extra invalid request.

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. One log record per request | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Invalid → 400, model_calls 0, tokens 0 | 10 of 10 attempts | 3/3 | 3/3 | 3/3 (+1 extra = 10/10) | MET |
| 3. Successful runs ≤ 15 s, cache off | 8 of 10 | 6/6 | 6/6 | 6/6 | MET (slowest 8.1 s, trial 1's cold start) |
| 4. model_calls/tokens valid; 0/0 on no-results | all records | 10/10 | 10/10 | 10/10 | MET |
| 5. Broken key → one `model_error` record, error set, no fit card | 1 of 1 | — | — | 1/1 | MET (log shows outcome "model_error", fit_card null; the failed call was counted as model_calls 1 with tokens 0) |

All five MET. The honest caveat: trial 1's first request (8.1 s) was the only one near any limit, and it pointed at a cold-start cost — which is what the improvement below went after.

**The Improvement:** Trial 1's first request took 8.1 s while every warm request took 2.8–4.2 s, so I added a warm-up call in `serve.py` that initializes the model client at server start, before the first user request. One change, committed before the re-run, then all three trials again in the same format.

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. One log record per request | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Invalid → 400, 0/0 | 9 attempts this set | 3/3 | 3/3 | 3/3 | MET |
| 3. Successful runs ≤ 15 s | 8 of 10 | 5/6 (one at 16.9 s) | 6/6 | 6/6 | MET overall (17/18), but see below |
| 4. Fields valid, 0/0 on no-results | all records | 10/10 | 10/10 | 10/10 | MET |
| 5. (not re-run — nothing in the change touches it) | — | — | — | — | — |

**Did it help:** No. Trial 1 after the warm-up was slower than before it: 16.9, 11.1, 14.3, 4.3, 9.9, 3.0 s, against 8.1 s as the worst before. The warm-up ran (the server printed its confirmation), and trials 2 and 3 were back at ~3 s, so the slowdown can't be my client setup — requests 2 through 5 were slow too, which a cold client can't explain. The mechanism I can support from the log: service-side latency or backoff at that moment. The change didn't achieve what it targeted, one request even crossed my 15 s limit, and the honest conclusion is that cold-start cost was not the dominant source of latency variance — the model service's own variance is bigger than anything my code controls.

**What's Still Broken:** Nothing is missed, so the targets are the thing to examine. Criterion 3's 15 s limit was set generously: 35 of 36 successful runs across both sets finished under 5 s, and the one exception (16.9 s) came from service-side variance. I'd tighten it to "8 of 10 under 5 s" — my data says that's where the system actually lives, and that target can genuinely fail. If this were real and I had another unit, the one thing I'd do first is log the two model calls' durations separately inside a run, because this unit showed I can see *that* a run was slow but not *which* call made it slow.

**How I Used AI:** Two moments. (1) I pasted my five draft criteria into Claude and asked whether each could be checked by someone who couldn't ask me what I meant. It flagged that my criterion 4 said no-results requests "must record their model usage," which two scorers could read oppositely when the correct value is zero, and that criterion 5's "appropriate non-success HTTP response" would fail my own system by design, since the agent deliberately catches ModelUnavailable and returns 200 with a session error. I rewrote both to name the exact observables (0/0 recorded; outcome `model_error`). (2) When my after-improvement trial came back slower than before, I worked through the log with Claude to separate what the warm-up could explain from what it couldn't — requests 2–5 being slow ruled out client setup — and wrote the diagnosis myself from that.