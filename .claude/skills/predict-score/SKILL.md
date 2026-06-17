---
name: predict-score
description: Predicts the scoreline for a World Cup 2026 match between two teams. Use this skill whenever the user asks to predict, forecast, or guess the score/result of a game, match, or fixture between two nations in this tournament. Input is two team names, output is a predicted scoreline with reasoning. Also triggers on prompts like "what will the score be", "who wins", "predict the match", "what's the result" for any two competing nations.
---

# Score Predictor — WC 2026

Predict a scoreline using a **Poisson goal model** driven by per-team attack
(`gf_per_match`) and defense (`ga_per_match`) rates — not Elo-diff rounding.
This gives underdogs a real scoring chance and captures high-scoring games
(Elo-diff systematically over-predicts clean sheets and under-predicts blowouts).

## Step 1: Load context

- `team-rates.csv` — per-team attack/defense rates (the model's core input)
- `groups.md` / `knockout.md` — form notes, prep results, confidence labels
- `actual-results.md` — already-played results (don't re-predict a played game; cite the actual)

If a team isn't in `countries.csv`, say so and decline.

## Step 2: Run the model

```
python3 scripts/predict.py "Team A" "Team B" [flags]
```

Flags:
- `--hostA` / `--hostB` — team is a host (USA, Mexico, Canada): +15% attack, opponent suppressed
- `--formA <m>` / `--formB <m>` — multiplier on a team's expected goals (default 1.0)
- `--knockout` — knockout match: tighter game + pens note if draw is live

Set the **form multipliers from `groups.md` / `knockout.md` notes**, e.g.:
- "on fire / dominant prep / unbeaten streak" → `--formA 1.15`
- "worst form / lost all prep / catastrophic" → `--formB 0.85`
- neutral / no note → leave at 1.0

The script prints expected goals, modal scoreline, full W/D/L probabilities,
top-5 scorelines, P(over 2.5), and P(BTTS).

## Step 3: Pick the scoreline to report

- **Default:** report the script's modal scoreline.
- Poisson modes cluster low (1-0, 1-1). If a strong attacker meets a weak
  defense (expected goals ≥ ~2.3) and form notes agree, it's fine to report a
  scoreline one goal above the mode (e.g. 3-1) and say so.
- Always quote the W/D/L probabilities — they're the honest signal, more than the exact score.

## Step 4: Confidence + odds check

The script labels confidence from the win-probability margin (High ≥40pts / Medium ≥20 / Low <20).
If **Low**, or if form signals conflict with the model, pull market data:
- WebSearch: `"[Team A] vs [Team B]" World Cup 2026 odds prediction score`
- Look for Opta / ESPN / DraftKings / Bet365 / FiveThirtyEight; extract implied win % or predicted score
- Reconcile with the model; if they disagree sharply, say so rather than hiding it

## Step 5: Output

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

Keep reasoning to 3-4 bullets. No padding.

## Step 6: Save prediction

Write to:
- Group stage: `./predicted-scores/groupstage/teama-vs-teamb.md`
- Knockout: `./predicted-scores/knockoutstage/teama-vs-teamb.md`

Filename: lowercase, hyphenated, e.g. `canada-vs-bosnia-and-herzegovina.md`.
Content: the Step 5 block. Create the directory if missing.

## Step 7 (when a predicted game is later played): update rates from actuals

`team-rates.csv` ships with `source=elo-prior` rates (Elo-seeded, reproducible via
`scripts/build_team_rates.py`). As real games happen, sharpen the rates so future
predictions improve:
- Blend the team's actual goals-for/against into `gf_per_match` / `ga_per_match`
  (e.g. weighted avg toward recent matches), bump `sample_matches`, set
  `source=blended` (or `actual` once prior is fully replaced).
- This is the data point we were missing — real per-team goal rates. The more
  real games folded in, the less the model leans on the Elo prior.

## Notes

- Extra time / penalties in knockout: predict 90-min score; flag if it "could go to pens"
- Don't invent data — if no form note exists for a team, leave its multiplier at 1.0 and say so
- Rates are currently Elo-priors for un-played teams; treat exact scorelines as modal guesses,
  not certainties — lead with probabilities
