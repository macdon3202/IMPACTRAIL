import {createClient} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync} from 'node:fs';
const address='0x6027309e88CB1f51f891Eea85436ad80347592DB';
const A='0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43',B='0xc67532aeF9D2879cBA9375a02E6217A3524657B8';
const file=new URL('./.state/studionet-'+address.toLowerCase()+'.json',import.meta.url);
const journal=JSON.parse(readFileSync(file));const client=createClient({chain:studionet});
const transactions=[];
for(const [name,item] of Object.entries(journal.actions)){
 const receipt=await client.getTransaction({hash:item.hash});
 const leaders=(receipt.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');
 const votes=Object.values(receipt.consensus_data?.votes??{});
 transactions.push({name,hash:item.hash,status:receipt.statusName,execution:leaders.map(x=>x.execution_result),agree:votes.filter(x=>x==='agree').length,total:votes.length,
  passed:['ACCEPTED','FINALIZED'].includes(receipt.statusName)&&leaders.length>0&&leaders.every(x=>x.execution_result==='SUCCESS')&&votes.filter(x=>x==='agree').length>votes.length/2});
}
const grant=await client.readContract({address,functionName:'get_grant',args:[0n]});
const accounting=await client.readContract({address,functionName:'get_accounting',args:[]});
const balances={A:await client.getBalance({address:A}),B:await client.getBalance({address:B}),contract:await client.getBalance({address})};
const initial=journal.preflight.snapshot.balances;const deltas={A:BigInt(balances.A)-BigInt(initial.A),B:BigInt(balances.B)-BigInt(initial.B)};
const passed=journal.preflight.deployedSha256===journal.preflight.localSha256&&transactions.length===5&&transactions.every(x=>x.passed)&&grant.state==='PAID'&&grant.verdict==='PARTIAL'&&
 accounting.locked==='0'&&accounting.beneficiary_claimable==='0'&&accounting.sponsor_claimable==='0'&&BigInt(balances.contract)===0n&&deltas.A===-500000000000n&&deltas.B===500000000000n;
const result={checkedAt:new Date().toISOString(),address,passed,sourceSha256:journal.preflight.deployedSha256,transactions,grant,accounting,initialBalances:initial,finalBalances:balances,balanceDeltas:deltas,
 limitation:'One V5 PARTIAL lifecycle using maintainer-controlled GitHub fixture evidence; this is not independent proof of real-world impact.'};
const text=JSON.stringify(result,(_,v)=>typeof v==='bigint'?String(v):v,2);writeFileSync(new URL('../evidence-package/v5-live-lifecycle.json',import.meta.url),text);console.log(text);if(!passed)process.exitCode=1;
