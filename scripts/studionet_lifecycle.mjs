import {createClient,createAccount} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync,existsSync,mkdirSync} from 'node:fs';
import {parse} from '../../TreasuryPayoutVerifier/scripts/testnet/node_modules/dotenv/lib/main.js';
import {createHash} from 'node:crypto';

const address=process.env.IMPACTRAIL_ADDRESS??'0x377A27B57116eB21b2781879348676E4d71170F1';
const A='0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43',B='0xc67532aeF9D2879cBA9375a02E6217A3524657B8';
const base='ef0a23e4470dfaef0c38cfface89fcabf8225cd8',target='536091b33cb4c4a9cd45fb224277aa3c451889b3';
const artifactPath='evidence/impact-report.md',artifactSha256='095b20d4e6274cdc27459e30ac1af114aadf86ee0ff0d2639f3cce1b5e4b01b0',releaseTag='impactrail-v4-fixture';
const amount=1000000000000n,coverageStart=1788430000n;
if(!/^0x[0-9a-fA-F]{40}$/.test(address))throw Error('INVALID_CONTRACT_ADDRESS');
const stateDir=new URL('./.state/',import.meta.url);mkdirSync(stateDir,{recursive:true});const file=new URL(address==='0x377A27B57116eB21b2781879348676E4d71170F1'?'./.state/studionet-v4.json':'./.state/studionet-'+address.toLowerCase()+'.json',import.meta.url);
const encode=x=>JSON.stringify(x,(_,v)=>typeof v==='bigint'?String(v):v,2);let log=existsSync(file)?JSON.parse(readFileSync(file)):{address,releaseTag,actions:{}};const save=()=>writeFileSync(file,encode(log));
const reader=createClient({chain:studionet});const read=(functionName,args=[])=>reader.readContract({address,functionName,args});
function signer(who){const env=parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env',import.meta.url),'utf8'));const raw=env['SERVICE_LEDGER_KEY_'+who].replace(/^<|>$/g,'').trim();const account=createAccount(raw.startsWith('0x')?raw:'0x'+raw);const expected=who==='A'?A:B;if(account.address.toLowerCase()!==expected.toLowerCase())throw Error('WRONG_WALLET');return createClient({chain:studionet,account});}
async function receipt(hash){for(let i=0;i<50;i++){const tx=await reader.getTransaction({hash});const status=String(tx.statusName??'').toUpperCase();if(['FAILED','REJECTED','CANCELLED','UNDETERMINED'].includes(status))throw Error('TX_FAILED '+hash+' '+status);if(['ACCEPTED','FINALIZED'].includes(status)){
 const leaders=(tx.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');
 if(!leaders.length||leaders.some(x=>x.execution_result!=='SUCCESS'))throw Error('EXECUTION_NOT_SUCCESS '+hash);
 const votes=Object.values(tx.consensus_data?.votes??{});if(votes.filter(x=>x==='agree').length<=votes.length/2)throw Error('CONSENSUS_NOT_VERIFIED '+hash);
 return tx;
 }await new Promise(r=>setTimeout(r,3000));}throw Error('TX_PENDING_NO_RESUBMIT '+hash);}
async function snapshot(){const cfg=await read('get_config'),accounting=await read('get_accounting'),accountA=await read('get_account',[A,0n]),accountB=await read('get_account',[B,0n]);let grant=null;if(Number(accountA.count)>0)grant=await read('get_grant',[0n]);return {cfg,accounting,accountA,accountB,grant,balances:{A:await reader.getBalance({address:A}),B:await reader.getBalance({address:B}),contract:await reader.getBalance({address})}};}
async function send(name,who,functionName,args=[],value=0n){if(log.actions[name]?.hash){log.actions[name].receipt=await receipt(log.actions[name].hash);log.actions[name].after=await snapshot();log.actions[name].phase='EXECUTED';save();return;}if(log.actions[name])throw Error('AMBIGUOUS_SEND_NO_RESUBMIT '+name);const before=await snapshot();log.actions[name]={functionName,args,value,before,phase:'SENDING',startedAt:new Date().toISOString()};save();const hash=await signer(who).writeContract({address,functionName,args,value});log.actions[name].hash=hash;log.actions[name].phase='SUBMITTED';save();log.actions[name].receipt=await receipt(hash);log.actions[name].after=await snapshot();log.actions[name].phase='EXECUTED';save();console.log(encode({name,hash,state:log.actions[name].after.grant?.state,accounting:log.actions[name].after.accounting}));}
async function main(){const action=process.argv[2]??'read';if(action==='read'){log.latest=await snapshot();save();console.log(encode(log.latest));return;}
if(action==='preflight'){
 const code=await reader.getContractCode(address);
 const bytes=typeof code==='string'&&code.startsWith('0x')?Buffer.from(code.slice(2),'hex'):Buffer.from(code);
 const sha=x=>createHash('sha256').update(x).digest('hex');
 log.preflight={at:new Date().toISOString(),deployedSha256:sha(bytes),localSha256:sha(readFileSync(new URL('../contracts/impact_rail.py',import.meta.url))),snapshot:await snapshot()};save();
 console.log(encode(log.preflight));if(log.preflight.deployedSha256!==log.preflight.localSha256)throw Error('SOURCE_MISMATCH');return;
}
if(['register','fund','evaluate','withdraw'].includes(action)){
 if(!log.preflight||log.preflight.deployedSha256!==log.preflight.localSha256)throw Error('PREFLIGHT_REQUIRED');
 if(action==='register')await send('register','B','register_wallet');
 if(action==='fund')await send('fund','A','create_grant',[B,amount,'macdon3202','IMPACTRAIL',base,target,artifactPath,artifactSha256,releaseTag,'Deliver ImpactRail V4 with deterministic custody and commit-pinned public evidence.',1n,1n,coverageStart,900n,5000n],amount);
 if(action==='evaluate')await send('evaluate','A','evaluate_grant',[0n]);
 if(action==='withdraw'){
  const current=await snapshot();
  if(BigInt(current.grant?.beneficiary_due??0)>0n)await send('withdraw-beneficiary','B','withdraw',[0n]);
  const afterBeneficiary=await snapshot();
  if(BigInt(afterBeneficiary.grant?.sponsor_due??0)>0n)await send('withdraw-sponsor','A','withdraw',[0n]);
 }return;
}
if(action==='recover'){
 let current=await snapshot();
 if(['FUNDED','INSUFFICIENT_EVIDENCE'].includes(current.grant?.state)){
  if(Math.floor(Date.now()/1000)<Number(current.grant.deadline))throw Error('WINDOW_OPEN_UNTIL '+current.grant.deadline);
  await send('expire','A','expire_grant',[0n]);current=await snapshot();
 }
 if(current.grant?.state==='EXPIRED_REFUND_CLAIMABLE')await send('refund','A','withdraw',[0n]);
 const final=await snapshot();log.recoveryReadback=final;save();
 const before=log.actions.refund?.before;
 const balanceDelta=before?BigInt(final.balances.A)-BigInt(before.balances.A):null;
 const passed=final.grant?.state==='PAID'&&final.accounting.locked==='0'&&final.accounting.sponsor_claimable==='0'&&BigInt(final.balances.contract)===0n&&balanceDelta===amount;
 console.log(encode({recoveryPassed:passed,balanceDelta,final}));if(!passed)throw Error('RECOVERY_NOT_YET_VERIFIED');return;
}
if(action==='run'){
 const initial=await snapshot();if(initial.cfg.version!=='IMPACT_RAIL_V5')throw Error('WRONG_CONTRACT');
 await send('register','B','register_wallet');
 await send('fund','A','create_grant',[B,amount,'macdon3202','IMPACTRAIL',base,target,artifactPath,artifactSha256,releaseTag,'Deliver ImpactRail V4 with deterministic custody and commit-pinned public evidence.',1n,1n,coverageStart,900n,5000n],amount);
 await send('evaluate','A','evaluate_grant',[0n]);let evaluated=await snapshot();if(evaluated.grant?.state==='INSUFFICIENT_EVIDENCE'){await send('retry','A','retry_grant',[0n]);evaluated=await snapshot();}if(evaluated.grant?.state!=='VERIFIED_CLAIMABLE')throw Error('NOT_VERIFIED '+encode(evaluated.grant));
 await send('withdraw','B','withdraw',[0n]);const final=await snapshot();if(final.grant?.state!=='PAID'||final.accounting.locked!=='0'||final.accounting.beneficiary_claimable!=='0'||final.accounting.sponsor_claimable!=='0')throw Error('FINAL_STATE_MISMATCH');log.final=final;save();console.log(encode({complete:true,final}));return;}throw Error('UNKNOWN_ACTION');}
main().catch(e=>{console.error(String(e.shortMessage??e.message).slice(0,2000));process.exitCode=1});
