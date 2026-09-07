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
