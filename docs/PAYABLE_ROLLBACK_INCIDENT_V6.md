# V6 payable rollback incident

Checked on 2026-09-09 against
`0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a`.

Three live `create_grant` calls attached 1,000,000,000,000 wei each and used
invalid sealed terms. All three transactions finalized with validator agreement
and the expected execution errors:

- commit threshold 251: `INVALID_COVERAGE_WINDOW`;
- minimum downloads 0: `UNSUPPORTED_DOWNLOAD_THRESHOLD`;
- inverted adoption dates: `INVALID_ADOPTION_PERIOD`.

The contract's grant accounting did not change, but authoritative balance
readback increased from zero to 3,000,000,000,000 wei and the sponsor balance
decreased by the same amount. V6 has no surplus-recovery method, so those funds
must not be described as refunded or recoverable. The exact hashes and before /
after readbacks are in `evidence-package/v6-threshold-negative.json`.

This disproves the V6 assumption that a rollback of a payable call restores
attached value on Studionet. V6 is superseded and must not receive new funds.

V7 removes value from term creation. Validated terms first create a non-payable
`DRAFT`; a separate minimal payable method funds it. Any non-zero invalid
funding is accepted into a per-sender refund ledger and can be withdrawn through
`withdraw_unallocated`, rather than relying on rollback semantics.
