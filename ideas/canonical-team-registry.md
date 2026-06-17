# Canonical Team Registry

**Files:** `countries.csv`, `fifa_rankings.csv`, skill SKILL.md files, `groups.md`, `knockout.md`

**Problem:** "South Korea" vs "Korea Republic", "Ivory Coast" vs "Côte d'Ivoire" — name translations documented only in `predict-groups/SKILL.md`. Every file crossing the two CSVs carries the mapping implicitly or re-derives it.

**Solution:** Single canonical team list merging `countries.csv` + `fifa_rankings.csv` + all alias variants. One place to look up any team's rank, Elo points, and all known names.

**Benefits:** Locality — name-mapping bugs appear in one file, not scattered. Leverage — skills stop carrying mapping logic; they just reference the registry.
