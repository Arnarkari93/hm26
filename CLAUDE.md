# HM26 — World Cup 2026 Predictions

## Goal
Predict group stage, knockout results, and exchange rates for 48 World Cup teams (June-July 2026).

## Scope
- 48 qualifying nations + host countries (USA, Mexico, Canada)
- Group stage & knockout bracket predictions
- Currency volatility & exchange rate predictions during tournament

## Key Files
- `countries.csv` - 48 WC teams with confederation & FIFA ranking
- `fifa_rankings.csv` - Full FIFA rankings with points
- `team-rates.csv` - per-team attack (gf/match) & defense (ga/match); Poisson model input. Regen: `scripts/build_team_rates.py`
- `scripts/predict.py` - Poisson scoreline engine (used by predict-score skill)
- `groups.md` - Group stage predictions & standings
- `knockout.md` - Knockout bracket predictions (Round of 32 onward)
- `third-place.md` - Best 8 of 12 third-place teams advancing to R32

## Notes
- Concise comms, sacrifice grammar
- Use `rg`, `fd`
- Focus on currencies of participating nations
