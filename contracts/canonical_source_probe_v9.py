# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Diagnostic-only canonical source probe for ImpactRail V9.

This contract has no storage, custody, payout, or configurable URL. Validators
fetch one fixed public source per call and agree on status, byte length and
SHA-256 so unavailable sources are identified before V9 is designed.
"""
import hashlib
import json
from genlayer import *


SOURCES = (
    ("npm_registry", "https://registry.npmjs.org/%40macdon3202%2Fimpactrail-canonical/1.0.0", "npm"),
    ("github_actions_run", "https://api.github.com/repos/macdon3202/IMPACTRAIL/actions/runs/34328794332", "github"),
    ("github_actions_jobs", "https://api.github.com/repos/macdon3202/IMPACTRAIL/actions/runs/34328794332/jobs?per_page=100", "github"),
    ("raw_workflow", "https://raw.githubusercontent.com/macdon3202/IMPACTRAIL/3469b3ff604d4e2d72bf1da3534f9bd427fd5d58/.github/workflows/verify-impactrail-v8.yml", "raw"),
)


class CanonicalSourceProbeV9(gl.Contract):
    def __init__(self):
        pass

    @gl.public.write
    def probe(self, index: int) -> str:
        if index < 0 or index >= len(SOURCES):
            raise gl.vm.UserError("INVALID_SOURCE_INDEX")
        name, url, kind = SOURCES[index]

        def fetch() -> str:
            headers = {"User-Agent": "ImpactRail-V9-Source-Probe"}
            if kind == "github":
                headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
            response = gl.nondet.web.get(url, headers=headers)
            body = response.body if isinstance(response.body, bytes) else b""
            result = {
                "index": index,
                "name": name,
                "status": response.status,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "usable": response.status == 200 and 0 < len(body) <= 128000,
            }
            if response.status != 200:
                result["error_sha256"] = hashlib.sha256(body[:2048]).hexdigest()
            return json.dumps(result, sort_keys=True, separators=(",", ":"))

        return gl.eq_principle.strict_eq(fetch)

    @gl.public.view
    def get_sources(self) -> list:
        return [{"index": i, "name": item[0], "url": item[1]} for i, item in enumerate(SOURCES)]
