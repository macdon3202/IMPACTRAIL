import hashlib,json
from pathlib import Path
import pytest

CONTRACT=Path(__file__).parents[1]/"contracts"/"impact_rail_v9.py"
A="0x"+"11"*20;B="0x"+"22"*20;BASE="a"*40;TARGET="b"*40;VERIFY="c"*40;AMOUNT=1000;START=1788652800
ARTIFACT=b"substantive canonical implementation";ARTIFACT_SHA=hashlib.sha256(ARTIFACT).hexdigest();WORKFLOW=b"verified workflow";WORKFLOW_SHA=hashlib.sha256(WORKFLOW).hexdigest();PATH=".github/workflows/verify-impactrail-v8.yml";RUN=12345

def deploy(vm,direct_deploy):
    vm.warp("2026-09-07T12:00:00+00:00");c=direct_deploy(CONTRACT,sdk_version="v0.2.16");from genlayer.py.types import Address;old=vm.sender;vm.sender=Address(B);c.register_wallet();vm.sender=old;return c
def args(commits=1,workflow_sha=WORKFLOW_SHA):return [B,AMOUNT,"impactrail","demo",BASE,TARGET,"evidence/report.md",ARTIFACT_SHA,"v1","Deliver verified infrastructure",commits,1,START,120,5000,"impact-package","1.0.0",VERIFY,PATH,workflow_sha,RUN]
def fund(c,vm):
    gid=c.create_grant(*args());vm.value=AMOUNT;vm.deal(vm._contract_address,vm._balances.get(vm._contract_address,0)+AMOUNT)
    try:assert c.fund_grant(gid)=="FUNDED"
    finally:vm.value=0
    return gid
def gate_payloads(run_ok=True):
    metadata={"name":"impact-package","version":"1.0.0","repository":{"url":"https://github.com/impactrail/demo.git"},"gitHead":TARGET}
    run={"id":RUN,"head_sha":VERIFY,"head_repository":{"full_name":"impactrail/demo"},"head_branch":"main","event":"push","status":"completed","conclusion":"success" if run_ok else "failure","path":PATH}
    names={"Checkout sealed source","Verify npm registry binding","Install published package","Validate V9 contract","Run V9 contract tests","Test frontend journal","Build production frontend"}
    jobs={"total_count":1,"jobs":[{"head_sha":VERIFY,"conclusion":"success","steps":[{"name":n,"conclusion":"success"} for n in names]}]}
    return metadata,run,jobs
def mock_gate(vm,index,run_ok=True,status=200):
    values=gate_payloads(run_ok);patterns=[r"registry\.npmjs\.org",r"actions/runs/12345$",r"actions/runs/12345/jobs",r"raw\.githubusercontent\.com/.*/"+VERIFY+r"/\.github/workflows"]
    bodies=[json.dumps(values[0]),json.dumps(values[1]),json.dumps(values[2]),WORKFLOW]
    vm.mock_web(patterns[index],{"status":status,"body":bodies[index]})
def mock_final(vm,fit=True):
    repo={"visibility":"public","full_name":"impactrail/demo"};commit={"sha":TARGET,"commit":{"message":"deliver feature"}};comparison={"status":"ahead","ahead_by":1,"total_commits":1,"commits":[{"sha":TARGET,"author":{"login":"builder"}}]};release={"tag_name":"v1","target_commitish":TARGET,"draft":False,"prerelease":False}
    for p,b in [(r"repos/impactrail/demo$",repo),(r"commits/",commit),(r"compare/",comparison),(r"raw\.githubusercontent\.com/.*/"+TARGET,ARTIFACT),(r"releases/tags/",release)]:vm.mock_web(p,{"status":200,"body":b if isinstance(b,bytes) else json.dumps(b)})
    vm.mock_llm("IMPACT_RAIL_V9",{"delivery":"FULL","materiality":"SUBSTANTIVE"} if fit else {"delivery":"NONE","materiality":"COSMETIC"})
