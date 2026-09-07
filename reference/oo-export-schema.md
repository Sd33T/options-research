# OptionOmega Trade-Log CSV Export — Column Reference

Confirmed firsthand (Sep 7, 2026) by exporting a real backtest and cross-checking
against the individual leg premiums shown in the OO UI. Written because a units
mistake here (dividing an already-per-contract field by contract count again)
produced a materially wrong finding earlier this session — don't repeat it.

## Units convention
OO quotes option premiums the standard way: **points per share**. A contract is
100 shares, so a quoted premium of `13.90` costs **$1,390 per contract**. The
`Max Premium` entry-condition field in the UI is in these same points, despite
showing a "$" sign next to it — `Max Premium: 16` means a $16.00/share quote,
i.e. a $1,600/contract cap, not a literal $16 cap.

## Key columns (`*SPX RIC--0-DTE` export, applies generally)
- `Premium` — net premium at open, **already per single contract**, in dollars
  (i.e. already ×100 vs. the points quote). NOT a total across `No. of Contracts`.
  To get total position-level debit/credit: `Premium * No. of Contracts`.
  To get the points-quote equivalent (matches the UI's leg display and the
  Max Premium field): `Premium / 100`.
- `No. of Contracts` — position size for that trade (grows over time as the
  account compounds, since allocation is a % of portfolio).
- `P/L` — realized dollar P/L for the **whole position** (already multiplied by
  contracts), not per-contract.
- `P/L %` — P/L as a % of the initial premium. For debit trades, -100% = full
  loss of the debit paid.
- `Opening VIX` / `Closing VIX` — VIX level at trade open/close (only present
  if VIX is used as an entry/exit condition).
- `Gap` — overnight move, prior day's close to current day's open (points).
- `Movement` — underlying's move from the day's open to the moment the trade
  was actually opened (points) — NOT intraday range. (Earlier working notes
  from a prior analysis session called this "intraday range" — that was wrong,
  or referred to a different metric; trust this definition, confirmed against
  the current OO docs as of Sep 2026.)
- `Max Loss` / `Max Profit` — largest adverse/favorable unrealized excursion
  during the trade's life, as a %. This is MAE/MFE, not the realized outcome.
- `Reason For Close` — e.g. "Expired", "Above Delta", "Exited at Specified
  Time". If every row says "Expired," there's no active exit management
  configured (pure defined-risk hold-to-expiration).
- `Legs` — pipe-or-line-separated per-leg detail: date, strike, right (P/C),
  action (BTO/STO/BTC/STC), fill price (points, "db"=debit "cr"=credit).

## Backtest summary page (not the CSV, but the same units issue applies)
- "Avg Per Trade", "Avg Winner", "Avg Loser", "Max Winner", "Max Loser" are
  all labeled "/lot" and are already correctly per-contract — no further
  division needed.
- "Total Premium" and "P/L" on the summary page are portfolio-level totals
  across all trades and all contract sizes — don't compare these directly to
  a single trade's per-lot numbers without accounting for `No. of Contracts`.

## Backtest config unit gotchas
- `Max Premium` in Entry Conditions ("Use Min/Max Entry Premium"): points
  per share (see above), not a literal dollar amount.
- `Profit Target` / `Stop Loss` in the Profit & Loss section: percentage of
  the initial premium (confirmed via a live 50%/-50% test — see
  spx-ric-0dte/findings.yaml).
