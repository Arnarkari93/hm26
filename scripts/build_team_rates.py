#!/usr/bin/env python3
"""Build team-rates.csv: per-team attack (gf_per_match) & defense (ga_per_match).

These feed the Poisson goal model in the predict-score skill.
Seeded from Elo as a transparent prior (source=elo-prior). Override rows with
real qualifying/recent goal data as it's gathered (set source=actual/blended).

Re-run: python3 scripts/build_team_rates.py
"""
import csv

# WC team name -> fifa_rankings.csv name (only where they differ)
ALIAS = {
    "United States": "USA",
    "Iran": "IR Iran",
    "South Korea": "Korea Republic",
    "Ivory Coast": "Côte d'Ivoire",
    "Türkiye": "Turkey",
    "DR Congo": "Congo DR",
    "Cape Verde": "Cabo Verde",
}

# League baseline: ~2.7 total goals/game => 1.35 per team
MU = 1.35
# Sensitivity of attack/defense to Elo strength (per 100 Elo pts above/below mean)
ATK_K = 0.17
DEF_K = 0.14
GF_FLOOR, GF_CEIL = 0.55, 3.20
GA_FLOOR, GA_CEIL = 0.55, 3.00


def load_elo():
    elo = {}
    with open("fifa_rankings.csv") as f:
        for r in csv.DictReader(f):
            elo[r["country"].strip()] = float(r["points"])
    return elo


def main():
    elo = load_elo()
    wc = list(csv.DictReader(open("countries.csv")))

    def team_elo(name):
        return elo[ALIAS.get(name, name)]

    elos = [team_elo(r["country"].strip()) for r in wc]
    mean_elo = sum(elos) / len(elos)

    rows = []
    for r in wc:
        c = r["country"].strip()
        s = (team_elo(c) - mean_elo) / 100.0          # Elo strength, ~[-2.7, +3.3]
        gf = min(GF_CEIL, max(GF_FLOOR, MU * (1 + ATK_K * s)))
        ga = min(GA_CEIL, max(GA_FLOOR, MU * (1 - DEF_K * s)))
        rows.append((c, round(gf, 2), round(ga, 2)))

    rows.sort(key=lambda x: -x[1])  # by attack, just for readability
    with open("team-rates.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["country", "gf_per_match", "ga_per_match", "sample_matches", "source"])
        for c, gf, ga in rows:
            w.writerow([c, gf, ga, 0, "elo-prior"])

    mgf = sum(x[1] for x in rows) / len(rows)
    print(f"Wrote team-rates.csv ({len(rows)} teams). mean gf={mgf:.3f} (= league mu used by skill)")


if __name__ == "__main__":
    main()
