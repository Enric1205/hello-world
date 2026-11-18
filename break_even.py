#!/usr/bin/env python3
"""Break-Even-Rechner für Produktentwicklungen (CLI).

Beispiel:
    python3 break_even.py --dev 450000 --unit-cost 67 --fixed 400000 \
        --price 149 --volume 6000 --years 5 --growth 15 --cost-inflation 2
"""
from __future__ import annotations

import argparse
import sys

EUR = "\u20ac"


def fmt(value: float, decimals: int = 0) -> str:
    s = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} {EUR}"


def compute(args: argparse.Namespace) -> dict:
    db_unit = args.price - args.unit_cost
    fixed_cash = args.fixed - args.depreciation
    bep_units = args.fixed / db_unit if db_unit > 0 else float("inf")
    bep_revenue = bep_units * args.price if db_unit > 0 else float("inf")
    bep_cash = fixed_cash / db_unit if db_unit > 0 else float("inf")
    db_margin = db_unit / args.price if args.price > 0 else 0.0

    rows = []
    cumulative = -args.dev
    payback = None
    for year in range(1, args.years + 1):
        volume = args.volume * (1 + args.growth / 100) ** (year - 1)
        price = args.price * (1 + args.price_drift / 100) ** (year - 1)
        var_y = args.unit_cost * (1 + args.cost_inflation / 100) ** (year - 1)
        revenue = volume * price
        variable = volume * var_y
        db = revenue - variable
        ebit = db - args.fixed
        cash = ebit + args.depreciation
        start = cumulative
        cumulative += cash
        if payback is None and cumulative >= 0:
            payback = (year - 1) + (min(1.0, -start / cash) if cash > 0 else 0.0)
        bep_year = args.fixed / (price - var_y) if price > var_y else float("inf")
        rows.append(dict(year=year, volume=volume, price=price, revenue=revenue,
                         variable=variable, db=db, ebit=ebit, cash=cash,
                         cumulative=cumulative, bep=bep_year))
    return dict(db_unit=db_unit, db_margin=db_margin, bep_units=bep_units,
                bep_revenue=bep_revenue, bep_cash=bep_cash, payback=payback, rows=rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Break-Even-Rechner für Produktentwicklungen")
    p.add_argument("--dev", type=float, required=True, help="einmalige Entwicklungskosten (EUR)")
    p.add_argument("--unit-cost", type=float, required=True, help="variable Stückkosten (EUR)")
    p.add_argument("--fixed", type=float, required=True, help="fixe Kosten pro Jahr (EUR)")
    p.add_argument("--price", type=float, required=True, help="Verkaufspreis netto pro Stück (EUR)")
    p.add_argument("--volume", type=float, required=True, help="Absatzmenge Jahr 1 (Stück)")
    p.add_argument("--years", type=int, default=5, help="Planungshorizont (Jahre, Standard 5)")
    p.add_argument("--growth", type=float, default=0.0, help="Absatzwachstum %% p. a.")
    p.add_argument("--price-drift", type=float, default=0.0, help="Preisänderung %% p. a.")
    p.add_argument("--cost-inflation", type=float, default=0.0, help="Inflation variable Kosten %% p. a.")
    p.add_argument("--depreciation", type=float, default=0.0, help="Abschreibungen in Fixkosten (EUR/Jahr)")
    args = p.parse_args()

    if args.price <= 0 or args.unit_cost < 0:
        sys.exit("Fehler: Preis muss positiv sein.")
    r = compute(args)

    print("=" * 74)
    print("BREAK-EVEN-RECHNER \u00b7 PRODUKTENTWICKLUNG")
    print("=" * 74)
    print(f"Deckungsbeitrag / Stück        : {fmt(r['db_unit'], 2)}  (Marge {r['db_margin']*100:.1f} %)")
    if r["db_unit"] <= 0:
        sys.exit("Fehler: Preis deckt variable Stückkosten nicht ab – kein Break-Even möglich.")
    print(f"Break-Even-Menge               : {r['bep_units']:,.0f} Stück/Jahr".replace(",", "."))
    print(f"Break-Even-Umsatz              : {fmt(r['bep_revenue'])}/Jahr")
    print(f"Cash-Break-Even (o. Abschr.)   : {r['bep_cash']:,.0f} Stück/Jahr".replace(",", "."))
    print(f"Amortisation Entwicklung       : "
          + (f"{r['payback']:.1f} Jahre" if r["payback"] is not None else "nicht im Horizont"))
    print()
    header = (f"{'Jahr':>4} {'Absatz':>9} {'Umsatz':>14} {'Var.Kosten':>13} "
              f"{'DB':>13} {'EBIT':>13} {'Kumuliert':>14} {'BEP Stk.':>9}")
    print(header)
    print("-" * len(header))
    for row in r["rows"]:
        print(f"{row['year']:>4} {row['volume']:>9,.0f} {fmt(row['revenue']):>14} "
              f"{fmt(row['variable']):>13} {fmt(row['db']):>13} {fmt(row['ebit']):>13} "
              f"{fmt(row['cumulative']):>14} {row['bep']:>9,.0f}".replace(",", "."))
    print("=" * 74)


if __name__ == "__main__":
    main()
