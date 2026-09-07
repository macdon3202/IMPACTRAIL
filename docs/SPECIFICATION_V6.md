# ImpactRail V6 specification

## Product boundary

ImpactRail settles one native-GEN public-goods grant against a sealed npm
package release. It does not accept arbitrary evidence URLs, screenshots,
owner-supplied JSON, ERC-20 custody, or mutable branch content.

## Actors and custody

- Sponsor seals the terms and deposits the exact amount.
- A separately registered beneficiary may evaluate and claim only its due.
- Either participant may trigger verification; neither supplies evidence at
  evaluation time.
- Validators independently fetch the derived canonical URLs.

## Sealed inputs

The immutable terms bind sponsor, beneficiary, amount, GitHub owner/repository,
base and target commits, raw artifact path and SHA-256, release tag and markers,
milestone statement, commit/contributor thresholds, npm package and version,
historical download dates and threshold, partial payout basis points, and the
deadline. The terms digest is verified before every evaluation.

## Independent proof obligation

A positive payout requires all of the following:

1. Public GitHub repository identity, exact target commit and complete compare
   range of at most 250 commits.
2. Raw artifact bytes at that commit matching the sealed SHA-256.
3. Published, non-draft release markers binding repository, commit, artifact,
   beneficiary and amount.
4. Official npm Registry metadata binding exact package/version, repository and
   `gitHead` to the same GitHub target commit.
5. Official npm Downloads response binding exact package and sealed historical
   dates, with an integer count meeting the sealed threshold.
6. Bounded AI classification of substantive FULL or PARTIAL delivery.

Project-authored GitHub narrative is necessary provenance but is never
sufficient: npm adoption is a mandatory independent gate.

## Deterministic state machine

`FUNDED` may become retryable `INSUFFICIENT_EVIDENCE`, or terminal
`VERIFIED_CLAIMABLE`, `PARTIAL_CLAIMABLE`, or `REFUND_CLAIMABLE`. Unresolved
records become `EXPIRED_REFUND_CLAIMABLE` at the deadline. Successful withdrawal
zeroes the due before requesting the transfer and eventually records `PAID`.
At most three evaluations are permitted.

## Failure taxonomy

- Objective mismatch: terminal rejection and sponsor refund.
- Transport, malformed source, model failure, or validator disagreement:
  retryable insufficient evidence, no claimable payout.
- Unsupported thresholds or dates: creation reverts before funds are recorded.
- Replay, stale state, wrong caller, early expiry, or duplicate evidence:
  transaction reverts with accounting unchanged.

## Invariants

`deposited = locked + beneficiary_claimable + sponsor_claimable + outbound_requested`.
Remaining balance covers locked plus claimable reserves. AI never chooses an
address, amount, state transition, threshold result, source URL or transfer.

## Acceptance matrix

V6 is deployable only after GenVM lint/validation, Direct Mode positive and
negative paths, validator differential checks, frontend receipt/journal tests,
and a production build pass. Production configuration remains blank until the
new address reports `IMPACT_RAIL_V6`, deployed source hash matches the reviewed
source, and a complete live frontend journey receives canonical state readback.
