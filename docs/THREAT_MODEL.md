# Threat model and adversarial matrix

| Threat | Contract response | Direct check |
|---|---|---|
| Self-authored or substituted evidence | URLs are constructed from sealed identifiers; repository, exact commit, raw artifact path and computed SHA-256 are checked | mismatched repository / commit / artifact digest |
| Release markers edited or mismatched | Exact release tag, target, publication time and sealed marker set are required | beneficiary / amount / commit / digest mismatch |
| Commit range too small | `ahead_by` and distinct contributors must meet sealed thresholds | below-threshold compare response |
| Prompt injection or model overreach | bounded untrusted context; exact two-field schema; deterministic payout | injection text and extra output field |
| HTTP/IPFS/JSON failure | source size/status, duplicate-key rejection, independent validator and retryable verdict | 404 and malformed JSON |
| Replay/stale evaluation | immutable terms digest, evidence identity key, attempt counter and per-sender cooldown | duplicate evidence and stale calls |
| Unauthorized settlement/claim | participant and direct wallet checks; per-party due ledgers | third-party evaluate/withdraw |
| Deadline race | no evaluation after deadline; expiry only after deadline | early expiry and expiry refund |
| Double claim/accounting drift | due zeroed before transfer request; reserve ledgers updated once | second withdrawal and final zero ledger |

The matrix is intentionally layered: static/lint, Direct Mode entrypoints,
negative and adversarial combinations, then live Studionet lifecycle and
authoritative balance/source readback after deployment.
