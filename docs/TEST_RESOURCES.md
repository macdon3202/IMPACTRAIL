# Canonical test resources

Direct Mode uses deterministic synthetic responses with the same shapes as the
official sources. They are not evidence of a live repository or vote.

- GitHub: `https://api.github.com/repos/{owner}/{repo}`, `/commits/{sha}` and
  `/compare/{base}...{target}`.
- npm: `https://registry.npmjs.org/{package}/{version}`.
- Snapshot: `https://testnet.hub.snapshot.org/graphql` for the testnet profile;
  production uses the public Hub. The contract embeds the proposal query and
  validates the returned space, markers, vote finality and score policy.

No applicant-supplied JSON, IPFS pin, image, or arbitrary URL is trusted. A live
release should record exact response URLs, fetch timestamps, SHA-256 digests,
the contract address and the post-finalization readback in a separate evidence
file; a failed attempt must remain recorded as failed.
