# ImpactRail V8 adversarial audit

Status: deployed and custody-safe, but live positive payout not achieved.

The first public run (`34325485141`) failed before contract execution because
the test harness selected its unavailable latest release (`v0.3.0-rc7`) instead
of the contract's documented `v0.2.16` runtime. npm binding, package installation
and contract validation had succeeded. The failure is retained in GitHub Actions
history; Direct Mode now explicitly selects `v0.2.16`, whose official release
artifact remains available, and requires a fresh complete run.

The replacement public run
[`34328794332`](https://github.com/macdon3202/IMPACTRAIL/actions/runs/34328794332)
completed successfully at commit
`3469b3ff604d4e2d72bf1da3534f9bd427fd5d58`. It passed npm Registry
binding, installation of the published package, GenVM lint and validation,
all 23 V8 Direct Mode tests, all 5 frontend journal tests and the production
frontend build. The failed predecessor remains visible rather than being
concealed or overwritten.

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

## Canonical verification

- GitHub commit: `3469b3ff604d4e2d72bf1da3534f9bd427fd5d58`;
- workflow run: `34328794332`, conclusion `success`;
- workflow path: `.github/workflows/verify-impactrail-v8.yml`;
- workflow SHA-256: `a7d4b7201f5bef5a07da2eb4e3e6ad3176d181bf016d9cf95b55a15b97fff6e1`;
- contract SHA-256: `7d29f563af347b1a796d67e7464c4c25e13aeb526e070413f29b1a54a5da6b4c`.

## Honest limitations

The canonical workflow is objective technical verification, not evidence of
unique users, economic value or third-party adoption. The workflow is stored in
the project repository, so the contract requires GitHub's independent run/job
records, npm's independent package record and exact workflow bytes; it does not
pretend the project is an organizationally independent auditor.

## Studionet lifecycle result

V8 was deployed at `0xbD64f40726d717B0f436AAf7c85c2C1f46692838`.
The initial config readback matched `IMPACT_RAIL_V8` and the seven documented
canonical sources. Invalid funding of `1000000000000` wei was credited to the
sender and fully recovered through `withdraw_unallocated`; the authoritative
contract balance returned to zero.

Grant 0 then completed DRAFT creation and exact funding. Three independent
evaluation transactions consistently returned `CANONICAL_VERIFICATION_UNAVAILABLE`.
Repository, commit coverage, artifact digest and release binding were all `YES`,
but package/adoption binding remained `UNKNOWN`. Funds stayed locked through all
attempts. After the sealed deadline, expiry and sponsor withdrawal succeeded;
the final authoritative readback shows state `PAID`, all locked/claimable ledgers
zero, and contract balance zero.

This is a successful fail-closed and recovery lifecycle, not a successful live
beneficiary payout. V8 must not be submitted as satisfying the steward's full
positive-path request. The next revision must identify the unavailable endpoint
explicitly and use a canonical source proven reachable from Studionet validators.
