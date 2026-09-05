import test from 'node:test';
import assert from 'node:assert/strict';
import {receiptState,saveJournal,loadJournal,normalizeHash} from './src/transactions.js';
test('finalized contract execution error must not appear accepted',()=>{
 const result=receiptState({statusName:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'ERROR',result:{status:'contract_error',payload:'FAIL'}}]}});
 assert.equal(result.failed,true);assert.equal(result.accepted,false);
});
test('missing execution evidence must not appear accepted',()=>assert.equal(receiptState({statusName:'FINALIZED'}).accepted,false));
test('successful execution with cancelled idle validator is accepted',()=>assert.equal(receiptState({statusName:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'SUCCESS'},{execution_result:'ERROR',result:{payload:'idle'}}]}}).accepted,true));
test('pending journal survives reload',()=>{
 const data=new Map();const storage={getItem:k=>data.get(k),setItem:(k,v)=>data.set(k,v)};
 const rows=[{localId:'pending',phase:'SUBMITTED',hash:'0x'+'a'.repeat(64),value:1n}];
 saveJournal(storage,rows);assert.equal(loadJournal(storage)[0].hash,rows[0].hash);
});
test('ambiguous wallet response is rejected',()=>assert.throws(()=>normalizeHash({}),/ambiguous/));
