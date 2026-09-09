import {createClient,createAccount} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync,existsSync,mkdirSync} from 'node:fs';
import {parse} from '../../TreasuryPayoutVerifier/scripts/testnet/node_modules/dotenv/lib/main.js';

const stateDir=new URL('./.state/',import.meta.url);mkdirSync(stateDir,{recursive:true});
const stateFile=new URL('./.state/canonical-source-probe-v9.json',import.meta.url);
let journal=existsSync(stateFile)?JSON.parse(readFileSync(stateFile)):{purpose:'Diagnostic only; no custody, payout, or eligibility decision',sourceSha256:'61ef066715434ae1c30a95efc2d2d69f61ac58f3c21344eddbc27fff89f417f6',address:'0xCb798Ac755495c0d372e6E71106eb6903D8aa5d5',deploymentSource:'user-deployed',calls:{}};
const save=()=>writeFileSync(stateFile,JSON.stringify(journal,null,2));
const reader=createClient({chain:studionet});
function signer(){const env=parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env',import.meta.url),'utf8'));const raw=env.SERVICE_LEDGER_KEY_A.replace(/^<|>$/g,'').trim();const account=createAccount(raw.startsWith('0x')?raw:'0x'+raw);if(account.address.toLowerCase()!=='0xfed97e2ae1a8c1983b7ca206b3545e6a2c685e43')throw Error('WRONG_SIGNER');return createClient({chain:studionet,account});}
async function receipt(hash){for(let i=0;i<80;i++){const tx=await reader.getTransaction({hash});const status=String(tx.statusName??'').toUpperCase();if(['FAILED','REJECTED','CANCELLED','UNDETERMINED'].includes(status))throw Error('TX_FAILED '+status);if(['ACCEPTED','FINALIZED'].includes(status)){const leaders=(tx.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');if(!leaders.length||leaders.some(x=>x.execution_result!=='SUCCESS'))throw Error('GENVM_ERROR '+hash);return {status,result:leaders[0].result?.payload};}await new Promise(r=>setTimeout(r,3000));}throw Error('PENDING_NO_RESUBMIT');}
const action=process.argv[2]??'status';
if(action==='deploy'){
  if(journal.deploy?.hash)throw Error('DEPLOY_ALREADY_HAS_HASH');
  journal.deploy={phase:'SENDING',startedAt:new Date().toISOString()};save();
  const hash=await signer().deployContract({code:new Uint8Array(readFileSync(new URL('../contracts/canonical_source_probe_v9.py',import.meta.url))),args:[]});
  journal.deploy={...journal.deploy,phase:'SUBMITTED',hash};save();console.log(hash);
}else if(action==='status'){
  if(!journal.deploy?.hash)throw Error('NO_DEPLOY_HASH');const tx=await reader.getTransaction({hash:journal.deploy.hash});journal.deploy.receipt={status:tx.statusName,address:tx.to_address};journal.address=tx.to_address;save();console.log(JSON.stringify(journal.deploy.receipt));
}else if(action==='call'){
  const index=Number(process.argv[3]),round=Number(process.argv[4]);if(!journal.address)throw Error('NO_ADDRESS');if(!Number.isInteger(index)||index<0||index>3||![1,2].includes(round))throw Error('INVALID_CALL');const key=`${index}:${round}`;if(journal.calls[key])throw Error('CALL_ALREADY_JOURNALED');journal.calls[key]={phase:'SENDING',startedAt:new Date().toISOString()};save();const hash=await signer().writeContract({address:journal.address,functionName:'probe',args:[BigInt(index)]});journal.calls[key]={...journal.calls[key],phase:'SUBMITTED',hash};save();console.log(hash);
}else if(action==='reconcile'){
  for(const [key,entry] of Object.entries(journal.calls)){if(!entry.hash||entry.phase==='VERIFIED')continue;entry.receipt=await receipt(entry.hash);entry.phase='VERIFIED';save();console.log(JSON.stringify({key,hash:entry.hash,...entry.receipt}));}
}else if(action==='report'){
  const results={};for(const [key,entry] of Object.entries(journal.calls)){if(entry.phase!=='VERIFIED')throw Error('INCOMPLETE '+key);const wrapped=entry.receipt.result;const readable=typeof wrapped==='string'?wrapped:wrapped?.readable;results[key]=JSON.parse(JSON.parse(readable));}for(let i=0;i<4;i++){const a=results[`${i}:1`],b=results[`${i}:2`];if(!a.usable||!b.usable||a.status!==200||b.status!==200||a.bytes!==b.bytes||a.sha256!==b.sha256)throw Error('SOURCE_GATE_FAILED '+i);}console.log(JSON.stringify({pass:true,address:journal.address,results},null,2));
}else throw Error('UNKNOWN_ACTION');
