# Options Research

Durable record of options backtest analysis (OptionOmega) -- raw trade-log
exports, dated and versioned, plus confidence-tagged findings per strategy.
Built so future analysis sessions reference what's already known instead of
re-deriving it from scratch.

Start at [INDEX.md](INDEX.md).

## Conventions
- One folder per strategy under `strategies/`.
- Each strategy folder: `README.md` (current understanding), `findings.yaml`
  (dated, confidence-tagged claims -- see spx-ric-0dte/findings.yaml for the
  format, including how a retracted/corrected claim is recorded rather than
  silently deleted), `backtests/` (raw OO CSV exports, named
  `YYYY-MM-DD_<version-or-variant>.csv`).
- `reference/oo-export-schema.md` -- OptionOmega's CSV column definitions and
  unit conventions, confirmed firsthand. Read before writing analysis code
  against an OO export.
- `portfolio/` -- cross-strategy analysis (correlation, drawdown overlap).
