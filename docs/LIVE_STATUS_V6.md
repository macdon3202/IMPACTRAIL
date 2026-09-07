# V6 live verification

Reconciled on 2026-09-07 at 05:17:21 UTC using read-only RPC calls.

- Contract: `0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a`
- Configuration: `IMPACT_RAIL_V6`
- Exact deployed/local SHA-256: `9aa7e0e2dd2e352bd5d386657d2bdaec137fab48c1d0002966db61772e8bf9d4`
- Evidence: `evidence-package/v6-live-lifecycle.json`
- Reconciliation command: `node scripts/reconcile_v6.mjs` (no signing or submission).

## Verified lifecycle

All five transactions are FINALIZED, with successful execution and majority
agree votes: beneficiary registration, funding, evaluation, expiry, refund.
Evaluation returned `INSUFFICIENT_EVIDENCE / NPM_SOURCE_UNAVAILABLE` and retained
the full 1,000,000,000,000 wei in custody. After expiry the sponsor withdrew it.

Refund transaction:
`0xeab31f767d98b7ca9a458740629cef5e1466d964a5a5e5e103d66b18af6be1ac`

Sponsor balance increased from 199941997000000000000 to 199941998000000000000
wei, exactly the grant amount. Beneficiary balance remained
199908001999999999998 wei. Grant 0 is `PAID` with verdict
`INSUFFICIENT_EVIDENCE` and reason `EXPIRED_UNRESOLVED`; here PAID means the
sponsor refund completed, not a successful impact payout. Contract balance,
locked funds and both claimable ledgers are zero.

## Scope and remaining release work

This demonstrates the missing-source rejection and expiry/refund path only.
Positive npm-backed payout, the complete browser wallet journey, V6 Cloudflare
deployment, GitHub publication and deployment-transaction capture remain
unverified. Earlier-version payout evidence does not establish a V6 payout.

Local regression rerun: 74 contract tests and 5 frontend transaction tests pass.
Pytest reports 18 unmatched-mock warnings on early-return negative paths.
