# Bracket Derivation

**Files:** `third-place.md`, `knockout.md`, `groups.md`

**Problem:** `knockout.md` was copied from gisko.is/knockout. `third-place.md` warns its table is probabilistic with swing scenarios. If a group result changes, three files need manual updates. The R32 bracket rules (1st/2nd from each group + best 8 third-placers) are deterministic given group results — yet re-derived by hand each time.

**Solution:** One derivation step: group results → third-place standings → R32 matchups. Third-place and bracket become outputs of group predictions, not independent documents.

**Benefits:** Leverage — correct group results automatically yield the correct bracket. Eliminates the silent mismatch where Panama is assumed to advance in `knockout.md` but the swing scenario in `third-place.md` says it might not.
