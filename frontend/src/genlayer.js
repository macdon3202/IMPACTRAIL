import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import { normalizeHash, receiptState, VERSION, sameAddress } from './transactions';

export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS || '';
export const makeReadClient = () => createClient({chain: studionet});
export const readContract = (functionName, args = []) => {
  if (!/^0x[0-9a-fA-F]{40}$/.test(CONTRACT_ADDRESS)) throw new Error('VITE_CONTRACT_ADDRESS is not configured yet.');
  return makeReadClient().readContract({address: CONTRACT_ADDRESS, functionName, args});
};
export async function connectWallet() {
  if (!window.ethereum) throw new Error('Install a browser wallet such as MetaMask.');
  const [account] = await window.ethereum.request({method: 'eth_requestAccounts'});
  const client = createClient({chain: studionet, account, provider: window.ethereum});
  await client.connect('studionet');
  return {client, account};
}
export async function writeContract(wallet, functionName, args = [], value = 0n) {
  try {
    const [active] = await window.ethereum.request({method: 'eth_accounts'});
    if (!sameAddress(active, wallet.account)) throw new Error('Wallet changed. Reconnect.');
    const chain = await window.ethereum.request({method: 'eth_chainId'});
    if (BigInt(chain) !== BigInt(studionet.id)) throw new Error('Switch wallet to Studionet.');
    const cfg = await readContract('get_config');
    if (cfg.version !== VERSION) throw new Error('This is not an ImpactRail deployment. No transaction sent.');
  } catch (error) { error.notSent = true; throw error; }
  return normalizeHash(await wallet.client.writeContract({address: CONTRACT_ADDRESS, functionName, args, value}));
}
export async function waitTransaction(client, hash, onUpdate = () => {}) {
  for (let i = 0; i < 40; i += 1) {
    const info = await client.getTransaction({hash}); const state = receiptState(info); onUpdate(state);
    if (state.failed) { const e = new Error('Transaction execution failed. Consensus acceptance is not success.'); e.confirmedFailure = true; throw e; }
    if (state.accepted) return info;
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  throw new Error('Still pending or unknown. Use Reconcile; do not submit again.');
}
