import hashlib
import json

import pytest


CONTRACT = "contracts/impact_rail_v8.py"
A = bytes.fromhex("11" * 20)
B = bytes.fromhex("22" * 20)
B_HEX = "0x" + "22" * 20
BASE = "a" * 40
TARGET = "b" * 40
ARTIFACT = b"canonical project-authored artifact"
ARTIFACT_SHA = hashlib.sha256(ARTIFACT).hexdigest()
AMOUNT = 1000
START_TS = 1788652800
NOW = "2026-09-07T12:00:00+00:00"
VERIFY = "c" * 40
WORKFLOW_PATH = ".github/workflows/verify-impactrail-v8.yml"
WORKFLOW = b"name: canonical verification"
WORKFLOW_SHA = hashlib.sha256(WORKFLOW).hexdigest()
RUN_ID = 12345


def deploy(vm, direct_deploy):
    vm.warp(NOW)
    vm.strict_mocks = True
    contract = direct_deploy(CONTRACT)
    from genlayer.py.types import Address
    original = vm.sender
    vm.sender = Address(B_HEX)
    contract.register_wallet()
    vm.sender = original
    return contract


def release_body():
    return "\n".join((
        "impactrail_repo: impactrail/demo",
        "impactrail_target_commit: " + TARGET,
        "impactrail_artifact_path: evidence/report.md",
        "impactrail_artifact_sha256: " + ARTIFACT_SHA,
        "impactrail_release_tag: v1.0.0",
        "impactrail_beneficiary: " + B_HEX,
        "impactrail_amount_wei: 1000",
    ))


def payloads(repository="https://github.com/impactrail/demo.git", git_head=TARGET,
             run_head=VERIFY, run_conclusion="success", workflow=WORKFLOW):
    repo = {"visibility": "public", "full_name": "impactrail/demo"}
    commit = {"sha": TARGET, "commit": {"message": "release", "author": {"date": "2026-09-06T10:00:00Z"}}}
    compare = {"status": "ahead", "ahead_by": 1, "total_commits": 1, "base_commit": {"sha": BASE}, "commits": [{"sha": TARGET, "author": {"login": "builder"}, "commit": {"author": {"date": "2026-09-06T10:00:00Z"}}}]}
    release = {"tag_name": "v1.0.0", "target_commitish": TARGET, "draft": False, "prerelease": False, "published_at": "2026-09-06T11:00:00Z", "body": release_body()}
    metadata = {"name": "impact-package", "version": "1.0.0", "repository": {"url": repository}, "gitHead": git_head}
    run = {"id": RUN_ID, "head_sha": run_head, "head_repository": {"full_name": "impactrail/demo"}, "head_branch": "main",
           "event": "push", "status": "completed", "conclusion": run_conclusion, "path": WORKFLOW_PATH, "run_attempt": 1}
    names = {"Checkout sealed source", "Verify npm registry binding", "Install published package", "Validate V8 contract",
             "Run V8 contract tests", "Test frontend journal", "Build production frontend"}
    jobs = {"total_count": 1, "jobs": [{"id": 88, "head_sha": run_head, "conclusion": run_conclusion,
            "steps": [{"name": name, "conclusion": "success"} for name in sorted(names)]}]}
    return repo, commit, compare, release, metadata, run, jobs, workflow


