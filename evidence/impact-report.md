# ImpactRail delivery artifact

This repository delivers ImpactRail V3: a public-goods grant rail whose
validators independently verify a GitHub repository, an exact commit range, a
raw evidence artifact pinned to the target commit, and a final Snapshot vote.

The contract computes the artifact SHA-256 itself, fails closed on unavailable
or inconsistent evidence, and derives payout accounting deterministically.

Release note: the canonical artifact is now independently retrieved from its
commit-pinned raw GitHub URL during the V3 verification path.