def gates(c,vm):
    for i,name in enumerate(("verify_package","verify_run","verify_jobs","verify_workflow")):mock_gate(vm,i);assert getattr(c,name)(0).endswith("_VERIFIED")

def test_happy_staged_path_and_withdraw(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);gates(c,direct_vm);assert c.get_grant(0)["gate_mask"]==15;mock_final(direct_vm);assert c.evaluate_grant(0)=="VERIFIED";assert c.get_grant(0)["state"]=="VERIFIED_CLAIMABLE"
    from genlayer.py.types import Address;direct_vm.sender=Address(B);sent=[];direct_vm._gl_call_hook=lambda vm,r:(sent.append(r["EthSend"]) or {"ok":None});assert c.withdraw(0)=="TRANSFER_REQUESTED";assert int(sent[0]["value"])==AMOUNT;assert c.get_accounting()["locked"]==c.get_accounting()["beneficiary_claimable"]=="0"
def test_final_rejected_until_all_gates(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);mock_gate(direct_vm,0);c.verify_package(0)
    with direct_vm.expect_revert("STAGED_GATES_INCOMPLETE"):c.evaluate_grant(0)
    assert c.get_accounting()["locked"]==str(AMOUNT)
def test_failed_objective_gate_cannot_be_recorded(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);mock_gate(direct_vm,1,run_ok=False)
    with direct_vm.expect_revert("GATE_FAILED_RUN_MISMATCH"):c.verify_run(0)
    assert c.get_grant(0)["gate_mask"]==0 and c.get_accounting()["locked"]==str(AMOUNT)
def test_duplicate_gate_and_terminal_replay_blocked(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);mock_gate(direct_vm,0);c.verify_package(0);mock_gate(direct_vm,0)
    with direct_vm.expect_revert("GATE_ALREADY_SET"):c.verify_package(0)
    gates_rest=((1,"verify_run"),(2,"verify_jobs"),(3,"verify_workflow"))
    for i,n in gates_rest:mock_gate(direct_vm,i);getattr(c,n)(0)
    mock_final(direct_vm);c.evaluate_grant(0);before=c.get_accounting()
    with direct_vm.expect_revert("GRANT_NOT_FUNDED"):c.evaluate_grant(0)
    assert c.get_accounting()==before
@pytest.mark.parametrize("commits",[251,1000])
def test_threshold_rejected_before_custody(direct_vm,direct_deploy,commits):
    c=deploy(direct_vm,direct_deploy);before=c.get_accounting()
    with direct_vm.expect_revert("INVALID_BOUNDS"):c.create_grant(*args(commits=commits))
    assert c.get_accounting()==before
def test_invalid_funding_recoverable(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);direct_vm.value=777;direct_vm.deal(direct_vm._contract_address,777)
    try:assert c.fund_grant(999)=="REFUND_CLAIMABLE"
    finally:direct_vm.value=0
    sent=[];direct_vm._gl_call_hook=lambda vm,r:(sent.append(r["EthSend"]) or {"ok":None});assert c.withdraw_unallocated()=="TRANSFER_REQUESTED";assert int(sent[0]["value"])==777;assert c.get_accounting()["unallocated_claimable"]=="0"
def test_source_failure_preserves_funds(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);mock_gate(direct_vm,2,status=503)
    with direct_vm.expect_revert("GATE_FAILED_JOBS_UNAVAILABLE"):c.verify_jobs(0)
    assert c.get_accounting()["locked"]==str(AMOUNT)
def test_model_failure_is_not_payable(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);fund(c,direct_vm);gates(c,direct_vm);mock_final(direct_vm);direct_vm._llm_mocks.clear();direct_vm.mock_llm("IMPACT_RAIL_V9","bad")
    assert c.evaluate_grant(0)=="INSUFFICIENT_EVIDENCE";assert c.get_grant(0)["state"]=="FUNDED";assert c.get_accounting()["locked"]==str(AMOUNT)
