import {createClient} from '../frontend/node_modules/genlayer-js/dist/index.js';
import {studionet} from '../frontend/node_modules/genlayer-js/dist/chains/index.js';
import {readFileSync,writeFileSync} from 'node:fs';
const address='0x6027309e88CB1f51f891Eea85436ad80347592DB';
const source=new URL('./.state/live-matrix-'+address.toLowerCase()+'.json',import.meta.url);
const journal=JSON.parse(readFileSync(source));const client=createClient({chain:studionet});const transactions=[];
for(const [name,item] of Object.entries(journal.actions)){
 const receipt=await client.getTransaction({hash:item.hash});
 const leaders=(receipt.consensus_data?.leader_receipt??[]).filter(x=>x.result?.payload!=='idle');
 const text=JSON.stringify(leaders);const passed=receipt.statusName==='FINALIZED'&&leaders.length>0&&leaders.every(x=>x.execution_result==='ERROR')&&text.includes(item.expectedError);
 transactions.push({name,hash:item.hash,status:receipt.statusName,execution:leaders.map(x=>x.execution_result),expectedError:item.expectedError,passed});
}
const accounting=await client.readContract({address,functionName:'get_accounting',args:[]});
const same=JSON.stringify(journal.negative.before)===JSON.stringify(journal.negative.after)&&JSON.stringify(journal.negative.after)===JSON.stringify(accounting);
const result={checkedAt:new Date().toISOString(),address,passed:transactions.length===3&&transactions.every(x=>x.passed)&&same,transactions,accountingBefore:journal.negative.before,accountingAfter:accounting};
const text=JSON.stringify(result,null,2);writeFileSync(new URL('../evidence-package/v5-negative-calls.json',import.meta.url),text);console.log(text);if(!result.passed)process.exitCode=1;
