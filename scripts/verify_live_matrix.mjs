import {createClient} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync} from 'node:fs';
const address='0xb61678034F70E5aC688851c3Ab547f4E428E781e';
const A='0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43',B='0xc67532aeF9D2879cBA9375a02E6217A3524657B8';
const journal=JSON.parse(readFileSync(new URL('./.state/live-matrix.json',import.meta.url)));
const lifecycle=JSON.parse(readFileSync(new URL('./.state/studionet-'+address.toLowerCase()+'.json',import.meta.url)));
const client=createClient({chain:studionet});
const accounting=await client.readContract({address,functionName:'get_accounting',args:[]});
const balances={A:await client.getBalance({address:A}),B:await client.getBalance({address:B}),contract:await client.getBalance({address})};
const initial=lifecycle.preflight.snapshot.balances;
const deltas={A:BigInt(balances.A)-BigInt(initial.A),B:BigInt(balances.B)-BigInt(initial.B)};
const cases={};for(const [name,item] of Object.entries(journal.cases))cases[name]={id:item.id,state:(await client.readContract({address,functionName:'get_grant',args:[BigInt(item.id)]})).state};
const transactions=[];for(const [name,item] of Object.entries(journal.actions)){const r=await client.getTransaction({hash:item.hash});const leaders=(r.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');transactions.push({name,hash:item.hash,status:r.statusName,execution:leaders.map(x=>x.execution_result),passed:item.passed===true&&leaders.length>0&&leaders.every(x=>x.execution_result==='SUCCESS'||item.expectedError)});}
const passed=Object.values(cases).every(x=>x.state==='PAID')&&transactions.every(x=>x.passed)&&BigInt(balances.contract)===0n&&accounting.locked==='0'&&accounting.beneficiary_claimable==='0'&&accounting.sponsor_claimable==='0'&&deltas.A===-1500000000000n&&deltas.B===1500000000000n;
const result={checkedAt:new Date().toISOString(),address,passed,cases,accounting,initialBalances:initial,finalBalances:balances,balanceDeltas:deltas,transactions,interpretation:'Beneficiary received FULL 1000000000000 + PARTIAL 500000000000; rejected and expired deposits returned to sponsor.'};
const text=JSON.stringify(result,(_,v)=>typeof v==='bigint'?String(v):v,2);writeFileSync(new URL('../evidence-package/live-adversarial-matrix.json',import.meta.url),text);console.log(text);if(!passed)process.exitCode=1;
