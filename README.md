# ImpactRail

ImpactRail is a GenLayer intelligent contract and companion frontend for a
narrow public-goods grant workflow. A sponsor locks exact native GEN against a
beneficiary and a sealed milestone. The contract constructs and checks three
canonical sources: GitHub API commit history, npm registry release metadata,
and a closed Snapshot proposal. Validators acquire the sources independently;
the bounded model observes only delivery/materiality. The contract derives the
verdict and payout, so a contributor cannot self-author evidence or choose the
recipient of a reward.

## Status

The source has passed Python compilation, GenVM lint/schema validation, 13
Direct Mode tests, and a production frontend build. It is not deployed by this
repository. A live deployment address and live readback must be added after the
deploying wallet transaction; the frontend intentionally remains disabled until
`VITE_CONTRACT_ADDRESS` identifies an `IMPACT_RAIL_V2` contract.

## Local gates

```powershell
cd 'G:\Genlayer 4\ImpactRail'
genvm-lint check contracts/impact_rail.py --json
pytest -q
cd frontend
npm run build
```

The test fixtures are synthetic canonical API responses for Direct Mode only;
they do not claim live GitHub, npm, Snapshot or Studionet evidence. See
`docs/RELEASE_EVIDENCE.md` for the honest release checklist.

The current V2 contract has no constructor inputs. Its short Studionet evidence
window is fixed at 120–900 seconds.
