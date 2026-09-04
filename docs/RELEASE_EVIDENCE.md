# Release evidence and deployment gates

## Completed locally

- Contract source compiles with Python.
- `genvm-lint check contracts/impact_rail.py --json` passes lint and schema.
- Direct Mode: 14 tests pass, including verified, partial, mismatch refund,
  HTTP failure/expiry, malformed model, prompt injection, unauthorized calls,
  duplicate withdrawal and accounting readback.
- Frontend `npm run build` passes with the supplied logo asset.

## Studionet deployment readback

- Address: `0x2c1b0842da58927d1653614DB29D36053e63E487`
- `get_config().version`: `IMPACT_RAIL_V1`
- `get_config().profile`: `testnet`
- Evidence window: 120–900 seconds
- Sources: GitHub API, npm registry and Snapshot Hub
- Deployment transaction hash: `0x7cdd075f71821d9f60e3a264d9f4310b3b197a1fda299f10c608374f0c9ba8cd`
- Explorer deploy result: `FINALIZED`, GenVM `SUCCESS`, consensus `Accepted`
- Explorer source header/version visually matches the locked ImpactRail source;
  exact byte-for-byte source parity still requires an exported source readback
- Live grant lifecycle: not yet run

This V1 deployment is superseded before any live grant was funded. Preparing a
real npm resource exposed that the version endpoint did not supply the release
time map and V1 did not bind npm `gitHead` to the sealed target commit. V2 now
fetches the package packument, selects the sealed version, checks its release
time and requires `gitHead == target_commit`. V2 passes all local gates and its
active deployment is recorded below.

## Active V2 deployment

- Address: `0x39e5Dc71024E358474EFC78fBC880213Ef1d1caf`
- Deploy transaction: `0x60c4befc6a73537648ccf24d69b04d59bccc8bfe9af059a02c103e46a87f201e`
- Constructor inputs: none
- Explorer: `FINALIZED`, GenVM `SUCCESS`, consensus `Accepted`
- `get_config().version`: `IMPACT_RAIL_V2`
- Public accounting readback: all ledgers and balance are zero before funding
- Live funded grant lifecycle: not yet run

## Deployment parity checks

1. Run the lint command and record the exact source SHA-256.
2. Preserve the V2 deployment transaction hash from Studio Explorer.
3. Reconfirm the deployed source and constructor against the source manifest.
4. The local frontend now targets the exact deployed address and has rebuilt.

## After deployment

Register a real beneficiary, fund one small grant with a real canonical
GitHub/npm/Snapshot fixture, evaluate from a participant wallet, and read back
the grant, attempts, accounting and recipient balances. Repeat one failed or
expired case. `ACCEPTED` or `FINALIZED` alone is not a pass; execution result,
consensus and state/balance readback are all required. This file must be updated
with live hashes only when those checks actually run.
