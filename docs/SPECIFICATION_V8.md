# ImpactRail V8 specification

## Product boundary

ImpactRail V8 releases a native-GEN public-goods grant only when a published
npm artifact, its exact GitHub delivery, and a successful canonical verification
run agree. It does not use screenshots, mutable branches, contributor-supplied
evaluation JSON, daily download counters, or arbitrary evidence URLs.

## Sealed proof obligation

The sponsor seals an exact npm name/version, repository, base and target commit,
artifact path and SHA-256, release tag and markers, bounded commit coverage,
verification commit, workflow path and SHA-256, and GitHub Actions run ID.

Validators independently acquire the public repository, exact commit, complete
bounded compare, raw artifact, published release, npm Registry metadata, GitHub
Actions run/jobs records, and workflow bytes at the run's exact head commit.

The run must be a completed successful push on `main`, belong to the sealed
repository, use the sealed workflow path, and report exactly one successful job.
Every required verification step must have a successful GitHub-owned job record.
The fetched workflow SHA-256 must equal the sealed digest.

This proves reproducible technical delivery, not download popularity or unique
users. Workflow contents remain project-authored, but narrative or a declared
digest alone is insufficient: npm and GitHub independently serve and bind the
package, run, jobs, commit and bytes.

## Custody and state machine

`create_grant` validates and seals a non-payable `DRAFT`. `fund_grant` moves an
exact sponsor payment into `FUNDED`. Any other non-zero payable funding returns
normally and credits the actual sender's `unallocated_claimable` balance;
`withdraw_unallocated` recovers it. No payable validation branch depends on
rollback for refunds.

After funding, bounded consensus, retry, expiry, deterministic FULL/PARTIAL/
refund accounting, terminal replay protection and effects-before-interaction
withdrawal rules apply.

## Acceptance matrix

- static lint and validation;
- Direct Mode happy, canonical mismatch, transport/model/validator failure,
  custody, recovery, replay and adversarial combinations;
- successful public canonical workflow at the exact candidate commit;
- deployment source parity;
- live valid funding and successful payout;
- live invalid funding and exact recovery;
- production frontend address/version parity, wallet journey and state readback.

Receipt finality without successful execution, validator agreement and state
readback is not PASS.
