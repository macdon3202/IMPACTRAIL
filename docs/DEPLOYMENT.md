# Contract deployment handoff

The following V1 contract was deployed on Studionet but is superseded and must
not be used for a funded lifecycle:

```text
0x2c1b0842da58927d1653614DB29D36053e63E487
```

The superseded V1 deployment used a profile argument. The current V2 source has
no constructor inputs: deploy it with an empty constructor form. Its Studionet
evidence window is fixed to 120–900 seconds.

The fixed configuration limits the evidence window to 120–900 seconds for a
short Studionet demonstration. There is no configuration transaction after
construction.

The address is set in the local frontend and the production build passes.
Deployment transaction:

```text
0x7cdd075f71821d9f60e3a264d9f4310b3b197a1fda299f10c608374f0c9ba8cd
```

Studio Explorer shows `FINALIZED`, GenVM `SUCCESS` and consensus `Accepted`.
Those receipt signals do not erase the npm binding defect found before live
funding. It is retained only as honest deployment history.

## Active V2

```text
Address: 0x39e5Dc71024E358474EFC78fBC880213Ef1d1caf
Deploy tx: 0x60c4befc6a73537648ccf24d69b04d59bccc8bfe9af059a02c103e46a87f201e
Constructor: no inputs
```

The local frontend targets this V2 address. Explorer and public method readback
both confirm `IMPACT_RAIL_V2`; accounting is zero before live funding.
The frontend will refuse writes to an address whose `get_config().version` is
not `IMPACT_RAIL_V2`.

Live follow-up is still required: register a beneficiary, fund a small grant,
evaluate it, inspect the consensus/execution result, read the grant and
accounting state, and check recipient balance after withdrawal. Do not mark a
grant passed from a receipt status alone.
