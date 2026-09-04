"""Direct contract, failure-path and adversarial tests for ImpactRail."""
import json
import pytest

SPONSOR = "0x" + "11" * 20
BENEFICIARY = "0x" + "22" * 20
OTHER = "0x" + "33" * 20
BASE = "a" * 40
TARGET = "b" * 40
PID = "0x" + "44" * 32
PACKAGE = "impactrail-demo"
VERSION = "1.0.0"
SOURCE = "contracts/impact_rail.py"
COVERAGE = 1788307200
AMOUNT = 1000


def body_for(beneficiary=BENEFICIARY, amount=AMOUNT, repo="impactrail/demo", package=PACKAGE, version=VERSION):
    return "\n".join(("impactrail_repo: " + repo, "impactrail_package: " + package, "impactrail_version: " + version,
                      "impactrail_beneficiary: " + beneficiary, "impactrail_amount_wei: " + str(amount),
                      "Milestone: publish a reproducible public-good release"))


def source_payloads(beneficiary=BENEFICIARY, amount=AMOUNT, repo="impactrail/demo", package=PACKAGE, version=VERSION):
    github_repo = {"visibility": "public", "full_name": repo}
    github_commit = {"sha": TARGET, "commit": {"message": "Implement reproducible impact release", "author": {"date": "2026-09-03T00:00:00Z", "name": "Builder"}}}
    compare = {"status": "ahead", "ahead_by": 3, "commits": [
        {"sha": "1" * 40, "author": {"login": "alice"}, "commit": {"author": {"name": "Alice"}}},
        {"sha": "2" * 40, "author": {"login": "bob"}, "commit": {"author": {"name": "Bob"}}},
        {"sha": "3" * 40, "author": {"login": "carol"}, "commit": {"author": {"name": "Carol"}}}]}
    release = {"name": package, "version": version, "gitHead": TARGET, "description": "A public goods release", "repository": {"url": "https://github.com/" + repo + ".git"}}
    npm = {"name": package, "versions": {version: release}, "time": {version: "2026-09-03T00:00:00Z"}}
    proposal = {"id": PID, "body": body_for(beneficiary, amount, repo, package, version), "state": "closed", "type": "single-choice", "start": "2026-09-01T00:00:00Z", "end": "2026-09-03T12:00:00Z", "choices": ["For", "Against", "Abstain"], "scores": [90, 2, 1], "scores_state": "final", "quorum": 1, "space": {"id": "impactrail.eth"}}
    return github_repo, github_commit, compare, npm, proposal


def mocks(vm, *args, model='{"delivery":"FULL","materiality":"SUBSTANTIVE"}', status=200, **kwargs):
    if kwargs:
        base = source_payloads()
        values = {"beneficiary": kwargs.get("beneficiary", base[4].get("impactrail_beneficiary", BENEFICIARY)),
                  "amount": kwargs.get("amount", AMOUNT), "repo": kwargs.get("repo", "impactrail/demo"),
                  "package": kwargs.get("package", PACKAGE), "version": kwargs.get("version", VERSION)}
        args = (values["beneficiary"], values["amount"], values["repo"], values["package"], values["version"])
    repo, commit, compare, npm, proposal = source_payloads(*args)
    vm._web_mocks.clear()
    vm._llm_mocks.clear()
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/commits/", {"status": status, "body": json.dumps(commit)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo/compare/", {"status": status, "body": json.dumps(compare)})
    vm.mock_web(r"api\.github\.com/repos/impactrail/demo$", {"status": status, "body": json.dumps(repo)})
    vm.mock_web(r"registry\.npmjs\.org/impactrail-demo$", {"status": status, "body": json.dumps(npm)})
    vm.mock_web(r"testnet\.hub\.snapshot\.org/graphql", {"status": status, "body": json.dumps({"data": {"proposal": proposal}})})
    vm.mock_llm("IMPACT_RAIL_V2", model)


