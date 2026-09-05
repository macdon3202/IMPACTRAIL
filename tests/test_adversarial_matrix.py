"""Adversarial assertions against the real V4 contract; failures remain failures."""
import json
import pytest
from test_impact_rail import (ctx, source_payloads, fund, mocks, register, capture_transfer,
    BENEFICIARY, OTHER, AMOUNT, BASE, TARGET, ARTIFACT_PATH, ARTIFACT_SHA256, RELEASE, COVERAGE)

def install(vm, payloads):
    patterns = (r"api\.github\.com/repos/impactrail/demo$", r"api\.github\.com/repos/impactrail/demo/commits/",
                r"api\.github\.com/repos/impactrail/demo/compare/", r"raw\.githubusercontent\.com/impactrail/demo/",
                r"api\.github\.com/repos/impactrail/demo/releases/tags/")
    vm._web_mocks.clear()
    for pattern, payload in zip(patterns, payloads):
        vm.mock_web(pattern, {"status": 200, "body": payload if isinstance(payload, bytes) else json.dumps(payload)})

@pytest.mark.parametrize('field,value', [('impactrail_beneficiary', OTHER), ('impactrail_amount_wei','999'),
 ('impactrail_target_commit','c'*40), ('impactrail_artifact_sha256','d'*64), ('impactrail_repo','evil/other')])
def test_release_binding(ctx, field, value):
    vm,c=ctx
    p=source_payloads()
    p[4]['body']='\n'.join(field+': '+value if line.startswith(field+':') else line for line in p[4]['body'].splitlines())
    install(vm,p)
    gid=fund(vm,c)
    assert c.evaluate_grant(gid)=='REJECTED'
    assert c.get_grant(gid)['beneficiary_due']=='0'

def test_retry_append_only_and_cooldown(ctx):
    vm,c=ctx
    mocks(vm,status=500);gid=fund(vm,c)
    assert c.evaluate_grant(gid)=='INSUFFICIENT_EVIDENCE'
    first=c.get_attempts(gid,0)
    with pytest.raises(Exception,match='RETRY_COOLDOWN'):c.retry_grant(gid)
    vm.warp('2026-09-04T00:01:01Z');mocks(vm)
    assert c.retry_grant(gid)=='VERIFIED'
    assert c.get_attempts(gid,0)[:1]==first
    assert c.get_grant(gid)['attempt_count']==2
    with pytest.raises(Exception,match='GRANT_TERMINAL'):c.retry_grant(gid)

def test_outsider_withdraw_preserves_state(ctx):
    from genlayer.py.types import Address
    vm,c=ctx;gid=fund(vm,c);c.evaluate_grant(gid)
    before=c.get_accounting();grant=c.get_grant(gid)
    vm.sender=Address(OTHER)
    with pytest.raises(Exception,match='RECIPIENT_ONLY'):c.withdraw(gid)
    assert c.get_accounting()==before and c.get_grant(gid)==grant

def test_unverified_author_names_do_not_satisfy_contributors(ctx):
    vm,c=ctx;p=source_payloads()
    for i,commit in enumerate(p[2]['commits']):
        commit['author']=None
        commit['commit']['author']['name']='invented identity '+str(i)
    install(vm,p);gid=fund(vm,c)
    assert c.evaluate_grant(gid)!='VERIFIED', 'unverified Git author names satisfy the contributor threshold'

def test_same_evidence_cannot_bypass_dedup_by_duration(ctx):
    vm,c=ctx;fund(vm,c)
    vm.value=AMOUNT;vm.deal(vm._contract_address,AMOUNT*2)
    with pytest.raises(Exception,match='DUPLICATE_GRANT'):
        c.create_grant(BENEFICIARY,AMOUNT,'impactrail','demo',BASE,TARGET,ARTIFACT_PATH,ARTIFACT_SHA256,RELEASE,
                      'Publish a reproducible public-good release',2,2,COVERAGE,181,5000)

@pytest.mark.parametrize('source', ['commit','release'])
def test_future_timestamp_cannot_verify(ctx,source):
    vm,c=ctx;p=source_payloads()
    if source=='commit':p[1]['commit']['author']['date']='2099-01-01T00:00:00Z'
    else:p[4]['published_at']='2099-01-01T00:00:00Z'
    install(vm,p);gid=fund(vm,c)
    assert c.evaluate_grant(gid)!='VERIFIED', 'future evidence accepted'

@pytest.mark.parametrize('mutation', ['base','tip','pagination','old_range_commit'])
def test_compare_range_must_be_complete_and_time_bound(ctx,mutation):
    vm,c=ctx;p=source_payloads()
    if mutation=='base':p[2]['base_commit']['sha']='f'*40
    if mutation=='tip':p[2]['commits'][-1]['sha']='e'*40
    if mutation=='pagination':p[2]['total_commits']=4
    if mutation=='old_range_commit':p[2]['commits'][0]['commit']['author']['date']='2020-01-01T00:00:00Z'
    install(vm,p);gid=fund(vm,c)
    assert c.evaluate_grant(gid)!='VERIFIED'

def test_exact_duplicate_blocked(ctx):
    vm,c=ctx;fund(vm,c)
    with pytest.raises(Exception,match='DUPLICATE_GRANT'):fund(vm,c)

def test_partial_rounding_conserves_amount(ctx):
    vm,c=ctx;mocks(vm,amount=1001,model='{"delivery":"PARTIAL","materiality":"SUBSTANTIVE"}')
    gid=fund(vm,c,amount=1001);assert c.evaluate_grant(gid)=='PARTIAL'
    g=c.get_grant(gid);assert int(g['beneficiary_due'])+int(g['sponsor_due'])==1001

def test_validator_rejects_different_evidence(ctx):
    vm,c=ctx;gid=fund(vm,c);c.evaluate_grant(gid)
    assert vm.run_validator() is True
    mocks(vm,artifact=b'changed after leader read')
    assert vm.run_validator() is False

def test_validator_rejects_different_model_observation(ctx):
    vm,c=ctx;gid=fund(vm,c);c.evaluate_grant(gid)
    mocks(vm,model='{"delivery":"PARTIAL","materiality":"SUBSTANTIVE"}')
    assert vm.run_validator() is False

def test_validator_rejects_fetch_failure(ctx):
    vm,c=ctx;gid=fund(vm,c);c.evaluate_grant(gid)
    mocks(vm,status=403)
    assert vm.run_validator() is False

def test_validator_ignores_unrelated_mutable_api_fields(ctx):
    vm,c=ctx;gid=fund(vm,c);c.evaluate_grant(gid)
    p=source_payloads();p[0]['stargazers_count']=999;p[4]['reactions']={'total_count':42}
    install(vm,p);mocks_model='{"delivery":"FULL","materiality":"SUBSTANTIVE"}'
    vm.mock_llm('IMPACT_RAIL_V5',mocks_model)
    assert vm.run_validator() is True

@pytest.mark.parametrize('model', ['{}','not json','{"delivery":"FULL"}',
 '{"delivery":"FULL","materiality":"SUBSTANTIVE","extra":true}'])
def test_invalid_model_never_unlocks(ctx,model):
    vm,c=ctx;mocks(vm,model=model);gid=fund(vm,c)
    assert c.evaluate_grant(gid)=='INSUFFICIENT_EVIDENCE'
    assert c.get_accounting()['locked']==str(AMOUNT)
