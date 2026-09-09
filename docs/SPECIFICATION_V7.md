# ImpactRail V7 specification

V7 preserves the V6 canonical GitHub and npm proof obligations, deterministic
verdicts, bounded thresholds, append-only attempts and claim accounting. It
changes custody intake after a live V6 test disproved payable rollback refunds.

## Two-phase custody

1. `create_grant` is non-payable. It validates all identifiers, thresholds,
   dates and participant bindings and creates an immutable `DRAFT` with no
   locked value.
2. `fund_grant` accepts value only for an existing draft, from its sponsor, and
   only at the exact sealed amount. A valid call fixes the deadline and moves
   the record to `FUNDED`.
3. Every non-zero invalid funding call returns normally as `REFUND_CLAIMABLE`,
   credits the full value to the actual sender, and leaves grant state and
   locked accounting unchanged.
4. `withdraw_unallocated` zeroes that sender's credit before requesting the
   transfer. The public `get_unallocated_refund` readback exposes the amount.

No payable input-validation branch uses a rollback as a refund mechanism.

## Invariants

`deposited = locked + beneficiary_claimable + sponsor_claimable +
unallocated_claimable + outbound_requested`.

Contract balance must cover all locked and claimable categories. AI cannot
choose custody state, address, amount, source, threshold result or payout
arithmetic.

## Candidate acceptance

Before deployment: lint and validation pass, Direct Mode covers the two-step
happy path, invalid terms before value, missing/wrong/repeated/outsider funding,
unallocated withdrawal, canonical evidence failures, differential validation,
terminal replay, retry cap and accounting conservation. Frontend tests and build
must pass with a V7 version gate and separate transaction journals.

After deployment: verify exact source parity; then run a valid draft/fund/
fail-closed/expiry/refund lifecycle and live invalid-funding/recovery call. V7
must not be represented as production-verified before those readbacks exist.
