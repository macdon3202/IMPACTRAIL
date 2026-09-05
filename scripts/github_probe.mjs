import {createClient,createAccount} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {parse} from '../../TreasuryPayoutVerifier/scripts/testnet/node_modules/dotenv/lib/main.js';
const path=new URL('./.state/github-probe-write.json',import.meta.url);
const log=existsSync(path)?JSON.parse(readFileSync(path)):{purpose:'Diagnostic only; no funds or eligibility',createdAt:new Date().toISOString()};
const save=()=>writeFileSync(path,JSON.stringify(log,(_,v)=>typeof v==='bigint'?String(v):v,2));
const client=createClient({chain:studionet});
const action=process.argv[2]??'status';
function signer(){
 const env=parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env',import.meta.url),'utf8'));
 const raw=env.SERVICE_LEDGER_KEY_A.replace(/^<|>$/g,'').trim();
 const account=createAccount(raw.startsWith('0x')?raw:'0x'+raw);
 if(account.address.toLowerCase()!=='0xfed97e2ae1a8c1983b7ca206b3545e6a2c685e43')throw Error('WRONG_SIGNER');
 return createClient({chain:studionet,account});
}
if(action==='call'){
 const address=process.argv[3],index=Number(process.argv[4]),withHeaders=process.argv[5]==='true';
 const key=index+':'+withHeaders;log.calls??={};if(log.calls[key])throw Error('ALREADY_ATTEMPTED_NO_RESUBMIT');
 log.calls[key]={phase:'SENDING'};save();
 const hash=await signer().writeContract({address,functionName:'probe',args:[BigInt(index),withHeaders]});
 log.calls[key]={phase:'SUBMITTED',hash};save();console.log(hash);
}else if(action==='call-status'){
 for(const [key,call] of Object.entries(log.calls??{})){
  if(!call.hash)continue;call.receipt=await client.getTransaction({hash:call.hash});save();
  console.log(JSON.stringify({key,hash:call.hash,status:call.receipt.statusName,leaders:call.receipt.consensus_data?.leader_receipt?.map(x=>({execution:x.execution_result,result:x.result,errors:x.genvm_result}))}));
 }
}else
if(action==='deploy'){
 if(log.phase)throw Error('ALREADY_ATTEMPTED_NO_RESUBMIT');
 const env=parse(readFileSync(new URL('../../secrets/genlayer-test-wallets.env',import.meta.url),'utf8'));
 const raw=env.SERVICE_LEDGER_KEY_A.replace(/^<|>$/g,'').trim();
 const account=createAccount(raw.startsWith('0x')?raw:'0x'+raw);
 if(account.address.toLowerCase()!=='0xfed97e2ae1a8c1983b7ca206b3545e6a2c685e43')throw Error('WRONG_SIGNER');
 log.phase='SENDING';save();
 log.hash=await createClient({chain:studionet,account}).deployContract({code:new Uint8Array(readFileSync(new URL('../contracts/github_fetch_probe.py',import.meta.url))),args:[]});
 log.phase='SUBMITTED';save();console.log(log.hash);
}else if(action==='status'){
 if(!log.hash)throw Error('NO_HASH');
 log.receipt=await client.getTransaction({hash:log.hash});save();
 console.log(JSON.stringify({hash:log.hash,address:log.receipt.to_address,status:log.receipt.statusName,leaders:log.receipt.consensus_data?.leader_receipt?.map(x=>({execution:x.execution_result,result:x.result}))}));
}else if(action==='read'){
 const address=process.argv[3],index=Number(process.argv[4]),withHeaders=process.argv[5]==='true';
 const result=await client.readContract({address,functionName:'probe',args:[BigInt(index),withHeaders]});
 log.reads??=[];log.reads.push({address,index,withHeaders,result,time:new Date().toISOString()});save();console.log(result);
}else throw Error('UNKNOWN_ACTION');
