# ImpactRail V6 adversarial audit

Date: 2026-09-07

## Steward requests addressed

1. **Independent evidence:** positive payout now requires official npm Registry
   identity plus historical npm Downloads adoption. GitHub evidence alone cannot
   unlock custody.
2. **Bounded thresholds:** creation rejects commit thresholds above the complete
   250-commit verifier bound, npm thresholds outside 1–1,000,000, inverted or
   future periods, and periods longer than 31 days before accepting custody.
3. **Protection tests:** Direct Mode covers the objective happy path, adoption
   below threshold, repository/gitHead/period mismatch, transport failure,
   invalid model output, validator differential adoption, terminal replay,
   custody conservation, withdrawal and the retry cap.
4. **Redeployment parity:** PASS at `0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a`;
   deployed and reviewed source hashes both equal `9aa7e0e2dd2e352bd5d386657d2bdaec137fab48c1d0002966db61772e8bf9d4`.
5. **Production frontend:** V6 fields, bounds, address and version gate are configured.
6. **Full frontend lifecycle:** contract-level fail-closed and refund lifecycle
   is PASS. A browser-wallet journey and live positive npm payout remain pending
   and are not represented as completed.

## Local results

- GenVM lint and validation: PASS (12 public methods).
- V6 Direct Mode contract suite: PASS, 18 tests.
- Frontend receipt/journal suite: PASS, 5 tests.
- Production frontend build: PASS.

## Live V6 result

Five Studionet calls finalized successfully: beneficiary registration, exact
funding, evaluation, expiry, and sponsor refund. Evaluation readback was
`INSUFFICIENT_EVIDENCE / NPM_SOURCE_UNAVAILABLE`; beneficiary due stayed zero
and the entire deposit remained locked. After the 120-second deadline, expiry
and withdrawal returned all `1,000,000,000,000 wei`; the grant is `PAID` and
contract balance, locked funds, and both claim reserves are zero. Transaction
receipts and scoped claims are recorded in
`evidence-package/v6-live-lifecycle.json`.

Warnings about unused mocks in early-return failure tests are expected: once an
upstream source fails closed, downstream sources and the model must not run.

## Honest limitations

npm download counts demonstrate package acquisition, not social value or unique
human users. Package publishers can influence downloads, so the threshold is an
objective, independently fetched adoption signal rather than proof of impact by
itself. The bounded model still assesses substantive delivery, but cannot bypass
any canonical binding or determine payout arithmetic.

## Work that must happen after deployment

Publish a real npm package whose immutable version metadata binds this repository
and exact `gitHead`, wait for an eligible historical Downloads API period, then
record a positive payout lifecycle. Also replay the browser-wallet journey with
reload reconciliation. These are explicitly pending rather than inferred from
the successful contract-level fail-closed lifecycle.
