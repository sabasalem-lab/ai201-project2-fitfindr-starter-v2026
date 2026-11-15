# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. Something about state

Given a listing is returned by search_listings, the exact same listing data (including its ID and attributes) is passed to suggest_outfit without being modified — in 5 of 5 tries.


**Why this target:**

To verify that the agent preserves the original listing data throughout the tool chain without accidentally changing or substituting the selected item.

---

## 4. Something about the fit card

Given the same item, 5 separate calls to create_fit_card produce 5 different captions (no two identical), and every caption contains the item's name and price — in 5 of 5 tries.


**Why this target:**

To verify that the model generates varied captions while consistently retaining the essential item information.

---

## 5. Your choice

Given a valid listing is found, the generated fit card contains all four required fields: item name, price, size, and fit recommendation — in 5 of 5 tries.

**Why this target:**

To ensure every successful fit card includes all the information needed for the user to evaluate the recommendation.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


## Capstone criteria

1. Logging reliability
Criterion: In 10 consecutive requests, every request must produce exactly one corresponding JSON record in `logs/runs.jsonl`. The 10 requests must include at least one successful request, one no-results query, and one empty query.
Why this target: Logging is a major part of my capstone extension. Testing different request outcomes ensures that both successful and unsuccessful requests are recorded reliably. Missing or duplicated records would make performance evaluation less trustworthy.
2. Invalid request handling
Criterion: An empty query or a request with a missing query field must return an HTTP 400 response in all 10 test attempts. Each attempt must be recorded in the log with `model_calls: 0` and `tokens: 0`.
Why this target: Invalid requests should be rejected before reaching the model. This prevents unnecessary API usage and makes the system's behavior predictable.
3. Request execution time
Criterion: With caching disabled, at least 8 out of 10 successful requests must complete within 15 seconds, measured using the `duration_ms` field in `logs/runs.jsonl`.
Why this target: Since the system makes external model API calls, response time affects usability. A 15-second limit provides a measurable performance target while allowing some variation in API response times.
4. Model call and token tracking
Criterion: Every completed request must have `model_calls` and `tokens` fields containing nonnegative integer values in its log record. A no-results request that does not call the model must record `model_calls: 0` and `tokens: 0`.
Why this target: Tracking model calls and tokens helps measure API usage and understand the cost of running the system. Recording zero usage for requests that do not require the model is just as important as recording actual usage.
5. Model/API failure handling
Criterion: When the model API is unavailable, tested by intentionally changing one character of the API key, the application must record exactly one log entry with `outcome: "model_error"`. The response must contain an error field and must not return a fit card as a successful result.
Why this target: External APIs can become unavailable or authentication can fail. The application should identify these situations, communicate the error, and preserve the failure information in its logs instead of incorrectly reporting a successful result.