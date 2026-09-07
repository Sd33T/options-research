# SPX RIC 0DTE — Reverse Iron Condor

OO saved test: `*SPX RIC--0 DTE--Daily--v2.1` (SPX, May 16 2022 - present,
235 trades as of the Sep 7 2026 pull).

## Structure
- Buy 40Δ put, buy 50Δ call (0DTE) — long inner strangle, roughly ATM.
- Sell call at (long call strike + 35pts), sell put at (long put strike - 35pts)
  — short outer wings, 0DTE. Net debit, defined risk both directions.
- Median debit ~15.3 points/lot ($1,530/contract); debit is clustered 13-16pts
  across essentially all VIX regimes (see Findings — VIX bucket note).

## Entry filter
- Window 9:35am-12:30pm, daily frequency, 2% portfolio allocation.
- VIX overnight move down >= 0.02, VIX intraday move down >= 1%.
- Max entry premium <= 16 points ($1,600/contract) — see reference/oo-export-schema.md,
  this field's unit is points despite the $ sign in the UI.
- Author's own version note (from OO): threshold was swept 0.01->0.1 for the
  VIX O/N-down filter; 0.02 was the best of the sweep, tighter than 0.02 wasn't
  tested, looser (up to 0.1) diminished outcomes.

## Baseline performance (v2.1, full history)
P/L $165,593 | CAGR 25.4% | Max DD -4.1% | MAR 6.2 | Sharpe 2.10 | Sortino 4.01
| Win% 64.3% (151/235) | Avg/trade $413/lot | Avg winner $1,113/lot | Avg loser
-$847/lot | Max winner $2,235/lot | Max loser -$1,605/lot | Avg hold 5.4hr |
100% of exits are "Expired" — no active stop/profit-target configured.

## Greeks profile (structural, not OO-computed — OO's backtester doesn't expose
a live per-trade Greeks feed; see reference/oo-export-schema.md)
- Delta: slightly long-biased at entry (50Δ call vs 40Δ put means the call leg
  dominates slightly) — small, not the main driver.
- Gamma: the whole trade. Long inner strangle is aggressively long gamma,
  extreme intraday for 0DTE especially near the close. This is what generates
  the convex payoff (max winner >> max loser on similar-sized debits).
- Theta: net negative (net debit), but the short wings partially offset it vs.
  a naked long strangle. Decay is brutal into the close, which is exactly why
  full-loss ("pin") trades go to -100%.
- Vega: net positive from the inner strangle, front-loaded (shrinks through
  the day as time value bleeds out).
- Charm/vanna: charm matters more than usual for a 0DTE hold of this length
  (~5.4hr avg) — position delta drifts meaningfully from time decay alone,
  independent of price action. Vanna direction depends on spot-vol correlation
  (down moves + IV pop reinforce each other here; up moves partially offset).

## Portfolio role
See ../../portfolio/correlation-notes.md. Correlation with the double-calendar
book is close to zero (not negative) — genuine diversification, not a designed
hedge. During the Jul-Aug 2026 drawdown specifically, most of the RIC's worst
days had no calendar trade open at all to cushion them.

See findings.yaml for the full, dated, confidence-tagged claim list —
including one significant correction (the VIX 20-25 "underperformance" turned
out to be a units bug + noise, not a real regime effect).
