# V5 live status

Address: `0x6027309e88CB1f51f891Eea85436ad80347592DB`.

Deployed source SHA-256 equals local source SHA-256:
`a6adf413020ea7511b86526601db3a4b942db2e9507c329f8880e752916ec3e4`.
Initial contract balance and accounting were zero.

Grant 0 completed registration, funding, evaluation and both withdrawals. All
five transactions finalized, all non-idle leader executions succeeded, and each
had a validator majority agreeing. Canonical bindings were YES. The model
observed PARTIAL and SUBSTANTIVE, so deterministic accounting assigned
500,000,000,000 wei to each party.

Authoritative final readback showed PAID, contract balance zero, locked zero and
both claimable totals zero. Relative to the initial snapshot, sponsor balance was
down 500,000,000,000 wei and beneficiary balance was up 500,000,000,000 wei.
Machine-readable evidence is in `evidence-package/v5-live-lifecycle.json`.

Three live negative calls were then executed against the finalized grant:

- a second beneficiary withdrawal finalized with `NOT_CLAIMABLE`;
- retrying the terminal grant finalized with `GRANT_TERMINAL`;
- retrying a nonexistent grant finalized with `GRANT_NOT_FOUND`.

Every non-idle leader execution returned the expected contract error. Contract
balance, locked funds, deposited/outbound totals and both claimable totals were
identical before and after the calls. Machine-readable receipts and readbacks
are in `evidence-package/v5-negative-calls.json`.

This is one V5 PARTIAL lifecycle plus three V5 live negative calls. The broader
FULL/PARTIAL/REJECTED/EXPIRED matrix was performed on V4 before the findings were
patched. Local V5 tests cover those fixed paths, but a broad V5 live outcome
matrix is not claimed.
Fixture evidence is controlled by the repository maintainer and is not
independent certification of real-world impact.
