import {createClient} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {receiptState} from '../frontend/src/transactions.js';

// Read-only reconciliation: never signs or resubmits a transaction.
const file = new URL('./.state/studionet-v6.json', import.meta.url);
const log = JSON.parse(readFileSync(file));
const address = '0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a';
assert.equal(log.address.toLowerCase(), address.toLowerCase());
const client = createClient({chain: studionet});
const read = (functionName, args = []) => client.readContract({address, functionName, args});
const encode = value => JSON.stringify(value, (_, v) => typeof v === 'bigint' ? String(v) : v, 2);
for (const name of ['register', 'fund', 'evaluate', 'expire', 'refund']) {
  const action = log.actions[name];
  assert.match(action.hash, /^0x[0-9a-fA-F]{64}$/);
  const receipt = await client.getTransaction({hash: action.hash});
  assert.equal(receiptState(receipt).accepted, true, name + ': execution not verified');
  const votes = Object.values(receipt.consensus_data?.votes ?? {});
  assert.ok(votes.filter(v => v === 'agree').length > votes.length / 2, name + ': consensus');
  action.receipt = receipt;
  action.phase = 'VERIFIED';
}
const config = await read('get_config');
const accounting = await read('get_accounting');
const grant = await read('get_grant', [0n]);
const balances = {A: await client.getBalance({address: grant.sponsor}), B: await client.getBalance({address: grant.beneficiary}), contract: await client.getBalance({address})};
assert.equal(config.version, 'IMPACT_RAIL_V6');
assert.equal(grant.state, 'PAID');
assert.equal(grant.verdict, 'INSUFFICIENT_EVIDENCE');
for (const key of ['locked', 'sponsor_claimable', 'beneficiary_claimable', 'balance']) assert.equal(BigInt(accounting[key]), 0n);
assert.equal(balances.contract, 0n);
assert.equal(balances.A - BigInt(log.actions.refund.before.balances.A), BigInt(grant.amount_wei));
assert.equal(balances.B, BigInt(log.actions.refund.before.balances.B));
const code = await client.getContractCode(address);
const bytes = typeof code === 'string' && code.startsWith('0x') ? Buffer.from(code.slice(2), 'hex') : Buffer.from(code);
const sha = value => createHash('sha256').update(value).digest('hex');
assert.equal(sha(bytes), sha(readFileSync(new URL('../contracts/impact_rail_v6.py', import.meta.url))));
log.final = {config, accounting, grant, balances};
log.reconciledAt = new Date().toISOString();
log.sourceSha256 = sha(bytes);
log.scope = 'Live insufficient-evidence, expiry and sponsor refund only. No live positive payout or browser wallet journey claimed.';
writeFileSync(file, encode(log));
writeFileSync(new URL('../evidence-package/v6-live-lifecycle.json', import.meta.url), encode(log));
console.log(encode({checkedAt: log.reconciledAt, sourceSha256: log.sourceSha256, transactions: Object.fromEntries(Object.entries(log.actions).map(([name, a]) => [name, {hash: a.hash, status: a.receipt.statusName}])), final: log.final}));
