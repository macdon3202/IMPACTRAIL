import json
from pathlib import Path

import pytest


CONTRACT = Path(__file__).parents[1] / "contracts" / "canonical_source_probe_v9.py"


def deploy(direct_deploy):
    return direct_deploy(CONTRACT, sdk_version="v0.2.16")


@pytest.mark.parametrize("index,name", [(0, "npm_registry"), (1, "github_actions_run"), (2, "github_actions_jobs"), (3, "raw_workflow")])
def test_each_source_is_independent(direct_vm, direct_deploy, index, name):
    contract = deploy(direct_deploy)
    direct_vm.mock_web(".*", {"status": 200, "body": b"canonical"})
    result = json.loads(contract.probe(index))
    assert result == {
        "bytes": 9,
        "index": index,
        "name": name,
        "sha256": "0deeb8fa1dbbee4c0dbe7f5e3c9183940139f26d22797ee8ab07c00557a4c2ff",
        "status": 200,
        "usable": True,
    }


def test_non_200_is_explicit_and_not_usable(direct_vm, direct_deploy):
    contract = deploy(direct_deploy)
    direct_vm.mock_web(".*", {"status": 403, "body": b"denied"})
    result = json.loads(contract.probe(2))
    assert result["name"] == "github_actions_jobs"
    assert result["status"] == 403
    assert result["usable"] is False
    assert len(result["error_sha256"]) == 64


def test_oversized_source_is_not_usable(direct_vm, direct_deploy):
    contract = deploy(direct_deploy)
    direct_vm.mock_web(".*", {"status": 200, "body": b"x" * 128001})
    result = json.loads(contract.probe(0))
    assert result["bytes"] == 128001
    assert result["usable"] is False


def test_invalid_index_rejected(direct_vm, direct_deploy):
    contract = deploy(direct_deploy)
    with pytest.raises(Exception, match="INVALID_SOURCE_INDEX"):
        contract.probe(4)


def test_source_inventory_is_fixed(direct_vm, direct_deploy):
    sources = deploy(direct_deploy).get_sources()
    assert [item["name"] for item in sources] == ["npm_registry", "github_actions_run", "github_actions_jobs", "raw_workflow"]
    assert all(item["url"].startswith("https://") for item in sources)
