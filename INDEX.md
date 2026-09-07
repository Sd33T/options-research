# Options Research — Index

Read this first. One paragraph per strategy, pointing into its own folder for
detail. The point of this repo: never re-derive a finding Claude (or you)
already checked — look here first, then extend it.

Reference: `reference/oo-export-schema.md` — OptionOmega CSV export column
definitions and unit conventions. Read before writing any analysis script
against an OO export; a units mistake here already cost a wasted round-trip
once (Sep 7, 2026).

## Strategies

- **[SPX RIC 0DTE](strategies/spx-ric-0dte/README.md)** — reverse iron condor,
  0DTE, long-gamma/long-vol debit structure. Most fully analyzed strategy in
  this repo so far: full Greeks writeup, VIX-regime breakdown, three active-exit
  variants tested (all worse than doing nothing), portfolio correlation check
  against the double calendars. See its findings.yaml for the closed/open
  question list.
- **[SPX DC 1/2](strategies/spx-dc-1-2/README.md)**, **[SPX DC 11/23](strategies/spx-dc-11-23/README.md)**,
  **[SPX DC 14/28](strategies/spx-dc-14-28/README.md)**, **[SPX DC 5/7](strategies/spx-dc-5-7/README.md)**
  — double calendar variants. Only pulled so far for the RIC correlation check
  (see portfolio/correlation-notes.md) — no dedicated Greeks/regime analysis
  done yet on any of these individually.

## Portfolio-level

- **[portfolio/correlation-notes.md](portfolio/correlation-notes.md)** — RIC
  vs. double-calendar daily P/L correlation, and a specific look at whether the
  calendar book cushions the RIC's Jul-Aug 2026 drawdown (short answer: not
  really — correlation is ~0, and 2 of 4 calendars had zero trades open during
  that window).

## Known gaps (not yet done, flagged so nobody assumes they're done)

- QQQ 14/28 DTE calendar — referenced in an old saved OO Portfolio name but
  never located as a standalone saved test; not pulled or analyzed.
- Four Butterfly variants and a "SPX--PCS--0DTE--Daily" test exist in the OO
  account but aren't accounted for anywhere in this repo — unclear if they're
  live/considered live.
- No dedicated strategy README/findings yet for any of the four DC variants —
  only the RIC has full writeups so far.
