# ImpactRail V8 adversarial audit

Status: candidate awaiting its public canonical workflow run and deployment.

## Steward-request mapping

1. Payout no longer depends on npm's delayed daily counter or owner narrative.
   npm Registry identity, GitHub run identity, exact run commit, completed job
   steps and commit-pinned workflow bytes are reacquired by each validator.
2. Unsupported commit bounds and malformed workflow/run bindings are rejected
   by non-payable creation before custody.
3. Direct Mode covers positive verification, failed run, repository/gitHead/run
   commit/workflow mismatch, transport failure, invalid model output,
   validator disagreement, retry cap, terminal replay and claim conservation.
4. The V6 payable-rollback custody finding is fixed through two-phase intake and
   explicit sender refunds for missing, wrong-value, outsider or repeated funding.
5. The frontend journals draft creation and funding separately, supports
   resuming a DRAFT, rejects non-V8 deployments and never auto-resubmits.
6. Source parity, live payout, live invalid-funding recovery and the complete
   browser-wallet journey remain mandatory after deployment.

## Current local results

- GenVM lint and validation: PASS, 15 public methods;
- V8 Direct Mode: 23 PASS;
- frontend journal tests: 5 PASS;
- production frontend build: PASS.

## Honest limitations

The canonical workflow is objective technical verification, not evidence of
unique users, economic value or third-party adoption. The workflow is stored in
the project repository, so the contract requires GitHub's independent run/job
records, npm's independent package record and exact workflow bytes; it does not
pretend the project is an organizationally independent auditor.

No V8 deployment or live result is claimed yet.
