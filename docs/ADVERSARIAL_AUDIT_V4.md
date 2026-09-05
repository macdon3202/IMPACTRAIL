# V4 adversarial audit

Audit date: 2026-09-05. Deployment under test:
`0xb61678034F70E5aC688851c3Ab547f4E428E781e`.

## Live results

- FULL finalized and paid 1,000,000,000,000 wei to the beneficiary.
- A deliberately wrong artifact digest produced
  `GITHUB_ARTIFACT_DIGEST_MISMATCH`; the beneficiary received nothing and the
  sponsor refund was requested.
- An honestly incomplete two-part milestone produced PARTIAL. The beneficiary
  and sponsor each received 500,000,000,000 wei; balances were checked after
  asynchronous transfers settled.
- Second withdrawal, retry after terminal state and evaluation of a missing
  grant all returned contract errors. Accounting did not change.
- EXPIRY reached `EXPIRED_REFUND_CLAIMABLE`, then PAID after the sponsor withdrew.

## Findings fixed in source

1. Unlinked Git commit author names counted as contributors. The patched source
   counts only GitHub-controlled `author.login`.
2. Commit and release timestamps had no upper bound. The patched source rejects
   timestamps later than observation time.
3. Changing policy fields could reuse the same evidence. The patched evidence
   key binds sponsor, beneficiary, amount and canonical evidence identity.
4. Digests contained whole mutable GitHub API objects. The patched source hashes
   stable decision fields and retains raw response digests for audit history.
5. The frontend could display success without proof of successful contract
   execution. Receipt parsing now checks non-idle leader receipts.

The fixes form V5 and pass 56 direct contract tests, including differential validator tests,
and five frontend transaction tests. They change contract bytes and are not in
the deployment above. A new deployment and source-parity check are required.

## Scope limitation

The release and artifact are maintained in the same repository. They are
canonical and reproducible, but do not independently prove real-world impact.
The live PARTIAL result is a model observation over an intentionally incomplete
milestone, not an externally certified audit result.
