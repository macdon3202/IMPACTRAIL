# ImpactRail V9 source-probe gate

The probe is diagnostic only. It has no custody, payout, mutable source, or
eligibility decision. It independently tests the four canonical endpoints that
V8 grouped under `CANONICAL_VERIFICATION_UNAVAILABLE`.

V9 must not be implemented or deployed until every retained endpoint produces:

- HTTP 200 from a finalized Studionet call;
- `usable: true`;
- the same byte length and SHA-256 on two separate calls;
- successful GenVM execution and accepted validator consensus.

An unavailable, oversized, or nondeterministic source must be removed or
replaced. Probe success establishes transport availability only; it does not
prove the eventual V9 business logic or payout lifecycle.

## Live result — PASS

Probe `0xCb798Ac755495c0d372e6E71106eb6903D8aa5d5` tested all four sources
twice. Every call had successful GenVM execution, accepted consensus, HTTP 200,
`usable: true`, and identical byte length/SHA-256 between rounds. Therefore V9
will stage package, run, jobs and workflow verification across separate
transactions instead of issuing all canonical requests inside one execution.
