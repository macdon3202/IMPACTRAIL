# ImpactRail V9 — Complete Production Lifecycle Evidence

This consolidated release artifact records the deployed contract, canonical inputs, every live Studionet transaction, authoritative state and accounting readbacks, adversarial coverage, production frontend parity, and disclosed limitations.

## Release identity

| Field | Verified value |
|---|---|
| Network | GenLayer Studionet |
| Active contract | [`0x8bc22E809b85EF6568DD1083108F495f33d276FA`](https://explorer-studio.genlayer.com/address/0x8bc22E809b85EF6568DD1083108F495f33d276FA) |
| Version readback | `IMPACT_RAIL_V9` |
| Constructor | No inputs |
| Reviewed source | [`contracts/impact_rail_v9.py`](../contracts/impact_rail_v9.py) |
| Contract source SHA-256 | `f4bfcdd00666d44293ad6ab03a0c52f9a9b525ec114b161ca43f4f073df26fa2` |
| Verification commit | [`19e1c7ee715f37cc1d7a23ba8df7695e9938de29`](https://github.com/macdon3202/IMPACTRAIL/commit/19e1c7ee715f37cc1d7a23ba8df7695e9938de29) |
| Canonical workflow run | [`34336729341`](https://github.com/macdon3202/IMPACTRAIL/actions/runs/34336729341) — `success` |
| Production frontend | https://impactrail.pages.dev |
| Repository | https://github.com/macdon3202/IMPACTRAIL |

Live `get_config()` returned profile `testnet`, maximum verifiable commits `250`, and verification policy `four staged objective gates then final GitHub semantic evaluation`.

## Proof boundary and architecture

ImpactRail is a public-goods grant rail. A sponsor seals a beneficiary, payout amount, repository, commit range, artifact digest, npm package/version, GitHub Actions run, workflow path and workflow digest before custody. Unsupported bounds are rejected in the non-payable draft step; funds enter only through a separate `fund_grant` call.

Four validator-recomputed objective gates must independently pass before semantic delivery evaluation:

1. npm Registry package identity and exact `gitHead` binding.
2. GitHub Actions run identity, repository, commit, workflow and successful conclusion.
3. GitHub Actions jobs and required completed steps.
4. Raw workflow bytes fetched from GitHub at the exact verification commit and matched to the sealed SHA-256.

Project-authored narrative cannot unlock a payout by itself. Final AI output is restricted to delivery and materiality observations; contract logic deterministically derives payout and accounting state.

## Sealed live fixture

| Field | Value |
|---|---|
| Grant ID | `0` |
| Sponsor | `0xfed97e2ae1a8c1983b7ca206b3545e6a2c685e43` |
| Beneficiary | `0xc67532aef9d2879cba9375a02e6217a3524657b8` |
| Amount | `1,000,000,000,000 wei` |
| Repository | `macdon3202/IMPACTRAIL` |
| Base commit | `4a3fd38f127ef54ccba668eafda02732d838fe4c` |
| Target commit | `c526aa3faaa8299f571b8598f56423e77084178b` |
| Artifact | `evidence/v6-npm-impact.md` |
| Artifact SHA-256 | `117f86c86f786b1ac0f3de11efcb4181b00f9f21b5b868a1aa94e279fc82d612` |
| npm package | `@macdon3202/impactrail-canonical@1.0.0` |
| Verification commit | `19e1c7ee715f37cc1d7a23ba8df7695e9938de29` |
| Workflow | `.github/workflows/verify-impactrail-v9.yml` |
| Workflow SHA-256 | `baccc20398a5161a1097c278473d914037f89b5ce230a06d472c4f0ecfe859ca` |
| Workflow run | `34336729341` |
| Partial payout | `5,000 bps` — 50% |

## Complete live transaction sequence

Every row was executed against the active V9 contract. A transition is verified only when execution, consensus where applicable, and subsequent contract readback agree.

| # | Action | Transaction | Verified result |
|---:|---|---|---|
| 1 | Register participant wallet | [`0x494347c1229fabfa3ce58dbe744e8ea558ef553a6c330a6b2552a375bc555b10`](https://explorer-studio.genlayer.com/tx/0x494347c1229fabfa3ce58dbe744e8ea558ef553a6c330a6b2552a375bc555b10) | `SUCCESS`; `REGISTERED` |
| 2 | Create non-payable grant draft | [`0x727183874bde653236897611465710c0dd7d3dd7c421f29c8e310a7d251d29c4`](https://explorer-studio.genlayer.com/tx/0x727183874bde653236897611465710c0dd7d3dd7c421f29c8e310a7d251d29c4) | `SUCCESS`; grant #0 `DRAFT`; balance and ledgers remain zero |
| 3 | Fund exact sealed amount | [`0x019ffc28cf7f78d57ec8f8f79564f3924b0746e14cf89b3ce56f04771ca30473`](https://explorer-studio.genlayer.com/tx/0x019ffc28cf7f78d57ec8f8f79564f3924b0746e14cf89b3ce56f04771ca30473) | `SUCCESS`; grant `FUNDED`; `1,000,000,000,000 wei` locked |
| 4 | Verify npm package binding | [`0x500e51e023eaeac05a2b7adb53001c22a704d83b5682ce52f1bd03e6dd4bbed7`](https://explorer-studio.genlayer.com/tx/0x500e51e023eaeac05a2b7adb53001c22a704d83b5682ce52f1bd03e6dd4bbed7) | `SUCCESS`; gate mask `1/15` |
| 5 | Verify GitHub Actions run | [`0xdf8a91d5aa542b33a4716057d12840960727c55191facff49531f96d813a11df`](https://explorer-studio.genlayer.com/tx/0xdf8a91d5aa542b33a4716057d12840960727c55191facff49531f96d813a11df) | `SUCCESS`; gate mask `3/15` |
| 6 | Verify completed Actions jobs | [`0x9c7e4affdfa6d8860692d08479a2e30cde6db18ff7695216ec8e136945014a20`](https://explorer-studio.genlayer.com/tx/0x9c7e4affdfa6d8860692d08479a2e30cde6db18ff7695216ec8e136945014a20) | `SUCCESS`; gate mask `7/15` |
| 7 | Verify commit-pinned workflow bytes | [`0xb6992672ec43dc388439db06c315cf3ec1ff3e0c76a322b1c19b7cd8321bdc09`](https://explorer-studio.genlayer.com/tx/0xb6992672ec43dc388439db06c315cf3ec1ff3e0c76a322b1c19b7cd8321bdc09) | `SUCCESS`; all objective gates `15/15` |
| 8 | Evaluate delivery | [`0xe32e7656d7e07c39996dc1a263e35bc42ba119593bd02f1b33804551110aa858`](https://explorer-studio.genlayer.com/tx/0xe32e7656d7e07c39996dc1a263e35bc42ba119593bd02f1b33804551110aa858) | `SUCCESS`, consensus `Accepted`; `PARTIAL_CLAIMABLE` |
| 9 | Beneficiary withdrawal | [`0x62da32c22d4e0f3b5c281904c6d79b51569281fd13d05651cc685861e63b057f`](https://explorer-studio.genlayer.com/tx/0x62da32c22d4e0f3b5c281904c6d79b51569281fd13d05651cc685861e63b057f) | `SUCCESS`; beneficiary received `500,000,000,000 wei` |
| 10 | Sponsor withdrawal | [`0x8c3e53f03401a466b089c7f15088124774405730b5bffc8a30c987e19ff96e7c`](https://explorer-studio.genlayer.com/tx/0x8c3e53f03401a466b089c7f15088124774405730b5bffc8a30c987e19ff96e7c) | `SUCCESS`; sponsor received `500,000,000,000 wei`; grant `PAID` |

## Objective evidence readback

The finalized grant recorded gate mask `15`, proving all four staged gates completed before evaluation.

| Gate | Stored digest |
|---|---|
| Immutable terms | `680d84372df4db5d8de1c0eb844761ce89b58dc014f74233c104416554fe7170` |
| npm package response | `3083ba5c2ac30ad4f4b0558e3d32241edfff7e064903a278eef74b85541ed656` |
| GitHub Actions run | `b3c695c4c2c92c5180ac8b13ddae772cab75c744978c5cc104f5c3575073f3b8` |
| GitHub Actions jobs | `a834bdce1da5423a3f6e4e8be2f87f0322e5f4809296dbca2c7a534560f3b257` |
| Commit-pinned workflow | `baccc20398a5161a1097c278473d914037f89b5ce230a06d472c4f0ecfe859ca` |

The associated public GitHub Actions run concluded successfully: https://github.com/macdon3202/IMPACTRAIL/actions/runs/34336729341.

## Settlement and accounting conservation

The semantic observation was `PARTIAL` with substantive materiality. Contract logic applied the sealed 50% rule:

- beneficiary claim: `500,000,000,000 wei`
- sponsor refund claim: `500,000,000,000 wei`
- total outbound requested: `1,000,000,000,000 wei`
- final grant state after both withdrawals: `PAID`

Final authoritative readback:

| Accounting field | Final value |
|---|---:|
| Contract balance | `0` |
| Total deposited | `1,000,000,000,000` |
| Locked | `0` |
| Outbound requested | `1,000,000,000,000` |
| Beneficiary claimable | `0` |
| Sponsor claimable | `0` |
| Unallocated claimable | `0` |

The funded amount was neither stranded nor duplicated, and all claim ledgers cleared after withdrawal.

## Failure and adversarial coverage

V9 was tested locally against the production contract source for unsupported commit thresholds before custody; invalid npm and evidence-window bounds; invalid funding recovery; incomplete gates; source transport failures; npm identity and `gitHead` mismatch; GitHub run identity, commit, workflow or conclusion mismatch; failed/incomplete jobs; workflow digest mismatch; duplicate gate replay; malformed model schema; prompt injection; unauthorized calls; terminal replay; duplicate withdrawal; partial settlement; withdrawals; and accounting conservation.

V9-specific Direct Mode tests passed `9/9`; the full contract regression passed `136/136`. These controlled tests support the live lifecycle but are not represented as extra live transactions.

## Independent canonical-source probe

Before custody testing, diagnostic deployment [`0xCb798Ac755495c0d372e6E71106eb6903D8aa5d5`](https://explorer-studio.genlayer.com/address/0xCb798Ac755495c0d372e6E71106eb6903D8aa5d5) independently fetched the npm metadata, GitHub Actions run, Actions jobs and exact-commit workflow twice. Each source produced stable bytes and SHA-256 across both rounds. See [`v9-source-probe-live.json`](../evidence-package/v9-source-probe-live.json).

## Source, deployment and frontend parity

- Contract readback reports `IMPACT_RAIL_V9`.
- Reviewed source SHA-256 and canonical verification identity are locked in [`source-manifest-v9.json`](./source-manifest-v9.json).
- Production frontend embeds V9 and the exact active contract address.
- Historical V1–V8 deployments are superseded and are not presented as current production contracts.

| Frontend check | Result |
|---|---|
| Production URL | https://impactrail.pages.dev |
| Immutable deployment | https://a62e649f.impactrail.pages.dev |
| HTTP readback | `200` |
| Bundle version | `IMPACT_RAIL_V9` |
| Bundle contract | `0x8bc22E809b85EF6568DD1083108F495f33d276FA` |
| Transaction journal tests | `6/6 PASS` |
| Production build | `PASS` |

The frontend separates draft creation from funding, refuses writes on version mismatch, persists pending transactions across reload, never automatically resubmits, checks execution and consensus, then verifies expected state through authoritative readback.

## Reproduction commands

```powershell
genvm-lint check contracts/impact_rail_v9.py
pytest -q tests/test_impact_rail_v9.py
pytest -q
cd frontend
node --test transactions.test.mjs
npm run build
```

## Evidence index

- Live lifecycle and transaction hashes: [`evidence-package/v9-live-lifecycle.json`](../evidence-package/v9-live-lifecycle.json)
- Canonical-source probe: [`evidence-package/v9-source-probe-live.json`](../evidence-package/v9-source-probe-live.json)
- Source/deployment/frontend manifest: [`docs/source-manifest-v9.json`](./source-manifest-v9.json)
- V9 specification: [`docs/SPECIFICATION_V9.md`](./SPECIFICATION_V9.md)
- V9 adversarial audit: [`docs/ADVERSARIAL_AUDIT_V9.md`](./ADVERSARIAL_AUDIT_V9.md)
- Production contract source: [`contracts/impact_rail_v9.py`](../contracts/impact_rail_v9.py)

## Honest limitations and non-claims

- The live result was `PARTIAL`, not `FULL`. The contract correctly applied the sealed 50% split; no full-payout claim is made for this grant.
- The public test repository, package and workflow are controlled by the project maintainer. Canonical sources are independently fetched and cryptographically bound, but this does not establish third-party adoption or independent economic impact.
- The lifecycle harness used two test wallets. A separate browser-wallet automation recording is not claimed.
- A finalized receipt alone was not treated as proof. Every claimed transition includes execution/consensus evaluation and authoritative contract readback.
- Historical failed and superseded deployments remain documented and are not counted as V9 passes.

## Release conclusion

ImpactRail V9 completed the full production lifecycle on Studionet: participant registration, non-payable draft validation, funding, four independent canonical gates, validator-based evaluation, deterministic partial settlement, withdrawals by both parties, and final zero-balance accounting readback. Failure behavior was exercised against the production source, and the production frontend was verified against the same deployed V9 contract.
