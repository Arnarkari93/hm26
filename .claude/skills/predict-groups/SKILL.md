---
name: predict-groups
description: Predict 2026 World Cup group stage outcomes using FIFA rankings and recent form. Outputs a reordered group table with predicted points per team. Use when asked to predict group results, simulate the group stage, or forecast World Cup standings.
---

# WC Group Stage Predictor

## Quick start

Run against groups.md + fifa_rankings.csv in this repo:

1. Read `groups.md` for group compositions
2. Read `fifa_rankings.csv` for ELO-style ranking points
3. WebSearch recent form for each team (last 5–10 matches)
4. Predict each group's matches and output ranked table

## Workflow

### 1. Load data
- Read `groups.md`: 12 groups × 4 teams
- Read `fifa_rankings.csv`: rank + points per country

### 2. Research form (parallel)
For each team, WebSearch: `"[country] national football team results 2025 2026"`
Extract: W/D/L from last ~8 matches, goals scored/conceded

### 3. Predict matches
For each group, simulate all 6 matches (round-robin):

**Match outcome formula:**
- Base probability from Elo point difference:
  - `p_win = 1 / (1 + 10^((opp_pts - team_pts) / 600))`
- Adjust ±5–10% based on recent form
- Classify as W/D/L using thresholds:
  - p_win > 0.58 → win
  - p_win < 0.42 → loss
  - else → draw

**Points:** Win = 3, Draw = 1, Loss = 0

Tiebreaker (when equal points): goal difference estimate from ranking gap, then head-to-head

### 4. Output format

First, show a match-by-match predictions table:

```
| Match | p_win (fav) | Result | Notes |
|-------|------------|--------|-------|
| Team A vs Team B | 0.67 | **A W** | reason |
| Team C vs Team D | 0.58 | **Draw** | reason |
...
```

Then the predicted standings:

```
## Group X — Predicted Standings

| # | Country | W | D | L | GD | Pts | Notes |
|---|---------|---|---|---|----|-----|-------|
| 1 | ...     | 2 | 1 | 0 | +3 |  7  | strong form |
| 2 | ...     | 1 | 2 | 0 | +1 |  5  |             |
| 3 | ...     | 1 | 0 | 2 | -2 |  3  | weak defense |
| 4 | ...     | 0 | 1 | 2 | -4 |  1  |             |

**Advances:** Team1, Team2

1–3 sentence reasoning paragraph covering key factors: form differentials,
tiebreaker logic, uncertainty flags.
```

### 5. Write back to groups.md

After presenting predictions in chat, update `groups.md` for that group:
- Replace the simple `| Country | FIFA Ranking |` table with the full standings table above
- Include `| # | Country | FIFA Ranking | W | D | L | GD | Pts |` columns
- Add the `**Advances:**` line and reasoning paragraph below the table

### 6. Summary
After all 12 groups, list the 24 teams predicted to advance.

## Notes
- Name mismatches between files: e.g. "USA" in rankings = "United States" in groups, "IR Iran" = "Iran", "Côte d'Ivoire" = "Ivory Coast", "Korea Republic" = "South Korea", "Cabo Verde" = "Cape Verde", "Congo DR" = "DR Congo"
- **Rank discrepancy**: ranking integers in `groups.md` may not match `fifa_rankings.csv` — always use `points` from the CSV for Elo calculations, not the rank number
- If WebSearch yields no useful form data, rely on rankings only and note it
- Be explicit about uncertainty — these are probabilistic predictions
