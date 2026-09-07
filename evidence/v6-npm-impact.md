# ImpactRail V6 npm adoption artifact

ImpactRail V6 adds an independently attributable payout gate. A positive grant
decision requires validators to retrieve official npm Registry metadata that
binds an exact package version to this repository and target commit, then
retrieve an exact historical download period from the official npm Downloads
API. GitHub commits, project artifacts, and release text remain provenance but
cannot unlock funds without the independent adoption gate.

The contract rejects unverifiable commit thresholds before custody, caps retry
attempts, fails closed on missing or inconsistent sources, and keeps expiry
recovery available. Direct Mode regression and a funded Studionet fail-closed
refund lifecycle are recorded separately; this artifact does not imply a
positive live payout before the Registry and Downloads API confirm it.
