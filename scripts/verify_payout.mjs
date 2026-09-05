import {createClient} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync,appendFileSync} from 'node:fs';
const address='0xb61678034F70E5aC688851c3Ab547f4E428E781e';
const journal=JSON.parse(readFileSync(new URL('./.state/studionet-'+address.toLowerCase()+'.json',import.meta.url)));
const client=createClient({chain:studionet});
const grant=await client.readContract({address,functionName:'get_grant',args:[0n]});
const accounting=await client.readContract({address,functionName:'get_accounting',args:[]});
const beneficiaryBalance=await client.getBalance({address:grant.beneficiary});
const contractBalance=await client.getBalance({address});
const txs=[];
for(const [name,action] of Object.entries(journal.actions)){
 const tx=await client.getTransaction({hash:action.hash});
 const leaders=(tx.consensus_data?.leader_receipt??[]).filter(r=>r.result?.payload!=='idle');
 const votes=Object.values(tx.consensus_data?.votes??{});
 txs.push({name,hash:action.hash,status:tx.statusName,execution:leaders.map(r=>r.execution_result),agree:votes.filter(v=>v==='agree').length,total:votes.length,
  passed:['ACCEPTED','FINALIZED'].includes(tx.statusName)&&leaders.length>0&&leaders.every(r=>r.execution_result==='SUCCESS')&&votes.filter(v=>v==='agree').length>votes.length/2});
}
const delta=BigInt(beneficiaryBalance)-BigInt(journal.actions.withdraw.before.balances.B);
const passed=txs.every(t=>t.passed)&&grant.state==='PAID'&&delta===1000000000000n&&BigInt(contractBalance)===0n&&['locked','beneficiary_claimable','sponsor_claimable'].every(k=>accounting[k]==='0');
const evidence={checkedAt:new Date().toISOString(),address,sourceParity:journal.preflight.deployedSha256===journal.preflight.localSha256,sourceSha256:journal.preflight.deployedSha256,passed,transactions:txs,grant,accounting,beneficiaryBalanceBefore:journal.actions.withdraw.before.balances.B,beneficiaryBalanceAfter:beneficiaryBalance,beneficiaryDelta:delta,contractBalance,limitation:'One funded FULL payout lifecycle. No live partial-payout or adversarial matrix is claimed.'};
const text=JSON.stringify(evidence,(_,v)=>typeof v==='bigint'?String(v):v,2);
appendFileSync(new URL('../evidence-package/patched-v4-readbacks.jsonl',import.meta.url),JSON.stringify(evidence,(_,v)=>typeof v==='bigint'?String(v):v)+'\n');
writeFileSync(new URL('../evidence-package/patched-v4-payout.json',import.meta.url),text);console.log(text);
if(!passed)process.exitCode=1;
