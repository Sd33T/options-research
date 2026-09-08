# Options Research — Index

Read this first. One paragraph per strategy, pointing into its own folder for
detail. The point of this repo: never re-derive a finding Claude (or you)
already checked — look here first, then extend it.

Reference: `reference/oo-export-schema.md` — OptionOmega CSV export column
definitions and unit conventions. Read before writing any analysis script
against an OO export; a units mistake here already cost a wasted round-trip
once (Sep 7, 2026).

Reference: `reference/significance_testing.py` — reusable stats toolkit
(Fisher's exact, permutation test, Welch t-test, Mann-Whitney U, omnibus
chi-square, Bonferroni correction, power analysis). Use it any time a new
strategy idea rests on "this subgroup of trades looks better/worse than the
rest" — that exact pattern produced a false alarm on the RIC's VIX 20-25
bucket (see its findings.yaml) before this test suite caught that it was
noise from scanning 5 buckets post-hoc.

## How to use this repo when evaluating a new strategy idea

1. Check `findings.yaml` in the relevant strategy folder(s) first — don't
   re-derive something already tested. Only trust entries tagged
   `confidence: high` and `status: closed` as settled; `open` or `low`
   confidence entries are explicitly unresolved, not confirmed either way.
   A `confidence: retracted` entry means exactly what it says — read why
   before assuming the superseding entry alone tells the whole story.
2. If the new idea implies a subgroup comparison (a VIX regime, a time-of-day
   window, a DTE bucket, etc.), run it through
   `reference/significance_testing.py` before writing up a causal story.
   Small-n backtest subsets produce convincing-looking noise constantly —
   see the VIX 20-25 episode for what that looks like before it's corrected.
3. If the new idea is pitched as a portfolio diversifier against an existing
   strategy, check `portfolio/correlation-notes.md`'s methodology (actual
   daily P/L correlation, not just "these are structurally opposite") before
   claiming a hedge relationship exists.
4. Cross-strategy priors worth weighing against, not treating as settled
   law: every active-exit variant tested on the RIC (profit target, stop
   loss, time exit) reduced risk-adjusted returns vs. holding to expiration
   — profit targets specifically cut the convex tail that a long-gamma
   structure depends on. If a new idea leans on an early-exit rule for a
   similar long-gamma/long-vol structure, that prior is worth explicitly
   re-testing against, not assuming will hold or won't.

## Strategies

- **[SPX RIC 0DTE](strategies/spx-ric-0dte/README.md)** — reverse iron condor,
  0DTE, long-gamma/long-vol debit structure. Most fully analyzed strategy in
  this repo so far: full Greeks writeup, VIX-regime breakdown, three active-exit
  variants tested (all worse than doing nothing), portfolio correlation check
  against the double calendars. See its findings.yaml for the closed/open
  question list.
- **[SPX DC 1/2](strategies/spx-dc-1-2/README.md)**, **[SPX DC 5/7](strategies/spx-dc-5-7/README.md)**
  — double calendar variants. Current focus, per Ryan (Sep 7, 2026). Only
  pulled so far for the RIC correlation check (see portfolio/correlation-notes.md)
  — no dedicated Greeks/regime analysis done yet on either individually.
- **[SPX DC 14/28](strategies/spx-dc-14-28/README.md)** — double calendar
  variant, not currently a focus (deprioritized alongside removal of the
  9/23-DTE test below; may return to it later).
- **[SPX Butterfly 14DTE 50D/40W](strategies/spx-butterfly-14dte-50d-40w/README.md)**
  — long call butterfly, 14 DTE, 50-delta center, +/-40 wings. Two variants
  reviewed side by side (v2: profit-target-only, models a resting GTC order;
  v2.2: profit-target + delta exit, models full OO bot automation) — see its
  findings.yaml for the open question on which execution model applies.
  First-pass review only (structure + headline outcomes); no Greeks/regime
  or correlation work done yet.
- **[SPX PCS 0DTE](strategies/spx-pcs-0dte/README.md)** — put credit spread,
  0DTE, bullish-continuation entry filter. Reviewed Sep 8, 2026 as part of
  auditing the "Claude portfolio test" OO portfolio. Recommendation: leave
  out of the live portfolio — weakest risk-adjusted profile of the five
  strategies reviewed (Sharpe 1.34), and positively correlated with the RIC
  (+0.355 on overlap days, the strongest relationship in the whole
  correlation matrix and in the wrong direction for diversification).

## Portfolio-level

- **[portfolio/correlation-notes.md](portfolio/correlation-notes.md)** — RIC
  vs. double-calendar daily P/L correlation, and a specific look at whether the
  calendar book cushions the RIC's Jul-Aug 2026 drawdown (short answer: not
  really — correlation is ~0, and 2 of 4 calendars had zero trades open during
  that window). Updated Sep 8, 2026 with a full five-strategy pairwise
  correlation matrix (Butterfly, DC 1/2, DC 5/7, RIC, PCS) covering the
  "Claude portfolio test" OO portfolio — see that file for the current read:
  DC 5/7 is the closest thing to a real complement to the Butterfly (-0.193
  on overlap days), PCS and RIC are positively correlated (the one pairing
  to actively avoid), and DC 1/2's diversification case is still unproven
  (near-zero or weakly positive against everything, and rarely even open
  when the others draw down).

## Removed / deprioritized

- **DC "9/23" / "11/23" test — removed Sep 7, 2026.** Ryan's working notes
  called this calendar "9/23 DTE," but the actual saved OO test was labeled
  "11/23" — a naming discrepancy that was never resolved (unclear if it's a
  typo somewhere, or the DTE window changed at some point without the label
  updating). Rather than carry ambiguous data forward, its README and CSV
  were deleted from `strategies/`, and its numbers were removed from
  portfolio/correlation-notes.md. If this strategy comes back into scope,
  re-pull it fresh from OO and confirm its actual DTE window before
  re-adding — don't resurrect this deleted data as-is.
- QQQ 14/28 DTE calendar — disregarded for now (Ryan, Sep 7, 2026). Was
  referenced in an old saved OO Portfolio name but never located as a
  standalone saved test.
- Two of four Butterfly variants reviewed (14 DTE, 50D/40W — see above).
  Two more Butterfly variants still exist in the OO account, not yet
  reviewed.

## Known gaps (not yet done, flagged so nobody assumes they're done)

- No dedicated strategy README/findings yet for DC 1/2 or DC 5/7 (current
  focus) — only the RIC has full writeups so far.