@pytest.fixture
def ctx(direct_vm, direct_deploy):
    vm = direct_vm
    vm.warp("2026-09-04T00:00:00Z")
    c = direct_deploy(SOURCE, "testnet")
    mocks(vm)
    return vm, c


def register(vm, c):
    from genlayer.py.types import Address
    original = vm.sender
    vm.sender = Address(BENEFICIARY)
    assert c.register_wallet() == "REGISTERED"
    vm.sender = original


def fund(vm, c, beneficiary=BENEFICIARY, amount=AMOUNT, attached=None):
    register(vm, c)
    value = amount if attached is None else attached
    snap = vm.snapshot()
    vm.value = value
    vm.deal(vm._contract_address, vm._balances.get(vm._contract_address, 0) + value)
    try:
        return c.create_grant(beneficiary, amount, "impactrail", "demo", BASE, TARGET, PACKAGE, VERSION, "impactrail.eth", PID,
                              "Publish a reproducible public-good release", 2, 2, COVERAGE, 180, 5000)
    except Exception:
        vm.revert(snap)
        raise
    finally:
        vm.value = 0


def capture_transfer(vm):
    emitted = []
    def hook(context, request):
        if "EthSend" in request:
            emitted.append(request["EthSend"])
            return {"ok": None}
        raise AssertionError(request)
    vm._gl_call_hook = hook
    return emitted


def test_constructor_and_sealed_config(ctx):
    _, c = ctx
    config = c.get_config()
    assert config["version"] == "IMPACT_RAIL_V2" and config["profile"] == "testnet"
    assert config["sources"] == ["github-api", "npm-registry", "snapshot-hub"]


def test_verified_path_and_accounting(ctx):
    vm, c = ctx
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "VERIFIED"
    grant = c.get_grant(grant_id)
    assert grant["state"] == "VERIFIED_CLAIMABLE" and grant["beneficiary_due"] == str(AMOUNT)
    assert c.get_accounting()["locked"] == "0"
    from genlayer.py.types import Address
    vm.sender = Address(BENEFICIARY)
    emitted = capture_transfer(vm)
    assert c.withdraw(grant_id) == "TRANSFER_REQUESTED" and int(emitted[0]["value"]) == AMOUNT
    assert c.get_grant(grant_id)["state"] == "PAID"
    with pytest.raises(Exception, match="NOT_CLAIMABLE"):
        c.withdraw(grant_id)


def test_partial_path_pays_both_parties(ctx):
    vm, c = ctx
    sponsor = vm.sender
    mocks(vm, model='{"delivery":"PARTIAL","materiality":"SUBSTANTIVE"}')
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "PARTIAL"
    assert c.get_grant(grant_id)["beneficiary_due"] == "500"
    from genlayer.py.types import Address
    vm.sender = Address(BENEFICIARY)
    capture_transfer(vm)
    c.withdraw(grant_id)
    vm.sender = sponsor
    capture_transfer(vm)
    c.withdraw(grant_id)
    accounting = c.get_accounting()
    assert accounting["beneficiary_claimable"] == "0" and accounting["sponsor_claimable"] == "0"


def test_mismatch_refunds_sponsor(ctx):
    vm, c = ctx
    sponsor = vm.sender
    mocks(vm, repo="other/project")
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "REJECTED"
    assert c.get_grant(grant_id)["state"] == "REFUND_CLAIMABLE"
    from genlayer.py.types import Address
    vm.sender = sponsor
    capture_transfer(vm)
    assert c.withdraw(grant_id) == "TRANSFER_REQUESTED"


def test_http_failure_is_retryable_and_expiry_refunds(ctx):
    vm, c = ctx
    mocks(vm, status=404)
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "INSUFFICIENT_EVIDENCE"
    assert c.get_accounting()["locked"] == str(AMOUNT)
    vm.warp("2026-09-04T00:04:00Z")
    assert c.expire_grant(grant_id) == "EXPIRED_REFUND_CLAIMABLE"


