# Break-Even-Rechner · Produktentwicklung

Interaktiver Rechner zur wirtschaftlichen Bewertung einer Produktentwicklung:
Amortisation der Entwicklungskosten, Break-Even-Menge und -Umsatz, Deckungsbeiträge
und Mehrjahresplanung.

## Nutzung

**Web-App:** `index.html` im Browser öffnen – keine Installation, keine Abhängigkeiten,
läuft komplett lokal. Alle Eingaben werden live berechnet.

**CLI:**

```bash
python3 break_even.py --dev 450000 --unit-cost 67 --fixed 400000 \
    --price 149 --volume 6000 --years 5 --growth 15 --cost-inflation 2
```

| Parameter | Bedeutung |
|---|---|
| `--dev` | Einmalige Entwicklungskosten (EUR) |
| `--unit-cost` | Variable Stückkosten (EUR) |
| `--fixed` | Fixe Kosten pro Jahr (EUR) |
| `--depreciation` | Anteil Abschreibungen in den Fixkosten (für Cash-Break-Even) |
| `--price` | Verkaufspreis netto pro Stück (EUR) |
| `--volume` | Absatzmenge Jahr 1 (Stück/Jahr) |
| `--growth` | Absatzwachstum % p. a. |
| `--price-drift` | Preisänderung % p. a. |
| `--cost-inflation` | Inflation der variablen Kosten % p. a. |
| `--years` | Planungshorizont in Jahren (Standard 5) |

## Funktionsumfang

- **Einmalige Entwicklungskosten**: Entwicklung & Konstruktion, Prototypen, Testing &
  Zertifizierung, Werkzeuge/Tooling, Launch-Marketing.
- **Variable Stückkosten**: Material, Fertigung/Lohn, Montage, Verpackung, Versand &
  Logistik, Qualität/Sonstiges.
- **Fixe Kosten pro Jahr**: Personal, Miete & Infrastruktur, Maschinen & Abschreibungen,
  Verwaltung, laufendes Marketing, Sonstiges.
- **Preis & Absatz**: Netto-Verkaufspreis, Absatz Jahr 1, Absatzwachstum, Preisdrift,
  Kosteninflation, Planungshorizont (1–15 Jahre).
- **Kennzahlen**: Deckungsbeitrag/Stück und DB-Marge, Break-Even-Menge und -Umsatz,
  Cash-Break-Even (ohne Abschreibungen), Amortisationsdauer der Entwicklung,
  kumulierte Stückzahl bis Amortisation, EBIT Jahr 1, kumulierter Cashflow.
- **Diagramme**: klassische Break-Even-Analyse (Erlös- vs. Kostenlinien mit
  Break-Even-Punkt) und kumulierter Cashflow über die Planungsjahre.
- **Mehrjahrestabelle** mit Umsatz, variablen Kosten, Deckungsbeitrag, Fixkosten, EBIT,
  Cashflow und jeweils gültiger Break-Even-Menge.
- **Sensitivitätsmatrix**: Break-Even-Menge bei Preis ±10 % × variablen Kosten ±10 %.
- **Export**: CSV (Semikolon, Excel-kompatibel) und Druck/PDF-Ansicht.

## Formeln

| Kennzahl | Formel |
|---|---|
| Deckungsbeitrag/Stück | `Preis − variable Stückkosten` |
| DB-Marge | `DB/Stück ÷ Preis` |
| Break-Even-Menge | `Fixkosten/Jahr ÷ DB/Stück` |
| Break-Even-Umsatz | `Break-Even-Menge × Preis` |
| Cash-Break-Even | `(Fixkosten − Abschreibungen) ÷ DB/Stück` |
| EBIT/Jahr | `Absatz × DB/Stück − Fixkosten` |
| Kumulierter Cashflow | `−Entwicklungskosten + Σ (EBIT + Abschreibungen)` |
| Amortisationsdauer | erstes Jahr mit kumuliertem Cashflow ≥ 0, linear interpoliert |

Alle Beträge netto (ohne Umsatzsteuer). Die Rechnung ist eine Planungsheuristik und
ersetzt keine Investitionsrechnung nach handels- oder steuerrechtlichen Grundsätzen
(z. B. Kapitalwertmethode, Zinsen, Steuern, Working Capital).
