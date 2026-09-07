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

## Live-execution question: v2 (resting PT + manual delta watch) vs. v2.2 (full bot automation)

Ryan currently runs **zero OO automation** — this strategy would be entered,
have its PT order placed, and be delta-monitored 100% manually. His proposed
plan: place the resting GTC PT order (v2's execution model — better fills
than a bot-driven market/limit close), watch position delta live via OO's
"Model" tool, and manually close if delta breaches the v2.2 thresholds
(< −7 or > 8).

**Exit-slippage sensitivity test (isolates fill quality from the delta-exit
rule):**

| Exit Slippage | P/L | CAGR | MDD | Sharpe | Sortino | Win % | Avg Loser/lot | Max Winner/lot |
|---|---|---|---|---|---|---|---|---|
| 0.25 (v2 baseline) | $455,240 | 48.8% | -6.8% | 4.74 | 9.32 | 93.3% | -$490 | $840 |
| 0.05 | $484,300 | 50.5% | -5.7% | 5.22 | 10.77 | 94.3% | -$503 | $325 |
| 0.00 (theoretical perfect fill) | $491,215 | 50.9% | -5.7% | 5.26 | 10.91 | 94.5% | -$503 | $330 |
| *(reference) v2.2, PT + delta exit* | *$508,260* | *51.9%* | *-6.9%* | *4.61* | *11.02* | *91.6%* | *-$297* | *$2,790* |

**Read:** Even a literally perfect fill only closes 68% of the P/L gap to
v2.2 ($35,975 of $53,020). The remaining ~$17K, and the persistent gap in
avg loser size (-$503 vs -$297/lot even at 0 slippage), isn't a fill-quality
artifact — it's the delta exit doing something a resting PT order
structurally cannot do: cut a losing trade before expiration. Fill quality
and loss-cutting are two separate, additive sources of the v2-to-v2.2 gap,
not one explaining the other.

It's not a clean win for v2.2, though. On Sharpe, every tightened-slippage
v2 variant (5.22-5.26) beats v2.2 (4.61) — same pattern as the RIC's active-
exit tests, where early cuts reduce return more than they reduce volatility
on a Sharpe basis. Sortino (which only penalizes downside) is close to a
wash: 10.77-10.91 vs 11.02.

**Second-order-automation question, resolved:** checked whether OO's bot
(Schwab, or any of its 4 supported brokers — Tradier, Schwab/ToS,
tastytrade, TradeStation) could run the resting PT and an automated delta
exit at the same time, which would remove the manual-monitoring dependency
entirely. No — per OO's own docs: *"If a user chooses a resting PT, they
cannot also have a resting SL. This is a broker limitation."* This is
general across brokers, not Schwab-specific, and a delta exit is
functionally another closing order competing with the resting one, so it
hits the same wall. The only unverified alternative is entirely outside OO:
let the bot rest the PT, and separately place a native ThinkorSwim
conditional/OCO order on underlying price as an imperfect delta proxy. Two
real problems with that, neither checked yet: (1) unclear whether an order
OO's bot places via the Schwab API is even visible or linkable into a
manually-built ToS OCO — worth asking Schwab support directly before
relying on it; (2) a fixed price trigger isn't a stable stand-in for a delta
threshold, since delta also moves with time decay and IV, so the "right"
trigger price would need recalculating per trade rather than being set once
— itself manual work, not a free automation win.

**Net: given zero automation running today, Ryan's plan isn't one option
among several — it's the only way to get both the fill-quality benefit of a
resting order and delta-based loss protection right now.**

**The real operative risk is monitoring cadence, not the exit rule.**
Verified OO's "Model" tool directly against Ryan's actual open 9/3/2026
butterfly position: it does show a resting closing order on the books and a
live Delta (and full Greeks) curve exactly as described. But a full scan of
that page found no alert or notification tied to Greek thresholds — it's a
manual pull/check tool only. A backtested delta exit fires the instant the
threshold is crossed; a manual check only catches a breach as fast as Ryan
happens to look. Since this is a fully manual pipeline end-to-end (entry,
PT placement, AND delta monitoring — not partially bot-assisted), the
realistic risk isn't "will the exit rule work," it's "will the breach be
seen promptly." A loose checking cadence could give back more than the ~$17K/
avg-loser gap quantified above, especially since attention tends to lapse
exactly when markets are moving fast — which is when delta is most likely to
spike past the threshold. Cheap mitigation, flagged but not yet verified: a
plain ThinkorSwim price-level alert (notification only, not an order) as a
backstop so delta-watching doesn't depend solely on remembering to open
OO's Model tab.
