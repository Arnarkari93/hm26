---
name: predict-score
description: Predicts WC 2026 scorelines — either all matches on a given date (or today by default), or a specific match between two named teams. Triggers on: "predict today's games", "what games are on today", "predict June 21 matches", "who plays today", "predict [Team A] vs [Team B]", "what's the score", "who wins today", or any request to forecast/guess WC 2026 match results. When no teams are named and a date or "today" is implied, look up the day's fixtures and predict all of them.
---

# Score Predictor — WC 2026

Predict scorelines using a **Poisson goal model** driven by per-team attack
(`gf_per_match`) and defense (`ga_per_match`) rates.

## Determine mode

**Date mode** (default when no specific teams are named, or user says "today" / gives a date):
→ Go to Step 0 to get the fixture list, then run Steps 1–6 for each match.

**Single-match mode** (user names two specific teams):
→ Skip to Step 1 with those two teams.

---

## Step 0 (date mode only): Get today's fixtures

1. Check `actual-results.md` — any matches listed for this date are already played; note them but don't re-predict.
2. WebSearch: `"World Cup 2026" fixtures "[date]"` (e.g. `"World Cup 2026" fixtures "June 21"`)
   - Extract the list of matches scheduled for that date
   - Cross-reference with `groups.md` / `knockout.md` to confirm group/stage
3. If no matches found for the date, say so and stop.
4. Run Steps 1–6 for each unplayed match in sequence. Collect all outputs, then print them together (Step 5 format for each), then save each one (Step 6).

---

## Step 1: Load context

- `team-rates.csv` — per-team attack/defense rates (the model's core input)
- `groups.md` / `knockout.md` — form notes, prep results, confidence labels
- `actual-results.md` — already-played results (don't re-predict a played game; cite the actual)

If a team isn't in `countries.csv`, say so and skip that match.

## Step 2: Run the model

```
python3 scripts/predict.py "Team A" "Team B" [flags]
```

Flags:
- `--hostA` / `--hostB` — team is a host (USA, Mexico, Canada): +15% attack, opponent suppressed
- `--formA <m>` / `--formB <m>` — multiplier on a team's expected goals (default 1.0)
- `--knockout` — knockout match: tighter game + pens note if draw is live

Set **form multipliers from `groups.md` / `knockout.md` notes**:
- "on fire / dominant prep / unbeaten streak" → `--formA 1.15`
- "worst form / lost all prep / catastrophic" → `--formB 0.85`
- neutral / no note → leave at 1.0

The script prints expected goals, modal scoreline, full W/D/L probabilities,
top-5 scorelines, P(over 2.5), and P(BTTS).

## Step 3: Pick the scoreline to report

- **Default:** report the script's modal scoreline.
- If a strong attacker meets a weak defense (xG ≥ ~2.3) and form agrees, report one goal above mode (e.g. 3-1) and say so.
- Always quote W/D/L probabilities — more honest than the exact score.

## Step 4: Confidence + odds check

Confidence label comes from win-probability margin (High ≥40pts / Medium ≥20 / Low <20).
If **Low**, or form signals conflict with the model:
- WebSearch: `"[Team A] vs [Team B]" World Cup 2026 odds prediction score`
- Look for Opta / ESPN / DraftKings / Bet365; extract implied win % or predicted score
- Reconcile with the model; if they disagree sharply, say so

In date mode with many matches: skip odds search for High/Medium confidence games; only search for Low confidence ones.

## Step 5: Output (per match)

```
**[Team A] vs [Team B]**
Predicted score: [Team A] X – Y [Team B]
Confidence: [High / Medium / Low] (~XX%)
Win prob: A NN% / draw NN% / B NN%   ·   P(BTTS) NN%  ·  P(o2.5) NN%

Reasoning:
- Model: xG [Team A] X.X – Y.Y [Team B] (rates gf/ga A: a/d, B: a/d)
- [1-2 form/context notes from project data that set the form multipliers]
- [If searched: "Markets: DraftKings Team A -150 (~55%)"]
```

Keep reasoning to 3-4 bullets. No padding. In date mode, print all match blocks together under a `## [Date] Predictions` header.

## Step 6: Save prediction

Write to:
- Group stage: `./predicted-scores/groupstage/teama-vs-teamb.md`
- Knockout: `./predicted-scores/knockoutstage/teama-vs-teamb.md`

Filename: lowercase, hyphenated, e.g. `canada-vs-bosnia-and-herzegovina.md`.
Content: the Step 5 block. Create the directory if missing.

## Step 7 (when a predicted game is later played): update rates from actuals

`team-rates.csv` ships with `source=elo-prior` rates. As real games happen, sharpen rates:
- Blend actual goals-for/against into `gf_per_match` / `ga_per_match`, bump `sample_matches`, set `source=blended`.

## Notes

- Extra time / penalties in knockout: predict 90-min score; flag if "could go to pens"
- Don't invent data — if no form note exists, leave multiplier at 1.0 and say so
- Rates are Elo-priors for un-played teams; treat exact scorelines as modal guesses, lead with probabilities
