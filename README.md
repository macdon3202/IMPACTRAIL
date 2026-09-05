# ImpactRail

Live frontend: https://impactrail.pages.dev

ImpactRail is a GenLayer intelligent contract and companion frontend for a
narrow public-goods grant workflow. A sponsor locks exact native GEN against a
beneficiary and a sealed milestone. The contract constructs and checks three
canonical sources: GitHub API commit history, raw GitHub content at an exact commit,
and a published GitHub Release attestation. Validators acquire the sources independently;
the bounded model observes only delivery/materiality. The contract derives the
verdict and payout, so a contributor cannot self-author evidence or choose the
recipient of a reward.

## Status

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
historical evidence; the frontend accepts only V5. Three direct V5 negative
calls also finalized with the expected `NOT_CLAIMABLE`, `GRANT_TERMINAL` and
`GRANT_NOT_FOUND` errors, while authoritative accounting remained unchanged.
See `evidence-package/v5-live-lifecycle.json` and
`evidence-package/v5-negative-calls.json`. This is not a claim that the complete
outcome matrix was rerun live on V5.

## Local gates

```powershell
cd 'G:\Genlayer 4\ImpactRail'
genvm-lint contracts/impact_rail.py
gltest -q
cd frontend
npm run build
```

The test fixtures are synthetic canonical API responses for Direct Mode only;
they do not claim live GitHub, npm, Snapshot or Studionet evidence. See
`docs/RELEASE_EVIDENCE.md` for the honest release checklist.

The current V5 source has no constructor inputs. Its short Studionet evidence
window is fixed at 120–900 seconds.