@pytest.mark.parametrize("case", ["value", "beneficiary", "duration", "commit", "model", "duplicate_marker"])
def test_negative_inputs_fail_closed(ctx, case):
    vm, c = ctx
    if case == "value":
        with pytest.raises(Exception, match="EXACT_VALUE_REQUIRED"):
            fund(vm, c, attached=AMOUNT - 1)
        return
    if case == "beneficiary":
        with pytest.raises(Exception, match="BENEFICIARY_NOT_REGISTERED"):
            fund(vm, c, beneficiary=OTHER)
        return
    if case == "duration":
        register(vm, c)
        vm.value = AMOUNT
        vm.deal(vm._contract_address, AMOUNT)
        with pytest.raises(Exception, match="INVALID_COVERAGE_WINDOW"):
            c.create_grant(BENEFICIARY, AMOUNT, "impactrail", "demo", BASE, TARGET, PACKAGE, VERSION, "impactrail.eth", PID, "x", 2, 2, COVERAGE, 30, 5000)
        vm.value = 0
        return
    if case == "commit":
        register(vm, c)
        vm.value = AMOUNT
        vm.deal(vm._contract_address, AMOUNT)
        with pytest.raises(Exception, match="INVALID_COMMIT_SHA"):
            c.create_grant(BENEFICIARY, AMOUNT, "impactrail", "demo", "0x" + BASE, TARGET, PACKAGE, VERSION, "impactrail.eth", PID, "x", 2, 2, COVERAGE, 180, 5000)
        vm.value = 0
        return
    if case == "model":
        mocks(vm, model='{"delivery":"FULL","materiality":"SUBSTANTIVE","amount":1}')
    if case == "duplicate_marker":
        repo, commit, compare, npm, proposal = source_payloads()
        proposal["body"] += "\nimpactrail_amount_wei: 2"
        vm._web_mocks.clear()
        vm.mock_web(r"api\.github\.com/repos/impactrail/demo/commits/", {"status": 200, "body": json.dumps(commit)})
        vm.mock_web(r"api\.github\.com/repos/impactrail/demo/compare/", {"status": 200, "body": json.dumps(compare)})
        vm.mock_web(r"api\.github\.com/repos/impactrail/demo$", {"status": 200, "body": json.dumps(repo)})
        vm.mock_web(r"registry\.npmjs\.org/impactrail-demo$", {"status": 200, "body": json.dumps(npm)})
        vm.mock_web(r"testnet\.hub\.snapshot\.org/graphql", {"status": 200, "body": json.dumps({"data": {"proposal": proposal}})})
        vm.mock_llm("IMPACT_RAIL_V2", '{"delivery":"FULL","materiality":"SUBSTANTIVE"}')
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "INSUFFICIENT_EVIDENCE"
    assert c.get_grant(grant_id)["state"] == "INSUFFICIENT_EVIDENCE"


def test_unauthorized_and_early_expiry_are_blocked(ctx):
    vm, c = ctx
    grant_id = fund(vm, c)
    from genlayer.py.types import Address
    vm.sender = Address(OTHER)
    with pytest.raises(Exception, match="PARTICIPANT_ONLY"):
        c.evaluate_grant(grant_id)
    with pytest.raises(Exception, match="EVIDENCE_WINDOW_OPEN"):
        c.expire_grant(grant_id)


def test_prompt_injection_does_not_pay(ctx):
    vm, c = ctx
    mocks(vm, model='{"delivery":"UNKNOWN","materiality":"UNKNOWN"}')
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "INSUFFICIENT_EVIDENCE"
    assert c.get_accounting()["locked"] == str(AMOUNT)


def test_cross_source_release_mismatch_rejects(ctx):
    vm, c = ctx
    mocks(vm, package="other-package")
    grant_id = fund(vm, c)
    assert c.evaluate_grant(grant_id) == "REJECTED"
    assert c.get_grant(grant_id)["reason"] == "NPM_RELEASE_MISMATCH"
