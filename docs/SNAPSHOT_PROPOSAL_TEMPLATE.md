# Snapshot proposal template for the live fixture

Create a testnet Snapshot single-choice proposal in the chosen space with exact
choices `For`, `Against`, `Abstain`. Wait until it is closed and scores are
final. Replace `TARGET_COMMIT`, beneficiary and amount only after the V3 commit exists.

```text
impactrail_repo: macdon3202/IMPACTRAIL
impactrail_target_commit: TARGET_COMMIT
impactrail_artifact_path: evidence/impact-report.md
impactrail_artifact_sha256: 2d5a5f2947353d0a7d1d388c2b1b530df26595e6de2d921112403e04902da692
impactrail_beneficiary: BENEFICIARY_ADDRESS
impactrail_amount_wei: EXACT_GRANT_AMOUNT

Authorize the ImpactRail public-goods release milestone represented by the
sealed GitHub target commit and raw delivery artifact. The milestone is complete only if
the repository, immutable commit-scoped artifact digest, beneficiary, amount and final vote all
match the sealed grant terms.
```

The proposal is not valid evidence until the Hub returns its canonical record
as closed with final scores and the exact markers above.
