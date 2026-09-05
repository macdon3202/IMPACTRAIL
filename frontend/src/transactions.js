export const VERSION = 'IMPACT_RAIL_V5';
export const NETWORK = 'studionet';
export const JOURNAL = 'impactrail_transactions_v1';
export const serialize = (value) => JSON.stringify(value, (_, v) => typeof v === 'bigint' ? v.toString() : v);
export const sameAddress = (a, b) => Boolean(a && b && a.toLowerCase() === b.toLowerCase());
export const normalizeHash = (tx) => {
  const hash = typeof tx === 'string' ? tx : tx?.txId || tx?.hash;
  if (!/^0x[0-9a-fA-F]{64}$/.test(hash || '')) throw new Error('Wallet response is ambiguous. Inspect wallet activity; do not resend.');
  return hash;
};
export const receiptState = (info) => {
  const status = String(info?.statusName ?? info?.status_name ?? info?.status ?? '').toUpperCase();
  const execution = String(info?.txExecutionResultName ?? info?.tx_execution_result_name ?? info?.execution_result ?? info?.resultName ?? '').toUpperCase();
  const receipts = (info?.consensus_data?.leader_receipt ?? []).filter(r => r.result?.payload !== 'idle');
  const failed = ['FAILED', 'REJECTED', 'CANCELLED', 'CANCELED', 'UNDETERMINED'].includes(status) || ['ERROR', 'FAILED', 'REVERT'].includes(execution) || receipts.some(r => r.execution_result === 'ERROR');
  const executionVerified = execution === 'SUCCESS' || (receipts.length > 0 && receipts.every(r => r.execution_result === 'SUCCESS'));
  return {status, execution, failed, accepted: !failed && executionVerified && ['ACCEPTED', 'FINALIZED'].includes(status)};
};
export const loadJournal = (storage) => {
  const raw = storage.getItem(JOURNAL); if (!raw) return [];
  const list = JSON.parse(raw); if (!Array.isArray(list)) throw new Error('Transaction journal is invalid; preserve it before clearing browser data.');
  return list;
};
export const saveJournal = (storage, records) => storage.setItem(JOURNAL, serialize(records));
