# RIC vs. Double-Calendar Correlation

Pulled Sep 7, 2026. Full trade logs for four starred SPX double-calendar
backtests vs. the RIC (see ../strategies/*/backtests/ for raw CSVs).

## Full-history daily P/L correlation (May 2022 - Sep 2026)

| Pair | Correlation (days RIC traded) |
|---|---|
| RIC vs DC 1/2 | 0.057 |
| RIC vs DC 11/23 | 0.018 |
| RIC vs DC 14/28 | 0.096 |
| RIC vs DC 5/7 | -0.027 |

Close to zero across the board, not negative. This is genuine independence,
not a designed hedge -- a true offsetting relationship would show up as
consistently negative correlation.

## Jul-Aug 2026 drawdown window (RIC's 2nd-worst drawdown, -$10,423, not yet
recovered as of the data pull)

- DC 11/23 and DC 14/28: **zero trades open in this entire window.** Last
  entries were May 11 and Apr 30, 2026 respectively -- well before the RIC
  drawdown started. Not broken, just infrequent (~10-12 trades/year each).
- DC 1/2 and DC 5/7 did overlap, and the offset worked as intended when it
  happened:
  - 2026-07-30: RIC +$2,079, same day DC 1/2 -$2,070 (near-perfect offset).
  - 2026-07-15: RIC hit a full pin loss (-$5,380), DC 5/7 +$1,820 the same
    day (cushioned about a third of it).
- But the RIC's four worst days in the window (Jul 14 -$4,695, Aug 12 -$4,500,
  Aug 21 -$5,300, Sep 3 -$4,185) had **no calendar strategy open at all.**

## Read
The long-gamma/short-gamma pairing is closer to "two uncorrelated return
streams that occasionally offset by coincidence of timing" than "a hedge that
reliably cushions RIC drawdowns." Still a legitimate diversification benefit
at the portfolio level (uncorrelated P&L reduces aggregate variance even
without negative correlation), but a weaker and different claim than "the
calendars absorb the RIC's drawdowns." Making that latter claim true would
require either trading the calendars more frequently or explicitly triggering
an additional calendar entry when the RIC is in an open drawdown -- neither
is configured today.

## Known gap
QQQ 14/28 DTE not included -- referenced in an OO Portfolio name but not
located as a standalone saved test. Four Butterfly variants and a
"SPX--PCS--0DTE--Daily" test also exist in the OO account and are not
accounted for here.
