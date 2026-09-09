import {createClient, createAccount} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync, writeFileSync, existsSync} from 'node:fs';
import {parse} from '../../TreasuryPayoutVerifier/scripts/testnet/node_modules/dotenv/lib/main.js';
import assert from 'node:assert/strict';

const address = '0xbA2DdBE10249E870EC2CF87A1b8C4e41553A995a';
const sponsor = '0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43';
const beneficiary = '0xc67532aeF9D2879cBA9375a02E6217A3524657B8';
const amount = 1000000000000n;
const stateFile = new URL('./.state/v6-threshold-negative.json', import.meta.url);
const outputFile = new URL('../evidence-package/v6-threshold-negative.json', import.meta.url);
const encode = value => JSON.stringify(value, (_, item) => typeof item === 'bigint' ? String(item) : item, 2);
const client = createClient({chain: studionet});

const env = parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env', import.meta.url), 'utf8'));
const rawKey = env.SERVICE_LEDGER_KEY_A.replace(/^<|>$/g, '').trim();
const account = createAccount(rawKey.startsWith('0x') ? rawKey : `0x${rawKey}`);
assert.equal(account.address.toLowerCase(), sponsor.toLowerCase(), 'WRONG_TEST_WALLET');
const signer = createClient({chain: studionet, account});

const journal = existsSync(stateFile)
  ? JSON.parse(readFileSync(stateFile, 'utf8'))
  : {address, createdAt: new Date().toISOString(), actions: {}};
const save = () => writeFileSync(stateFile, encode(journal));
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const valid = [
  beneficiary,
  amount,
  'macdon3202',
  'IMPACTRAIL',
  '4a3fd38f127ef54ccba668eafda02732d838fe4c',
  'c526aa3faaa8299f571b8598f56423e77084178b',
  'evidence/v6-npm-impact.md',
  '117f86c86f786b1ac0f3de11efcb4181b00f9f21b5b868a1aa94e279fc82d612',
  'impactrail-v6-npm-1.0.0',
  'Verify independently attributable ImpactRail delivery and objective npm adoption.',
  1n,
  1n,
  1788764800n,
  900n,
  5000n,
  '@macdon3202/impactrail-canonical',
  '1.0.0',
  '2026-09-07',
  '2026-09-07',
  1n,
];

const cases = [
  {name: 'commit-threshold-over-verifier-bound', index: 10, value: 251n, expectedError: 'INVALID_COVERAGE_WINDOW'},
  {name: 'zero-download-threshold', index: 19, value: 0n, expectedError: 'UNSUPPORTED_DOWNLOAD_THRESHOLD'},
  {name: 'inverted-adoption-period', index: 17, value: '2026-09-08', also: [18, '2026-09-07'], expectedError: 'INVALID_ADOPTION_PERIOD'},
];

async function receiptFor(hash) {
  for (let attempt = 0; attempt < 70; attempt += 1) {
    const receipt = await client.getTransaction({hash});
    if (receipt.statusName === 'FINALIZED') return receipt;
    await sleep(3000);
  }
  throw new Error(`PENDING_NO_RESUBMIT ${hash}`);
}

async function submit(testCase) {
  let action = journal.actions[testCase.name];
  if (!action) {
    const args = [...valid];
    args[testCase.index] = testCase.value;
    if (testCase.also) args[testCase.also[0]] = testCase.also[1];
    action = journal.actions[testCase.name] = {
      phase: 'SENDING',
      expectedError: testCase.expectedError,
      submittedAt: new Date().toISOString(),
    };
    save();
    action.hash = await signer.writeContract({address, functionName: 'create_grant', args, value: amount});
    action.phase = 'SUBMITTED';
    save();
  }
  if (!action.hash) throw new Error(`AMBIGUOUS_NO_RESUBMIT ${testCase.name}`);
  const receipt = await receiptFor(action.hash);
  const leaders = (receipt.consensus_data?.leader_receipt ?? []).filter(item => item.result?.payload !== 'idle');
  const text = JSON.stringify(leaders);
  action.receipt = receipt;
  action.phase = 'VERIFIED';
  action.passed = receipt.statusName === 'FINALIZED' && leaders.length > 0 &&
    leaders.every(item => item.execution_result === 'ERROR') && text.includes(testCase.expectedError);
  save();
  assert.equal(action.passed, true, `UNEXPECTED_EXECUTION ${testCase.name}`);
}

const snapshot = async () => ({
  accounting: await client.readContract({address, functionName: 'get_accounting', args: []}),
  contractBalance: await client.getBalance({address}),
  sponsorBalance: await client.getBalance({address: sponsor}),
  sponsorAccount: await client.readContract({address, functionName: 'get_account', args: [sponsor, 0n]}),
});

journal.before ??= await snapshot();
save();
for (const testCase of cases) await submit(testCase);
journal.after = await snapshot();
journal.checkedAt = new Date().toISOString();

const stable = value => encode(value);
const stateUnchanged = stable(journal.before) === stable(journal.after);
const transactions = cases.map(testCase => {
  const action = journal.actions[testCase.name];
  return {
    name: testCase.name,
    hash: action.hash,
    status: action.receipt.statusName,
    expectedError: testCase.expectedError,
    execution: (action.receipt.consensus_data?.leader_receipt ?? [])
      .filter(item => item.result?.payload !== 'idle')
      .map(item => item.execution_result),
    passed: action.passed,
  };
});
const result = {
  checkedAt: journal.checkedAt,
  address,
  scope: 'Three live V6 invalid-threshold create_grant calls; all attached value must roll back.',
  passed: stateUnchanged && transactions.every(item => item.passed),
  stateUnchanged,
  transactions,
  before: journal.before,
  after: journal.after,
};
writeFileSync(outputFile, encode(result));
console.log(encode(result));
assert.equal(result.passed, true, 'LIVE_THRESHOLD_NEGATIVE_FAILED');
