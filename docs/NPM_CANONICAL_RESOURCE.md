# ImpactRail V6 canonical npm resource

Published on 2026-09-07:

- Package: `@macdon3202/impactrail-canonical@1.0.0`
- npm page: https://www.npmjs.com/package/@macdon3202/impactrail-canonical/v/1.0.0
- Registry endpoint: https://registry.npmjs.org/%40macdon3202%2Fimpactrail-canonical/1.0.0
- GitHub repository: `macdon3202/IMPACTRAIL`
- Registry `gitHead`: `c526aa3faaa8299f571b8598f56423e77084178b`
- Registry integrity: `sha512-eymho80TY3kwsEL8lJeFkX5HQG8wdwoiepJFxBoJskq7+U6IxlTFBLxIHfbHCPPdIa9Iamo6PT2xQCmgnaGW1g==`
- GitHub release: https://github.com/macdon3202/IMPACTRAIL/releases/tag/impactrail-v6-npm-1.0.0
- Artifact: `evidence/v6-npm-impact.md`
- Artifact SHA-256: `117f86c86f786b1ac0f3de11efcb4181b00f9f21b5b868a1aa94e279fc82d612`

The Registry version endpoint returned HTTP 200 and binds the exact package
name/version, repository, and `gitHead`. A clean temporary consumer installation
also succeeded. The GitHub Release API returned HTTP 200 and binds the same
target commit, artifact, beneficiary, and test amount.

## Time-dependent adoption status

The npm Downloads API currently returns package-not-found for the 2026-09-07
daily period because the package and its first real installation were created
on that date and daily statistics have not yet closed. Therefore no live
positive payout is claimed yet.

Once the public endpoint reports an integer count of at least one, the sealed
grant inputs can use:

```text
npm_package: @macdon3202/impactrail-canonical
npm_version: 1.0.0
period_start: 2026-09-07
period_end: 2026-09-07
minimum_downloads: 1
target_commit: c526aa3faaa8299f571b8598f56423e77084178b
artifact_path: evidence/v6-npm-impact.md
artifact_sha256: 117f86c86f786b1ac0f3de11efcb4181b00f9f21b5b868a1aa94e279fc82d612
release_tag: impactrail-v6-npm-1.0.0
```

The contract also requires the period to be fully historical. The positive
lifecycle must not be submitted until both the time check and Downloads API
readback pass.
