# SPX PCS — 0 DTE, Daily

Put credit spread, defined-risk, net credit. Standalone OO test reviewed
Sep 8, 2026, plus its correlation against the other four strategies in the
"Claude portfolio test" OO portfolio.

## Structure

- **Short leg:** 1x short put at 45 delta, 0 DTE
- **Long leg:** 1x long put 5 points below the short strike, 0 DTE
- Entered daily (Mon–Fri) at 1:15 PM, exact DTE, exact strike offset, 1% of
  portfolio per trade
- Entry filter: underlying above its 5-day SMA, with a minimum 0.3% up-move
  required — a bullish-continuation filter, not a volatility or delta
  condition. Worth flagging: this is a fairly specific technical filter: it
  wasn't tested for how it generalizes out-of-sample, and a filter this
  narrow is exactly the kind of thing that can look better in a backtest
  than it will live.

## Standalone outcomes (May 2022 – Sep 2026, $100K start)

| Metric | Value |
|---|---|
| P/L | $45,108 |
| CAGR | 9% |
| Max Drawdown | -3.3% |
| MAR Ratio | 2.7 |
| Sharpe | 1.34 |
| Sortino | 1.84 |
| Win % | 76.4% |
| Total Premium | $146,390 |
| Capture Rate | 30.8% |
| Avg / trade | $54/lot |
| Avg winner | $159/lot (raw trade avg: $534) |
| Avg loser | -$288/lot (raw trade avg: -$995) |
| Max winner | $213/lot |
| Max loser | -$382/lot |
| Trades | 259 (198 winners) |
| Longest losing streak | 2 trades |

**Read:** this is meaningfully weaker than the other four strategies on
every risk-adjusted metric — Sharpe 1.34 vs. the butterfly's 4.74, MAR 2.7
vs. everything else in the 7-28 range. The 76.4% win rate looks good in
isolation, but avg loser (-$995/trade) is nearly double avg winner
($534/trade) — a classic short-premium asymmetry, not a red flag by itself,
but it means the strategy needs that high win rate just to be
breakeven-plus, leaving little margin if the win rate drifts.

**Year-by-year P/L is declining**, not flat: $9,554 (2022) → $16,444 (2023)
→ $7,962 (2024) → $8,357 (2025) → $2,791 (2026 YTD, 42 trades). Sample size
per year (42-64 trades) is too small to call this a confirmed decay in
edge with confidence, but it's a "watch" item, not nothing — worth
re-checking after this year closes out.

## Correlation with the other four (portfolio diversification check)

Full pairwise correlation, all five strategies, 0-filled daily P/L over the
complete history:

| | Butterfly | DC 1/2 | DC 5/7 | RIC | PCS |
|---|---|---|---|---|---|
| Butterfly | 1.00 | 0.035 | 0.027 | 0.009 | -0.004 |
| DC 1/2 | 0.035 | 1.00 | -0.031 | 0.027 | 0.005 |
| DC 5/7 | 0.027 | -0.031 | 1.00 | -0.004 | -0.017 |
| RIC | 0.009 | 0.027 | -0.004 | 1.00 | **0.161** |
| PCS | -0.004 | 0.005 | -0.017 | 0.161 | 1.00 |

Restricted to days both strategies actually had a position closing (thinner
samples, but this is where a real relationship shows up):

| Pair | Overlap days | Correlation |
|---|---|---|
| PCS vs RIC | 101 | **+0.355** |
| PCS vs DC 1/2 | 41 | -0.096 |
| PCS vs Butterfly | 121 | -0.083 |
| PCS vs DC 5/7 | 40 | -0.019 |

**This is the key finding.** PCS and RIC are positively correlated — the
strongest pairwise relationship (magnitude) of any pair across all five
strategies, in the wrong direction for diversification. On PCS's 10 worst
single days, RIC was also negative on 4 of them, including two of RIC's own
larger losses (-$4,665 on 2025-10-24, -$2,292 on 2025-11-26) landing the
same day as a PCS loss. This makes sense structurally — both are 0DTE SPX
premium-selling strategies exposed to the same large-intraday-move risk —
but it means PCS doesn't diversify the portfolio's strongest independent
performer, it adds correlated risk to it.

## Recommendation

**Leave it out of the live portfolio for now.** This isn't "needs more
data" — the standalone risk-adjusted metrics are the weakest of the five by
a wide margin, and the one strategy it's actually correlated with (RIC) is
the wrong one to be correlated with. If P/L keeps declining through the
rest of 2026 that's a second, independent reason to deprioritize it rather
than revisit.
