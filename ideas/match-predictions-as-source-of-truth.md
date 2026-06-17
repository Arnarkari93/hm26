# Match Predictions as Source of Truth

**Files:** `groups.md`, `predicted-scores/groupstage/*.md`

**Problem:** `groups.md` embeds final standings tables — the table is derived from match results but authored directly. Only 4 of ~48 group fixtures have dedicated prediction files. Group tables are the *output*, but they're written by hand, not computed.

**Solution:** Treat individual match predictions (score + reasoning) as the source. Group standings tables become a computed summary derived from those predictions. When one match changes, the table updates automatically.

**Benefits:** Locality — changing a match result means editing one file, not hunting for its echo in the standings table. Leverage — the standings interface hides all the arithmetic.
