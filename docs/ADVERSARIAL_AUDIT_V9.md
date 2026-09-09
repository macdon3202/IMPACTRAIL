# ImpactRail V9 adversarial audit

Status: deployed; staged canonical gates and funded settlement verified live.

Covered locally: incomplete gates, failed canonical run, duplicate gate replay,
terminal replay, unsupported commit bounds, invalid payable funding recovery,
source transport failure, invalid model output, successful payout and withdrawal
conservation. The live probe established two-round deterministic reachability of
all four staged endpoints. Deployment `0x8bc22E809b85EF6568DD1083108F495f33d276FA`
then completed a funded lifecycle: all gates reached mask 15, deterministic
settlement returned `PARTIAL`, both parties withdrew 500,000,000,000 wei, and
authoritative readback ended at `PAID` with zero contract balance, locked funds,
or claimable ledgers. Production is configured for this address. A complete
browser-wallet journey has not been claimed; that remains a disclosed limitation.

The live result and every transaction hash are recorded in
`evidence-package/v9-live-lifecycle.json`. Earlier V8 failures remain preserved
and are not represented as successful V9 evidence.

Canonical run
[`34336729341`](https://github.com/macdon3202/IMPACTRAIL/actions/runs/34336729341)
completed successfully at commit
`19e1c7ee715f37cc1d7a23ba8df7695e9938de29`. Contract source SHA-256 is
`f4bfcdd00666d44293ad6ab03a0c52f9a9b525ec114b161ca43f4f073df26fa2`.
