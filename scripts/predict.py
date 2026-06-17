#!/usr/bin/env python3
"""Poisson scoreline predictor for WC 2026.

Uses per-team attack (gf_per_match) & defense (ga_per_match) from team-rates.csv.
Independent-Poisson model:
    mu      = league avg goals/team/match (= mean gf across teams)
    lam_A   = gf_A * ga_B / mu        (team A's expected goals)
    lam_B   = gf_B * ga_A / mu
Optional host/form multipliers nudge each lambda.

Outputs: expected goals, modal scoreline, top scorelines, and W/D/L probs.
Unlike Elo-diff rounding, this gives underdogs nonzero scoring chance and a
real high-scoring tail.

Usage:
  python3 scripts/predict.py "Team A" "Team B" [--hostA] [--hostB]
          [--formA 1.1] [--formB 0.9] [--knockout]
"""
import argparse
import csv
import math
import sys

MAXG = 9  # goals grid 0..8

# accept common alt spellings -> countries.csv canonical name
ALIAS = {
    "usa": "United States", "united states": "United States", "us": "United States",
    "turkey": "Türkiye", "turkiye": "Türkiye", "türkiye": "Türkiye",
    "cape verde": "Cape Verde", "cabo verde": "Cape Verde",
    "ivory coast": "Ivory Coast", "cote d'ivoire": "Ivory Coast",
    "côte d'ivoire": "Ivory Coast",
    "dr congo": "DR Congo", "congo dr": "DR Congo",
    "south korea": "South Korea", "korea republic": "South Korea",
    "iran": "Iran", "ir iran": "Iran",
    "bosnia": "Bosnia and Herzegovina",
    "bosnia & herzegovina": "Bosnia and Herzegovina",
}


def load_rates(path="team-rates.csv"):
    rates = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            rates[r["country"].strip()] = (
                float(r["gf_per_match"]), float(r["ga_per_match"]))
    mu = sum(gf for gf, _ in rates.values()) / len(rates)
    return rates, mu


def resolve(name, rates):
    if name in rates:
        return name
    key = name.strip().lower()
    if key in ALIAS and ALIAS[key] in rates:
        return ALIAS[key]
    # case-insensitive direct
    for c in rates:
        if c.lower() == key:
            return c
    sys.exit(f"Team not found in team-rates.csv: {name!r}. "
             f"Check spelling against countries.csv.")


def pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("team_a")
    ap.add_argument("team_b")
    ap.add_argument("--hostA", action="store_true", help="team A is a host (USA/MEX/CAN)")
    ap.add_argument("--hostB", action="store_true")
    ap.add_argument("--formA", type=float, default=1.0, help="form multiplier on A's lambda")
    ap.add_argument("--formB", type=float, default=1.0)
    ap.add_argument("--knockout", action="store_true")
    a = ap.parse_args()

    rates, mu = load_rates()
    A, B = resolve(a.team_a, rates), resolve(a.team_b, rates)
    gfA, gaA = rates[A]
    gfB, gaB = rates[B]

    lamA = gfA * gaB / mu
    lamB = gfB * gaA / mu
    # host: ~+15% attack edge, opponent slightly suppressed (matches old +0.2/-0.1 feel)
    if a.hostA:
        lamA *= 1.15; lamB *= 0.92
    if a.hostB:
        lamB *= 1.15; lamA *= 0.92
    lamA *= a.formA
    lamB *= a.formB
    # knockout: marginally tighter (cagier) games
    if a.knockout:
        lamA *= 0.93; lamB *= 0.93

    pa = [pois(k, lamA) for k in range(MAXG)]
    pb = [pois(k, lamB) for k in range(MAXG)]
    grid = [[pa[i] * pb[j] for j in range(MAXG)] for i in range(MAXG)]

    # modal scoreline + top 5
    cells = sorted(((grid[i][j], i, j) for i in range(MAXG) for j in range(MAXG)),
                   reverse=True)
    pwA = sum(grid[i][j] for i in range(MAXG) for j in range(MAXG) if i > j)
    pwB = sum(grid[i][j] for i in range(MAXG) for j in range(MAXG) if i < j)
    pdr = sum(grid[i][i] for i in range(MAXG))

    margin = abs(pwA - pwB)
    if margin >= 0.40:
        conf = "High"
    elif margin >= 0.20:
        conf = "Medium"
    else:
        conf = "Low"

    p_top = cells[0][0]
    print(f"=== {A} vs {B} ===")
    print(f"Expected goals: {A} {lamA:.2f} – {lamB:.2f} {B}")
    print(f"Modal scoreline: {A} {cells[0][1]} – {cells[0][2]} {B}  (P={p_top:.1%})")
    print(f"W/D/L: {A} {pwA:.0%} / draw {pdr:.0%} / {B} {pwB:.0%}")
    print(f"Confidence: {conf}  (win-prob margin {margin:.0%})")
    print("Top scorelines:")
    for p, i, j in cells[:5]:
        print(f"  {A} {i}–{j} {B}   {p:.1%}")
    over25 = sum(grid[i][j] for i in range(MAXG) for j in range(MAXG) if i + j > 2)
    print(f"P(over 2.5 goals): {over25:.0%}   P(BTTS): "
          f"{(1-pa[0])*(1-pb[0]):.0%}")
    if a.knockout and pdr >= max(pwA, pwB) * 0.8:
        print("Note: draw plausible at 90' — could go to extra time / penalties.")


if __name__ == "__main__":
    main()
