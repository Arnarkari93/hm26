# Structured Confidence

**Files:** `groups.md`, `knockout.md`, `predicted-scores/*.md`

**Problem:** Confidence expressed three ways — "High", "~83%", "coin flip". No consistent metric, so you can't aggregate ("which picks am I least confident in?") or filter ("which R32 matches are coin flips?").

**Solution:** Standardize to a 5-point scale (or percentage) with a single definition. One schema applied in every prediction file and table.

**Benefits:** Leverage — any summary view of picks becomes trivial. Locality — the definition of "High confidence" lives in one place.
