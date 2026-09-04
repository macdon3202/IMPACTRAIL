# ImpactRail

ImpactRail is a GenLayer intelligent contract and companion frontend for a
narrow public-goods grant workflow. A sponsor locks exact native GEN against a
beneficiary and a sealed milestone. The contract constructs and checks three
canonical sources: GitHub API commit history, raw GitHub content at an exact commit,
and a closed Snapshot proposal. Validators acquire the sources independently;
the bounded model observes only delivery/materiality. The contract derives the
verdict and payout, so a contributor cannot self-author evidence or choose the
recipient of a reward.

## Status

The source has passed Python compilation, GenVM lint/schema validation, 14
Direct Mode tests, and a production frontend build. V2 is deployed on Studionet
at `0x39e5Dc71024E358474EFC78fBC880213Ef1d1caf`; public configuration and zeroed
pre-funding accounting have been read back. A funded live lifecycle remains to
be run and is not claimed here.

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
