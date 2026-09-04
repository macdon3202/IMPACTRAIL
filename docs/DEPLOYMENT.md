# Contract deployment handoff

The following V1 contract was deployed on Studionet but is superseded and must
not be used for a funded lifecycle:

```text
0x2c1b0842da58927d1653614DB29D36053e63E487
```

The superseded V1 deployment used a profile argument. The current V2 source has
no constructor inputs: deploy it with an empty constructor form. Its Studionet
evidence window is fixed to 120–900 seconds.

That profile intentionally limits the evidence window to 120–900 seconds for a
short Studionet demonstration. A production profile requires a 1–180 day
window. There is no configuration transaction after construction.

The address is set in the local frontend and the production build passes.
Deployment transaction:

```text
0x7cdd075f71821d9f60e3a264d9f4310b3b197a1fda299f10c608374f0c9ba8cd
```

Studio Explorer shows `FINALIZED`, GenVM `SUCCESS` and consensus `Accepted`.
Those receipt signals do not erase the npm binding defect found before live
funding. Deploy the current `IMPACT_RAIL_V2` source with no arguments, then update
the frontend address.
The frontend will refuse writes to an address whose `get_config().version` is
not `IMPACT_RAIL_V1`.

Live follow-up is still required: register a beneficiary, fund a small grant,
evaluate it, inspect the consensus/execution result, read the grant and
accounting state, and check recipient balance after withdrawal. Do not mark a
grant passed from a receipt status alone.
