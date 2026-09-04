# Snapshot proposal template for the live fixture

Create a testnet Snapshot single-choice proposal in the chosen space with exact
choices `For`, `Against`, `Abstain`. Wait until it is closed and scores are
final. Replace `TARGET_COMMIT` only after the release commit exists.

```text
impactrail_repo: macdon3202/IMPACTRAIL
impactrail_package: impactrail-evidence-2026
impactrail_version: 1.0.0
impactrail_beneficiary: BENEFICIARY_ADDRESS
impactrail_amount_wei: EXACT_GRANT_AMOUNT

Authorize the ImpactRail public-goods release milestone represented by the
sealed GitHub target commit and npm version. The milestone is complete only if
the repository, immutable npm gitHead, beneficiary, amount and final vote all
match the sealed grant terms.
```

The proposal is not valid evidence until the Hub returns its canonical record
as closed with final scores and the exact markers above.
