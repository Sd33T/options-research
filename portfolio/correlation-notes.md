# RIC vs. Double-Calendar Correlation

Pulled Sep 7, 2026. Full trade logs for four starred SPX double-calendar
backtests vs. the RIC (see ../strategies/*/backtests/ for raw CSVs).

**Note (Sep 7, 2026):** the DC "9/23"/"11/23" test's raw data was removed
from `strategies/` after this analysis was written (naming discrepancy
never resolved, deprioritized alongside QQQ 14/28 — see INDEX.md). Its
numbers below are kept as a historical record of what the correlation
looked like at the time, but the source CSV no longer exists in this repo
if you want to re-derive it — re-pull from OO first.

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

## Update, Sep 8 2026: full five-strategy matrix (Butterfly, DC 1/2, DC 5/7, RIC, PCS)

Re-ran this properly with actual trade-log data (not just RIC-vs-DC pairs)
once the butterfly and PCS backtests were pulled. Methodology: daily P/L per
strategy, non-trading days zero-filled, full history May 2022-Sep 2026.

**Full pairwise correlation (0-filled, full history):**

| | Butterfly | DC 1/2 | DC 5/7 | RIC | PCS |
|---|---|---|---|---|---|
| Butterfly | 1.00 | 0.035 | 0.027 | 0.009 | -0.004 |
| DC 1/2 | 0.035 | 1.00 | -0.031 | 0.027 | 0.005 |
| DC 5/7 | 0.027 | -0.031 | 1.00 | -0.004 | -0.017 |
| RIC | 0.009 | 0.027 | -0.004 | 1.00 | 0.161 |
| PCS | -0.004 | 0.005 | -0.017 | 0.161 | 1.00 |

**Restricted to days both strategies actually had a position closing**
(thinner samples, but this is where a real complementary relationship shows
up):

| Pair | Overlap days | Correlation |
|---|---|---|
| Butterfly vs DC 5/7 | 84 | -0.193 |
| PCS vs RIC | 101 | **+0.355** |
| DC 5/7 vs RIC | 33 | -0.125 |
| PCS vs DC 1/2 | 41 | -0.096 |
| PCS vs Butterfly | 121 | -0.083 |
| Butterfly vs RIC | 105 | -0.069 |
| PCS vs DC 5/7 | 40 | -0.019 |
| Butterfly vs DC 1/2 | 78 | -0.003 |
| DC 1/2 vs RIC | 35 | +0.139 |
| DC 1/2 vs DC 5/7 | 6 | -0.252 (n=6 -- too thin to trust, not a real finding) |

**Two things worth acting on:**

1. **DC 5/7 is the closest thing to a real complement to the butterfly.**
   -0.193 over 84 overlap days, and directly visible in the data: on three
   of the butterfly's 10 worst single days, DC 5/7 posted +$9,010, +$3,615,
   and +$2,250 the same day. Modest, but genuine.
2. **PCS and RIC are positively correlated (+0.355 on overlap days), the
   strongest relationship in the whole matrix and in the wrong direction.**
   Both are 0DTE SPX premium-selling strategies exposed to the same
   large-intraday-move risk. See spx-pcs-0dte/findings.yaml for the full
   writeup and recommendation (leave PCS out of the live portfolio).

No pair anywhere in the matrix shows two strategies both taking a >$3,000
single-day loss on the same day, across the whole 4.3-year history. Good
sign for diversification as tested, but every caveat from the original
analysis below still applies: this window hasn't seen a real tail event,
and near-zero correlations in calm markets are exactly the numbers that can
break down toward 1 in a genuine stress event.

## Known gap (updated)
QQQ 14/28 DTE still not included -- deprioritized per INDEX.md. Two more
Butterfly variants (v1, v1.1 or similar) still exist in the OO account and
haven't been reviewed. PCS 0DTE is no longer a gap -- reviewed Sep 8, 2026,
see spx-pcs-0dte/.
