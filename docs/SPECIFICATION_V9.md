# ImpactRail V9 specification

V9 retains V8's non-payable DRAFT and explicit recoverable funding, but replaces
one oversized canonical acquisition with four independently finalized staged
gates: npm package, GitHub Actions run, Actions jobs, and commit-pinned workflow.
Each gate is validator-recomputed, one-shot, and recorded with the immutable
terms digest. Final GitHub delivery evaluation is impossible until mask `15`.

Acceptance requires: threshold rejection before custody; all staged source and
mismatch tests; positive Direct Mode payout; live staged gates; live beneficiary
withdrawal; authoritative accounting/balance readback; deployed-source parity;
and production frontend configured to the verified deployment.
