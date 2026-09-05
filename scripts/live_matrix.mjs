import {createClient,createAccount} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {parse} from '../../TreasuryPayoutVerifier/scripts/testnet/node_modules/dotenv/lib/main.js';
const address='0xb61678034F70E5aC688851c3Ab547f4E428E781e';
const A='0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43', B='0xc67532aeF9D2879cBA9375a02E6217A3524657B8';
const amount=1000000000000n;
const path=new URL('./.state/live-matrix.json',import.meta.url);
const log=existsSync(path)?JSON.parse(readFileSync(path)):{address,actions:{},cases:{}};
const encode=v=>JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2);
const save=()=>writeFileSync(path,encode(log));
const client=createClient({chain:studionet});
const delay=()=>new Promise(r=>setTimeout(r,2500));
async function read(method,args=[]){await delay();return client.readContract({address,functionName:method,args});}
function signer(who){const env=parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env',import.meta.url),'utf8'));const raw=env['SERVICE_LEDGER_KEY_'+who].replace(/^<|>$/g,'').trim();const account=createAccount(raw.startsWith('0x')?raw:'0x'+raw);if(account.address.toLowerCase()!==(who==='A'?A:B).toLowerCase())throw Error('WRONG_WALLET');return createClient({chain:studionet,account});}
async function tx(key,who,method,args=[],value=0n,expectedError=null){
 let a=log.actions[key];
 if(!a){a=log.actions[key]={phase:'SENDING',method,args,value,expectedError,at:new Date().toISOString()};save();a.hash=await signer(who).writeContract({address,functionName:method,args,value});a.phase='SUBMITTED';save();}
 if(!a.hash)throw Error('AMBIGUOUS_NO_RESUBMIT '+key);
 for(let i=0;i<50;i++){
  await new Promise(r=>setTimeout(r,5000));const receipt=await client.getTransaction({hash:a.hash});a.receipt=receipt;save();
  if(!['ACCEPTED','FINALIZED'].includes(receipt.statusName))continue;
  const leaders=(receipt.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');
  const errors=leaders.filter(x=>x.execution_result==='ERROR');
  a.passed=expectedError?errors.length>0&&JSON.stringify(errors).includes(expectedError):leaders.length>0&&leaders.every(x=>x.execution_result==='SUCCESS');
  a.phase='OBSERVED';save();console.log(encode({key,hash:a.hash,passed:a.passed,status:receipt.statusName,error:expectedError}));
  if(!a.passed)throw Error('UNEXPECTED_EXECUTION '+key);return;
 }throw Error('PENDING_NO_RESUBMIT '+key);
}
async function main(){
 const action=process.argv[2],name=process.argv[3];
 if(action==='negative'){
  const before=await read('get_accounting');
  await tx('double-withdraw','B','withdraw',[0n],0n,'NOT_CLAIMABLE');
  await tx('terminal-retry','A','retry_grant',[0n],0n,'GRANT_TERMINAL');
  await tx('missing-grant','A','evaluate_grant',[999n],0n,'GRANT_NOT_FOUND');
  log.negative={before,after:await read('get_accounting')};log.negative.passed=encode(log.negative.before)===encode(log.negative.after);save();console.log(encode(log.negative));return;
 }
 if(action==='create'){
  if(!['reject','partial','expire'].includes(name))throw Error('INVALID_CASE');
  if(!log.cases[name]){const acc=await read('get_account',[A,0n]);log.cases[name]={id:Number(acc.count)};save();}
  const digest=name==='reject'?'0'.repeat(64):'095b20d4e6274cdc27459e30ac1af114aadf86ee0ff0d2639f3cce1b5e4b01b0';
  const milestone=name==='partial'?'Publish the commit-pinned ImpactRail report AND supply an independent external security audit with a named auditor and documented findings.':'Verify the published ImpactRail artifact ('+name+' test).';
  await tx(name+'-create','A','create_grant',[B,amount,'macdon3202','IMPACTRAIL','ef0a23e4470dfaef0c38cfface89fcabf8225cd8','536091b33cb4c4a9cd45fb224277aa3c451889b3','evidence/impact-report.md',digest,'impactrail-v4-fixture',milestone,1n,1n,1788430000n,name==='expire'?120n:300n,5000n],amount);
  log.cases[name].grant=await read('get_grant',[BigInt(log.cases[name].id)]);save();console.log(encode(log.cases[name]));return;
 }
 const c=log.cases[name];if(!c)throw Error('CASE_MISSING');const id=BigInt(c.id);
 if(action==='evaluate')await tx(name+'-evaluate','A','evaluate_grant',[id]);
 if(action==='expire')await tx(name+'-expire','A','expire_grant',[id]);
 if(action==='withdraw'){
  const g=await read('get_grant',[id]);
  c.balancesBefore??={A:await client.getBalance({address:A}),B:await client.getBalance({address:B})};save();
  if(BigInt(g.beneficiary_due)>0n)await tx(name+'-withdraw-B','B','withdraw',[id]);
  if(BigInt(g.sponsor_due)>0n)await tx(name+'-withdraw-A','A','withdraw',[id]);
 }
 c.grant=await read('get_grant',[id]);c.accounting=await read('get_accounting');
 c.balancesAfter={A:await client.getBalance({address:A}),B:await client.getBalance({address:B})};save();console.log(encode(c));
}
main().catch(e=>{console.error(e.shortMessage??e.message);process.exitCode=1});
