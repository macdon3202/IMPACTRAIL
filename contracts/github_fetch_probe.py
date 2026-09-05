# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Diagnostic only: no custody, no eligibility decisions, fixed public sources."""
import json
from genlayer import *


class GitHubFetchProbe(gl.Contract):
    def __init__(self):
        pass

    @gl.public.write
    def probe(self, index: int, with_headers: bool) -> str:
        root = "https://api.github.com/repos/macdon3202/IMPACTRAIL"
        target = "536091b33cb4c4a9cd45fb224277aa3c451889b3"
        urls = (root, root + "/commits/" + target,
                root + "/compare/ef0a23e4470dfaef0c38cfface89fcabf8225cd8..." + target,
                "https://raw.githubusercontent.com/macdon3202/IMPACTRAIL/" + target + "/evidence/impact-report.md",
                root + "/releases/tags/impactrail-v4-fixture")
        if index < 0 or index >= len(urls):
            raise gl.vm.UserError("INVALID_SOURCE")

        def fetch():
            headers = {}
            if with_headers:
                headers = {"User-Agent": "ImpactRail"}
                if index != 3:
                    headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
            response = gl.nondet.web.get(urls[index], headers=headers)
            body = response.body or b""
            return json.dumps({"index": index, "with_headers": with_headers,
                               "status": response.status, "bytes": len(body),
                               "error_excerpt": body[:700].decode("utf-8", errors="replace") if response.status != 200 else ""})

        return gl.eq_principle.strict_eq(fetch)
