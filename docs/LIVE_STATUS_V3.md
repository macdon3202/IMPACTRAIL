# V3 live status — incomplete

Deployment: `0x5f6EcEE07360624Daa2De584e4936B1c7623d2c2`.
Config readback returned `IMPACT_RAIL_V3`; accounting and balance were zero.
Source byte parity verified on 2026-09-04 at 11:34 UTC: deployed and local
SHA-256 both equal `8508ca703b3ac65db240d2f819de94d5e966a93601036add0602cb889c650cc9`.

Read-only GitHub preflight returned HTTP 200 for all four URLs. Raw artifact
SHA-256 matched the sealed value. However the selected target commit response
was 68,056 bytes and compare response was 75,518 bytes, exceeding V3's 48,000
byte per-response limit. This fixture cannot pass the deployed acquisition gate.
Select a smaller substantive commit range and authorize its exact markers in a
new proposal before funding; do not silently relax the gate or alter old evidence.

Snapshot proposal: `0xc9f9f1f89e482148f75d58308104381645bf088fedfbad18bde0956f554da4ca`.
Last observed: closed, scores [1, 0, 0], scores_state pending. This does not
prove permanent failure. No grant funding or payout is claimed.

A local V4 experiment counted votes against current members. It was withdrawn:
current membership is mutable, vote pagination was incomplete, and one-vote
counting does not reproduce arbitrary Snapshot voting strategies. V3 final-score
verification remains intact. Do not deploy the withdrawn experiment.

The earlier space lookup accidentally included a trailing space in its ID.
Its null result was not evidence that the existing space had disappeared.
A space-settings update was subsequently accepted by the Hub; this was not
necessary to establish that the original space existed. Further space mutations
are disabled in the fixture script. Signed attempts remain locally journalled.

Before funding: verify deployed source bytes, all canonical response URLs and
artifact hash, final Snapshot scores and exact markers. Harden the runner's
ambiguous-send guard, then verify execution, consensus, state and actual balances
for registration, funding, evaluation and withdrawal. Local tests alone are not
a live lifecycle PASS.