def mocks(vm, repository="https://github.com/impactrail/demo.git", git_head=TARGET,
          run_head=VERIFY, run_conclusion="success", workflow=WORKFLOW, fit="YES", status=200):
    repo, commit, compare, release, metadata, run, jobs, workflow_bytes = payloads(repository, git_head, run_head, run_conclusion, workflow)
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo$", {"status": status, "body": json.dumps(repo)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/commits/", {"status": status, "body": json.dumps(commit)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/compare/", {"status": status, "body": json.dumps(compare)})
    vm.mock_web(r"raw\.githubusercontent\.com/impactrail/demo/" + TARGET, {"status": status, "body": ARTIFACT})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/releases/tags/", {"status": status, "body": json.dumps(release)})
    vm.mock_web(r"registry\.npmjs\.org/impact-package/1\.0\.0", {"status": status, "body": json.dumps(metadata)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/actions/runs/" + str(RUN_ID) + r"$", {"status": status, "body": json.dumps(run)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/actions/runs/" + str(RUN_ID) + r"/jobs", {"status": status, "body": json.dumps(jobs)})
    vm.mock_web(r"raw\.githubusercontent\.com/impactrail/demo/" + VERIFY + r"/" + WORKFLOW_PATH, {"status": status, "body": workflow_bytes})
    vm.mock_llm("IMPACT_RAIL_V8", {"delivery": "FULL", "materiality": "SUBSTANTIVE"} if fit == "YES" else {"delivery": "NONE", "materiality": "COSMETIC"})

def create(contract, vm, minimum_commits=1, value=AMOUNT, verification_commit=VERIFY,
           workflow_path=WORKFLOW_PATH, workflow_sha256=WORKFLOW_SHA, workflow_run_id=RUN_ID):
    args = [B_HEX, AMOUNT, "impactrail", "demo", BASE, TARGET, "evidence/report.md", ARTIFACT_SHA, "v1.0.0",
            "Fund a reproducibly verified open-source public infrastructure package.", minimum_commits, 1, START_TS, 900, 5000,
            "impact-package", "1.0.0", verification_commit, workflow_path, workflow_sha256, workflow_run_id]
    grant_id = contract.create_grant(*args)
    vm.value = value
    vm.deal(vm._contract_address, vm._balances.get(vm._contract_address, 0) + value)
    try:
        result = contract.fund_grant(grant_id)
        if value == AMOUNT:
            assert result == "FUNDED"
        return grant_id
    finally:
        vm.value = 0

def test_config_exposes_objective_sources_and_bounds(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    config = contract.get_config()
    assert config["version"] == "IMPACT_RAIL_V8"
    assert config["max_verifiable_commits"] == 250
    assert "github-actions-jobs" in config["sources"]
    assert config["max_attempts"] == 3
    assert "commit-pinned-workflow" in config["sources"]


@pytest.mark.parametrize("commits,error", [(251, "INVALID_COVERAGE_WINDOW"), (1000, "INVALID_COVERAGE_WINDOW")])
def test_unsupported_commit_threshold_rejected_before_custody(direct_vm, direct_deploy, commits, error):
    contract = deploy(direct_vm, direct_deploy)
    before = contract.get_accounting()
    with direct_vm.expect_revert(error):
        create(contract, direct_vm, minimum_commits=commits)
    assert contract.get_accounting() == before
    assert contract.get_config()["version"] == "IMPACT_RAIL_V8"


def test_objective_adoption_happy_path(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "VERIFIED"
    grant = contract.get_grant(0)
    assert grant["state"] == "VERIFIED_CLAIMABLE"
    assert grant["observation"]["package_binding"] == "YES"
    assert grant["observation"]["adoption_binding"] == "YES"


def test_project_authored_narrative_cannot_bypass_missing_adoption(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm, run_conclusion="failure", fit="YES")
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "REJECTED"
    assert contract.get_grant(0)["reason"] == "OBJECTIVE_VERIFICATION_FAILED"
    assert contract.get_grant(0)["state"] == "REFUND_CLAIMABLE"


@pytest.mark.parametrize("kwargs", [
    {"repository": "https://github.com/other/repo.git"},
    {"git_head": "d" * 40},
    {"run_head": "d" * 40},
    {"workflow": b"changed workflow"},
])
def test_npm_object_and_period_binding_fail_closed(direct_vm, direct_deploy, kwargs):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm, **kwargs)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "REJECTED"
    assert contract.get_grant(0)["state"] == "REFUND_CLAIMABLE"


def test_source_unavailable_is_retryable_not_payable(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm, status=503)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "INSUFFICIENT_EVIDENCE"
    grant = contract.get_grant(0)
    assert grant["state"] == "INSUFFICIENT_EVIDENCE"
    assert grant["beneficiary_due"] == "0"


def test_terminal_replay_does_not_change_accounting(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    contract.evaluate_grant(0)
    before = contract.get_accounting()
    with direct_vm.expect_revert("GRANT_TERMINAL"):
        contract.retry_grant(0)
    assert contract.get_accounting() == before


@pytest.mark.parametrize("kwargs,error", [
    ({"workflow_path": "verify.yml"}, "INVALID_WORKFLOW_PATH"),
    ({"workflow_sha256": "f" * 63}, "INVALID_WORKFLOW_DIGEST"),
    ({"workflow_run_id": 0}, "INVALID_WORKFLOW_RUN"),
    ({"verification_commit": "z" * 40}, "INVALID_VERIFICATION_COMMIT"),
])
def test_unsupported_verification_terms_rejected_before_custody(direct_vm, direct_deploy, kwargs, error):
    contract = deploy(direct_vm, direct_deploy)
    before = contract.get_accounting()
    with direct_vm.expect_revert(error):
        create(contract, direct_vm, **kwargs)
    assert contract.get_accounting() == before

def test_model_failure_cannot_bypass_objective_gate(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm)
    direct_vm._llm_mocks.clear()
    direct_vm.mock_llm("IMPACT_RAIL_V8", "not-json")
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "INSUFFICIENT_EVIDENCE"
    grant = contract.get_grant(0)
    assert grant["state"] == "INSUFFICIENT_EVIDENCE"
    assert grant["beneficiary_due"] == "0"


def test_validator_rejects_changed_objective_adoption(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    contract.evaluate_grant(0)
    assert direct_vm.run_validator() is True
    direct_vm._web_mocks.clear()
    direct_vm._llm_mocks.clear()
    mocks(direct_vm, run_conclusion="failure")
    assert direct_vm.run_validator() is False


def test_verified_withdraw_conserves_accounting(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    assert contract.evaluate_grant(0) == "VERIFIED"
    emitted = []
    def hook(vm, request):
        if "EthSend" in request:
            emitted.append(request["EthSend"])
            return {"ok": None}
        raise AssertionError(request)
    direct_vm._gl_call_hook = hook
    assert contract.withdraw(0) == "TRANSFER_REQUESTED"
    assert int(emitted[0]["value"]) == AMOUNT
    accounting = contract.get_accounting()
    assert accounting["locked"] == accounting["beneficiary_claimable"] == accounting["sponsor_claimable"] == "0"
    assert accounting["outbound_requested"] == str(AMOUNT)
    assert contract.get_grant(0)["state"] == "PAID"


def test_attempt_cap_preserves_locked_funds(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    create(contract, direct_vm)
    mocks(direct_vm, status=503)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    for instant in ("2026-09-07T12:00:00+00:00", "2026-09-07T12:01:01+00:00", "2026-09-07T12:02:02+00:00"):
        direct_vm.warp(instant)
        assert contract.retry_grant(0) == "INSUFFICIENT_EVIDENCE"
    before = contract.get_accounting()
    direct_vm.warp("2026-09-07T12:03:03+00:00")
    with direct_vm.expect_revert("MAX_ATTEMPTS_REACHED"):
        contract.retry_grant(0)
    assert contract.get_accounting() == before
    assert before["locked"] == str(AMOUNT)



def test_creation_is_nonpayable_draft_then_exact_funding_locks(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    args = [B_HEX, AMOUNT, "impactrail", "demo", BASE, TARGET, "evidence/report.md", ARTIFACT_SHA, "v1.0.0",
            "Fund a reproducibly verified open-source public infrastructure package.", 1, 1, START_TS, 900, 5000,
            "impact-package", "1.0.0", VERIFY, WORKFLOW_PATH, WORKFLOW_SHA, RUN_ID]
    grant_id = contract.create_grant(*args)
    assert contract.get_grant(grant_id)["state"] == "DRAFT"
    assert contract.get_accounting()["locked"] == "0"
    direct_vm.value = AMOUNT
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + AMOUNT)
    try:
        assert contract.fund_grant(grant_id) == "FUNDED"
    finally:
        direct_vm.value = 0
    assert contract.get_grant(grant_id)["state"] == "FUNDED"
    assert contract.get_accounting()["locked"] == str(AMOUNT)


def test_invalid_payable_funding_is_recoverable_not_rolled_back(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.value = 777
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + 777)
    try:
        assert contract.fund_grant(999) == "REFUND_CLAIMABLE"
    finally:
        direct_vm.value = 0
    accounting = contract.get_accounting()
    assert accounting["unallocated_claimable"] == "777"
    assert accounting["balance"] == "777"
    emitted = []
    def hook(vm, request):
        if "EthSend" in request:
            emitted.append(request["EthSend"])
            return {"ok": None}
        raise AssertionError(request)
    direct_vm._gl_call_hook = hook
    assert contract.withdraw_unallocated() == "TRANSFER_REQUESTED"
    assert int(emitted[0]["value"]) == 777
    assert contract.get_accounting()["unallocated_claimable"] == "0"


def test_wrong_amount_and_repeated_funding_are_explicit_refunds(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    args = [B_HEX, AMOUNT, "impactrail", "demo", BASE, TARGET, "evidence/report.md", ARTIFACT_SHA, "v1.0.0",
            "Fund a reproducibly verified open-source public infrastructure package.", 1, 1, START_TS, 900, 5000,
            "impact-package", "1.0.0", VERIFY, WORKFLOW_PATH, WORKFLOW_SHA, RUN_ID]
    grant_id = contract.create_grant(*args)
    direct_vm.value = 999
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + 999)
    assert contract.fund_grant(grant_id) == "REFUND_CLAIMABLE"
    assert contract.get_grant(grant_id)["state"] == "DRAFT"
    direct_vm.value = AMOUNT
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + AMOUNT)
    assert contract.fund_grant(grant_id) == "FUNDED"
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + AMOUNT)
    assert contract.fund_grant(grant_id) == "REFUND_CLAIMABLE"
    direct_vm.value = 0
    sponsor = contract.get_grant(grant_id)["sponsor"]
    assert contract.get_unallocated_refund(sponsor) == str(999 + AMOUNT)
    accounting = contract.get_accounting()
    assert accounting["locked"] == str(AMOUNT)
    assert accounting["unallocated_claimable"] == str(999 + AMOUNT)


def test_outsider_funding_cannot_capture_draft_or_trap_value(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    args = [B_HEX, AMOUNT, "impactrail", "demo", BASE, TARGET, "evidence/report.md", ARTIFACT_SHA, "v1.0.0",
            "Fund a reproducibly verified open-source public infrastructure package.", 1, 1, START_TS, 900, 5000,
            "impact-package", "1.0.0", VERIFY, WORKFLOW_PATH, WORKFLOW_SHA, RUN_ID]
    grant_id = contract.create_grant(*args)
    from genlayer.py.types import Address
    direct_vm.sender = Address(B_HEX)
    direct_vm.value = AMOUNT
    direct_vm.deal(direct_vm._contract_address, direct_vm._balances.get(direct_vm._contract_address, 0) + AMOUNT)
    try:
        assert contract.fund_grant(grant_id) == "REFUND_CLAIMABLE"
    finally:
        direct_vm.value = 0
    assert contract.get_grant(grant_id)["state"] == "DRAFT"
    assert contract.get_unallocated_refund(B_HEX) == str(AMOUNT)
    assert contract.get_accounting()["locked"] == "0"
