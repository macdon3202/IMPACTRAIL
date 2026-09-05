# V4 live status — failed evaluation safely recovered

The deployment at `0x377A27B57116eB21b2781879348676E4d71170F1`
returned `INSUFFICIENT_EVIDENCE` twice with `SOURCE_HTTP_403`. The original
contract did not identify which of its five requests failed. It did not release
funds on either attempt.

After deadline, transaction
`0x7ed0d881b71502ef04323db9affa48b37f238d6ef1dcbc546efb2e3be5b2435b`
made the sponsor refund claimable. Transaction
`0xf42fbbd8fe525148498f6d5edcc2594049edc25a95b68f8a15551d49c4d907ce`
returned it. Authoritative readback showed `PAID`, contract balance `0`, locked
`0`, both claimable totals `0`, and sponsor balance delta exactly
`1000000000000` wei.

The patched source adds GitHub's recommended `User-Agent`, media type and API
version headers, performs requests sequentially, and records a bounded source-
specific failure code. A diagnostic contract then fetched the repository,
commit, comparison, raw artifact and release from GenVM; all returned HTTP 200.
The observed response sizes were respectively 5165, 4361, 11881, 699 and 2406
bytes. Since the same repository endpoint also returned 200 without headers
during the later probe, the historical 403 cannot honestly be attributed solely
to a missing header; a transient or rate-limit response remains possible.

This proves current acquisition reachability and safe recovery, not a successful
patched payout lifecycle. The patched main source still requires a new deployment
and a fresh funded lifecycle.
