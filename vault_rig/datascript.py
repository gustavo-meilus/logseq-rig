"""Opt-in, read-only named queries against a local Logseq DataScript API."""

from __future__ import annotations

from dataclasses import dataclass
import ipaddress
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .retrieval import Page, RetrievalError, blocks, page_evidence, resolve


class QueryError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code, self.message = code, message
        super().__init__(message)


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, newurl):
        return None


REGISTRY_VERSION = 1
QUERIES = {
    "page-by-name": {
        "arguments": ("name",),
        "result": "page",
        "query": "[:find (pull ?p [*]) :in $ ?name :where [?p :block/name ?name]]",
    },
    "blocks-referencing-page": {
        "arguments": ("page",),
        "result": "block",
        "query": "[:find (pull ?b [*]) :in $ ?page :where [?p :block/name ?page] [?b :block/refs ?p]]",
    },
}


def _loopback(url: str) -> bool:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
        return False
    if parts.hostname.casefold() == "localhost":
        return True
    try:
        return ipaddress.ip_address(parts.hostname).is_loopback
    except ValueError:
        return False


@dataclass(frozen=True)
class Client:
    endpoint: str
    token: str

    @classmethod
    def from_environment(cls) -> "Client":
        endpoint = os.environ.get("VAULT_RIG_LOGSEQ_ENDPOINT", "")
        token = os.environ.get("VAULT_RIG_LOGSEQ_TOKEN", "")
        if not endpoint or not token:
            raise QueryError("bridge_unavailable", "Logseq endpoint and token must be configured")
        if not _loopback(endpoint):
            raise QueryError("invalid_endpoint", "Logseq endpoint must use a loopback HTTP(S) URL")
        return cls(endpoint, token)

    def request(self, query: str, arguments: list[str]) -> dict[str, object]:
        payload = json.dumps({"method": "datascript_query", "params": {"query": query, "args": arguments}}).encode()
        request = Request(self.endpoint, data=payload, headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}, method="POST")
        try:
            with build_opener(_NoRedirect()).open(request, timeout=2) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise QueryError("unauthorized" if error.code in {401, 403} else "bridge_unavailable", f"Logseq endpoint returned HTTP {error.code}") from error
        except (URLError, OSError, UnicodeError, json.JSONDecodeError) as error:
            raise QueryError("bridge_unavailable", "Logseq endpoint is unavailable or returned invalid JSON") from error
        if not isinstance(result, dict) or "result" not in result:
            raise QueryError("api_drift", "Logseq endpoint response does not contain a result")
        return result


def probe() -> dict[str, object]:
    response = Client.from_environment().request("[:find ?e :where [?e :block/uuid]]", [])
    return {"available": True, "api_version": response.get("version", "unreported"), "registry_version": REGISTRY_VERSION}


def _normalize(item: object, result: str, pages: list[Page]) -> dict[str, object]:
    value = item if isinstance(item, dict) else {}
    if result == "page" and isinstance(value.get("name"), str):
        try:
            return {"live": value, "evidence": page_evidence(resolve(pages, value["name"]))}
        except RetrievalError:
            pass
    if result == "block" and isinstance(value.get("uuid"), str):
        match = next((block for block in blocks(pages) if block.uuid == value["uuid"]), None)
        if match:
            return {"live": value, "evidence": match.evidence()}
    return {"live": item, "evidence": None, "evidence_status": "unresolved_live_entity"}


def execute(name: str, arguments: list[str], pages: list[Page], *, registry_version: int = REGISTRY_VERSION) -> dict[str, object]:
    if registry_version != REGISTRY_VERSION:
        raise QueryError("incompatible_registry", "named-query registry version is unsupported")
    query = QUERIES.get(name)
    if query is None:
        raise QueryError("unknown_query", f"unknown named query: {name}")
    if len(arguments) != len(query["arguments"]) or not all(isinstance(value, str) and value for value in arguments):
        raise QueryError("invalid_arguments", f"{name} requires: {', '.join(query['arguments'])}")
    response = Client.from_environment().request(query["query"], arguments)
    raw = response["result"]
    if not isinstance(raw, list):
        raise QueryError("malformed_result", "Logseq query result must be a list")
    return {"query": name, "registry_version": REGISTRY_VERSION, "api_version": response.get("version", "unreported"), "results": [_normalize(item, query["result"], pages) for item in raw]}
