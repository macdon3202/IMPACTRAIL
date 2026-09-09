# ImpactRail

Live frontend: https://impactrail.pages.dev

ImpactRail is a GenLayer intelligent contract and companion frontend for a
public-goods grant workflow. The V8 candidate requires reproducible delivery:
official npm Registry metadata must bind an exact package version to the sealed
GitHub repository and commit, and a successful GitHub Actions run must bind the
exact verification commit, workflow bytes and completed job steps. GitHub commit,
raw artifact and release evidence remain
mandatory provenance, but project-authored narrative can no longer unlock a
payout by itself. Validators reacquire every source independently and the
contract derives the verdict, amount and recipient deterministically.

## Status

V8 is the current candidate and is not deployed. It removes the delayed npm
Downloads dependency and uses canonical npm identity plus commit-pinned GitHub
run/job evidence that can complete in the same day. It retains V7's replacement
of payable grant creation with non-payable validation followed by explicit funding. Invalid
payable funding is credited to a withdrawable sender refund rather than relying
on transaction rollback. GenVM lint/validation, 23 V8 Direct Mode tests, five
frontend tests and the production build pass. See `docs/SPECIFICATION_V8.md`
and `docs/ADVERSARIAL_AUDIT_V8.md`. V7 was never deployed.

V6 is deployed at `0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a`
but is superseded and must not receive new funds. A 2026-09-09 live test showed
that three payable rollbacks left 3,000,000,000,000 wei outside grant accounting.
See `docs/PAYABLE_ROLLBACK_INCIDENT_V6.md` and
`evidence-package/v6-threshold-negative.json`.
Canonical configuration and exact source parity have been verified. Live
readback shows the insufficient-evidence grant expired and reached `PAID`
after sponsor withdrawal, with zero balance and outstanding claims. Receipt
and balance reconciliation is recorded in `docs/LIVE_STATUS_V6.md`.
GenVM lint/validation, 18 V6 Direct Mode contract tests, five frontend receipt
and journal tests, and the production build pass. Unsupported commit counts
above 250 and invalid npm thresholds/periods are rejected before custody. The
local frontend now requires V8 and remains transaction-disabled until a V8
address passes its version gate.
Live positive npm-backed payout and the browser wallet journey remain unverified.
The public package, exact Registry `gitHead`, commit-bound GitHub Release and a
real consumer installation are now prepared; only the official daily Downloads
API aggregation is pending. See `docs/NPM_CANONICAL_RESOURCE.md`.
See `docs/SPECIFICATION_V6.md` and
`docs/ADVERSARIAL_AUDIT_V6.md`.

The patched V4 source has passed GenVM lint, 31 direct-contract tests and a
production frontend build. A no-funds GenVM probe reached all five fixed GitHub
sources with HTTP 200. The previous V4 grant failed closed on HTTP 403 and was
fully returned to its sponsor after expiry. The patched deployment at
`0xb61678034F70E5aC688851c3Ab547f4E428E781e` passed a funded FULL payout
lifecycle on 2026-09-05: source bytes matched, all four transactions finalized,
and the beneficiary received exactly 1,000,000,000,000 wei. Contract balance and
all outstanding claims are zero. See `evidence-package/patched-v4-payout.json`.
This does not establish a complete live adversarial matrix or independent
real-world impact: the fixture artifact and release are controlled by this repo's
maintainer, and the model's substantive-delivery judgment is an observation.

The subsequent adversarial audit completed FULL, PARTIAL, REJECTED and EXPIRED
paths and found four contract issues plus a frontend receipt issue. Those fixes
are now deployed as V5 at `0x6027309e88CB1f51f891Eea85436ad80347592DB`.
Source parity and a complete PARTIAL lifecycle are verified: 500,000,000,000 wei
went to each party and all reserves returned to zero. The V4 address remains
historical evidence; the current local frontend accepts only V6. Three direct V5 negative
calls also finalized with the expected `NOT_CLAIMABLE`, `GRANT_TERMINAL` and
`GRANT_NOT_FOUND` errors, while authoritative accounting remained unchanged.
See `evidence-package/v5-live-lifecycle.json` and
`evidence-package/v5-negative-calls.json`. This is not a claim that the complete
outcome matrix was rerun live on V5.

## Local gates

```powershell
cd 'G:\Genlayer 4\ImpactRail'
genvm-lint check contracts/impact_rail_v8.py
pytest -q tests/test_impact_rail_v8.py
cd frontend
node --test transactions.test.mjs
npm run build
```

The test fixtures are synthetic canonical API responses for Direct Mode only;
they do not claim live GitHub, npm, Snapshot or Studionet evidence. See
`docs/RELEASE_EVIDENCE.md` for the honest release checklist.

The V8 source has no constructor inputs. Its short Studionet evidence window is
fixed at 120–900 seconds. V6 and earlier addresses remain historical evidence.
