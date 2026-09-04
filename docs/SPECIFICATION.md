# ImpactRail specification

## Product boundary

ImpactRail verifies one public-goods grant at a time. The grant has one sponsor,
one beneficiary, one GitHub repository and commit range, one raw artifact path/digest,
one Snapshot proposal and one exact native GEN deposit. It does not execute
treasury payments, distribute ERC-20 tokens, accept images or accept arbitrary
evidence URLs.

## Sealed terms

The funding call seals beneficiary, amount, repository identifiers, base and
target commits, raw artifact path/SHA-256, Snapshot space/proposal, milestone text, minimum
commit/contributor thresholds, coverage start, testnet deadline and partial
payout basis points. Source URLs are derived inside the contract. The terms
digest is append-only; stale or replayed results are rejected.

## State machine

`FUNDED` → `INSUFFICIENT_EVIDENCE` (retryable) or one terminal claim state:
`VERIFIED_CLAIMABLE`, `PARTIAL_CLAIMABLE`, `REFUND_CLAIMABLE`. A deadline turns
`FUNDED` or `INSUFFICIENT_EVIDENCE` into `EXPIRED_REFUND_CLAIMABLE`. Claim
withdrawals move due amounts into `outbound_requested`; when both dues are zero,
the record is `PAID`.

## Deterministic verdicts

The observation schema has source-bound booleans for repository identity, commit
binding, commit-scoped artifact binding, Snapshot authorization and coverage, plus model fields
`delivery` and `materiality`. Any known source `NO` is `REJECTED`; unknown,
transport failure, invalid schema or disagreement is retryable insufficient
evidence; `FULL + SUBSTANTIVE` is `VERIFIED`; `PARTIAL + SUBSTANTIVE` is
`PARTIAL`; no delivery or cosmetic materiality is rejected. AI never chooses
amounts, addresses or state transitions.

## Invariants

The contract checks exact attached value and direct wallet/origin equality.
Accounting is `deposited = locked + beneficiary_claimable + sponsor_claimable + outbound_requested`;
contract balance must cover remaining locked and claimable reserves. Due amounts
are zeroed before requesting a transfer, and an entitled party can withdraw only
its own due balance.
