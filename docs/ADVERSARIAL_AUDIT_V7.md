# ImpactRail V7 adversarial audit

Status: pre-deployment candidate.

## Finding that triggered V7

The V6 live threshold test produced all three expected rollback errors but left
the attached value in the contract outside its accounting. This is a critical
custody failure, recorded without correction in
`evidence-package/v6-threshold-negative.json` and
`docs/PAYABLE_ROLLBACK_INCIDENT_V6.md`.

## Remediation under test

- invalid terms are rejected by non-payable `create_grant`;
- a valid DRAFT locks no value until exact sponsor funding;
- missing grant, wrong amount, outsider and repeated payable funding return
  normally and credit a sender-owned unallocated refund;
- `withdraw_unallocated` follows effects-before-interaction;
- accounting includes the unallocated reserve;
- the frontend records creation and funding as distinct transactions and lets a
  sponsor resume funding from a DRAFT.

## Verified locally

- GenVM lint: PASS;
- GenVM validation: PASS, 15 public methods;
- V7 Direct Mode: 22 PASS;
- complete repository Python suite: 96 PASS;
- frontend receipt/journal tests: 5 PASS;
- production frontend build: PASS.

Unmatched mock warnings are expected in early-return failure cases because
downstream sources and the model must not execute after an upstream failure.

## Not yet verified

No V7 address, deployed-source parity or V7 live lifecycle exists yet. Positive
npm payout also remains pending a non-empty official historical npm Downloads
response. None of these are claimed by local tests.
