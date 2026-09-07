# SPX Butterfly — 14 DTE, 50 Delta Center, ±40 Wings

Long call butterfly, defined-risk, net debit. Two saved variants differ only
in exit rules — same structure, same entry, same dates (May 16, 2022 – Sep 6,
2026).

## Structure

- **Body (short):** 2x short call at the 50-delta strike, 14 DTE
- **Wings (long):** 1x long call at center − 40 points, 1x long call at
  center + 40 points, both 14 DTE
- Entered daily (Mon–Fri) at 10:41 AM, exact DTE and exact strike offsets,
  1% of portfolio per trade, VIX filter: min 15 (no effective max)
- All calls — this is a call butterfly, not an iron butterfly (no puts
  involved)

This is a long-vega-near-center / short-gamma-at-the-wings structure typical
of a butterfly: max profit if SPX pins near the 50-delta strike at
expiration, defined max loss (the net debit paid) if it runs hard through
either wing.

## Two variants — same structure, different exit

| | v2 | v2.2 |
|---|---|---|
| Exit rule | Profit Target 35% only | Profit Target 35% **+** exit when position delta < −7 or > 8 |
| Author's note | "Replicates a trade with a resting GTC closing order... manual delta exit since the broker won't allow a delta exit condition with the resting closing order" | "PT and added delta exits which would be fully executed by the OO bot" |

**This distinction matters and isn't cosmetic.** v2 models what a *resting
GTC limit order* can mechanically do at the broker (profit target only — a
GTC order can't also watch delta). v2.2 models what the OO automation bot
*can* actually execute live (both rules, continuously monitored). Ryan's own
note flags this as an open question worth testing empirically — which one
here does, since both are saved side by side.

## Headline outcomes (May 2022 – Sep 2026, ~4.3 yr)

| Metric | v2 (PT only) | v2.2 (PT + delta exit) |
|---|---|---|
| P/L | $455,240 | $508,260 |
| CAGR | 48.8% | 51.9% |
| Max Drawdown | -6.8% | -6.9% |
| MAR | 7.2 | 7.5 |
| Sharpe | 4.74 | 4.61 |
| Sortino | 9.32 | 11.02 |
| Win % | 93.3% | 91.6% |
| Capture Rate (of total premium collected) | 28.2% | 31.2% |
| Avg / trade | $92/lot | $98/lot |
| Avg winner | $134/lot | $135/lot |
| Avg loser | -$490/lot | -$297/lot |
| Max winner | $840/lot | $2,790/lot |
| Max loser | -$775/lot | -$775/lot |
| Avg days in trade | 4.1 | 3.8 |
| Closed trades | 760 | 759 |

**Read:** v2.2's delta exit clearly does its job on the loss side — avg
loser shrinks from -$490 to -$297/lot (39% smaller) — at the cost of a
slightly lower win rate (93.3% → 91.6%, i.e. more trades get cut before
reaching a full loss AND before recovering to a win). Despite the lower win
rate, v2.2 wins on every risk-adjusted and absolute metric except Sharpe
(4.74 vs 4.61) and max loser (identical tail — the delta exit doesn't touch
the true worst case, which is presumably a fast overnight/gap move past the
delta trigger before it can fire intraday). Sortino tells the more relevant
story for an asymmetric strategy like this (9.32 vs 11.02, favoring v2.2) —
Sharpe penalizes upside deviation as much as downside, which understates how
much better v2.2's downside control actually is.

**Caveat before treating v2.2 as strictly better:** this is a backtest
comparison of two rule sets, not a comparison of what's achievable live. v2
exists specifically because a resting GTC order is what's *actually
executable* without the OO bot running continuously; v2.2 assumes the bot
fires exactly at the delta thresholds with no slippage beyond what's modeled
(0.25 exit slippage, same for both). If Ryan isn't running the OO automation
live 24/7 against this position, v2's numbers are the honest baseline and
v2.2 is the ceiling if automation is fully reliable.

## What hasn't been done yet

- No Greeks-over-time / regime analysis (VIX buckets, gap sensitivity) —
  this writeup covers structure and headline performance only, matching the
  depth of a first-pass review. Full second-order Greeks work (the depth
  given to the RIC) not yet done here.
- No correlation check against the RIC or the DC 1/2 and 5/7 strategies
  (portfolio/correlation-notes.md doesn't include this strategy).
- No significance testing performed (nothing here currently rests on a
  subgroup claim that would need it, per reference/significance_testing.py's
  usage criteria).
