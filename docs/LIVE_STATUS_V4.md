# V4 live status — failed evaluation safely recovered

The deployment at `0x377A27B57116eB21b2781879348676E4d71170F1`
returned `INSUFFICIENT_EVIDENCE` twice with `SOURCE_HTTP_403`. The original
contract did not identify which of its five requests failed. It did not release
funds on either attempt.

After deadline, transaction
`0x7ed0d881b71502ef04323db9affa48b37f238d6ef1dcbc546efb2e3be5b2435b`
made the sponsor refund claimable. Transaction
`0xf42fbbd8fe525148498f6d5edcc2594049edc25a95b68f8a15551d49c4d907ce`
returned it. Authoritative readback showed `PAID`, contract balance `0`, locked
`0`, both claimable totals `0`, and sponsor balance delta exactly
`1000000000000` wei.

The patched source adds GitHub's recommended `User-Agent`, media type and API
version headers, performs requests sequentially, and records a bounded source-
specific failure code. A diagnostic contract then fetched the repository,
commit, comparison, raw artifact and release from GenVM; all returned HTTP 200.
The observed response sizes were respectively 5165, 4361, 11881, 699 and 2406
bytes. Since the same repository endpoint also returned 200 without headers
during the later probe, the historical 403 cannot honestly be attributed solely
to a missing header; a transient or rate-limit response remains possible.

## Patched deployment — 2026-09-05

Address: `0xb61678034F70E5aC688851c3Ab547f4E428E781e`.
Deployed bytes match SHA-256
`ad94b173a02d2379eff800ae6600d47cb43234909da6cc59613480d16d90d608`.
Grant 0 completed registration, funding, evaluation and withdrawal, all FINALIZED
with successful execution and a majority agreeing. Evaluation returned VERIFIED
on its first attempt; delivery FULL and materiality SUBSTANTIVE were model outputs.
The beneficiary's balance increased by exactly 1,000,000,000,000 wei. Contract
balance, locked funds and both claimable balances are zero.

Immediately after withdrawal was accepted, state was PAID but the outgoing
transfer had not yet changed balances. At 01:33:38 UTC the final readback confirmed
actual delivery. Evidence: `evidence-package/patched-v4-payout.json`.

The later adversarial matrix also finalized PARTIAL, REJECTED and EXPIRED paths.
All four grants ended PAID; aggregate contract balance and all claimable ledgers
returned to zero. Sponsor and beneficiary balance deltas matched FULL plus the
sealed 50% PARTIAL payout. See `evidence-package/live-adversarial-matrix.json`.

That audit exposed issues documented in `ADVERSARIAL_AUDIT_V4.md`. They are fixed
in V5 source and require a new deployment. The tiny artifact commit and
maintainer-authored release do not independently prove the full milestone.
