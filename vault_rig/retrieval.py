"""Deterministic, on-demand retrieval from supported Logseq Markdown vaults."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

from .detection import VaultDescriptor


class RetrievalError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code, self.message = code, message
        super().__init__(message)


BLOCK = re.compile(r"^(?P<indent>[ \t]*)-\s+(?P<text>.*)$")
PROPERTY = re.compile(r"^(?P<indent>[ \t]*)(?P<key>[\w-]+)::\s*(?P<value>.*)$")
PAGE_REF = re.compile(r"\[\[([^\]]+)\]\]")
BLOCK_REF = re.compile(r"\(\(([\w-]+)\)\)")
TASK = re.compile(r"\b(?:TODO|DOING|DONE|LATER|NOW|WAITING|CANCELED)\b")


@dataclass
class Block:
    path: str
    page: str
    line: int
    indent: int
    text: str
    properties: dict[str, str] = field(default_factory=dict)
    parent: "Block | None" = None
    children: list["Block"] = field(default_factory=list)

    @property
    def uuid(self) -> str | None:
        return self.properties.get("id")

    @property
    def page_refs(self) -> list[str]:
        return PAGE_REF.findall(self.text) + [ref for value in self.properties.values() for ref in PAGE_REF.findall(value)]

    @property
    def block_refs(self) -> list[str]:
        return BLOCK_REF.findall(self.text) + [ref for value in self.properties.values() for ref in BLOCK_REF.findall(value)]

    def evidence(self, *, include_children: int = 0) -> dict[str, object]:
        value: dict[str, object] = {"file": self.path, "line": self.line, "page": self.page, "text": self.text, "properties": self.properties}
        if self.uuid:
            value["id"] = self.uuid
        if include_children:
            value["children"] = [child.evidence(include_children=include_children - 1) for child in self.children]
        return value


@dataclass
class Page:
    name: str
    path: str
    properties: dict[str, str]
    blocks: list[Block]

    @property
    def aliases(self) -> list[str]:
        raw = self.properties.get("alias", self.properties.get("aliases", ""))
        return PAGE_REF.findall(raw) or [item.strip() for item in raw.split(",") if item.strip()]


def _logical_name(relative: Path) -> str:
    return unquote(relative.with_suffix("").as_posix()).replace("___", "/")


def _files(descriptor: VaultDescriptor) -> list[Path]:
    root = Path(descriptor.root)
    return sorted(path for directory in (descriptor.pages_directory, descriptor.journals_directory) for path in (root / directory).rglob("*.md"))


def _parse(path: Path, root: Path, page: str) -> Page:
    blocks: list[Block] = []
    roots: list[Block] = []
    page_properties: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = BLOCK.match(line)
        if match:
            indent = len(match["indent"].expandtabs(2))
            while blocks and blocks[-1].indent >= indent:
                blocks.pop()
            block = Block(path.relative_to(root).as_posix(), page, line_number, indent, match["text"], parent=blocks[-1] if blocks else None)
            (blocks[-1].children if blocks else roots).append(block)
            blocks.append(block)
            continue
        property_match = PROPERTY.match(line)
        if property_match:
            key, value = property_match["key"], property_match["value"]
            indent = len(property_match["indent"].expandtabs(2))
            target = next((block for block in reversed(blocks) if indent > block.indent), None)
            (target.properties if target else page_properties)[key] = value
    return Page(page, path.relative_to(root).as_posix(), page_properties, roots)


def load(descriptor: VaultDescriptor) -> list[Page]:
    root = Path(descriptor.root)
    pages: list[Page] = []
    for directory in (descriptor.pages_directory, descriptor.journals_directory):
        base = root / directory
        for path in sorted(base.rglob("*.md")):
            pages.append(_parse(path, root, _logical_name(path.relative_to(base))))
    return pages


def blocks(pages: list[Page]) -> list[Block]:
    result: list[Block] = []
    def visit(block: Block) -> None:
        result.append(block)
        for child in block.children:
            visit(child)
    for page in pages:
        for block in page.blocks:
            visit(block)
    return result


def resolve(pages: list[Page], name: str) -> Page:
    matches = [page for page in pages if name == page.name or name in page.aliases]
    if not matches:
        raise RetrievalError("not_found", f"page not found: {name}")
    if len(matches) != 1:
        raise RetrievalError("ambiguous_page", f"page is ambiguous: {name}")
    return matches[0]


def find(pages: list[Page], query: str) -> list[dict[str, object]]:
    needle = query.casefold()
    return [block.evidence() for block in blocks(pages) if needle in block.text.casefold() or needle in " ".join(f"{key} {value}" for key, value in block.properties.items()).casefold() or needle in " ".join(block.page_refs + block.block_refs + ([block.uuid] if block.uuid else [])).casefold() or (TASK.search(block.text) and needle == TASK.search(block.text).group(0).casefold())]


def context(pages: list[Page], query: str, children: int) -> list[dict[str, object]]:
    result = []
    for block in blocks(pages):
        if query.casefold() in block.text.casefold():
            item = block.evidence(include_children=children)
            item["ancestors"] = [ancestor.evidence() for ancestor in reversed(list(_ancestors(block)))]
            result.append(item)
    return result


def _ancestors(block: Block):
    while block.parent:
        block = block.parent
        yield block


def page_evidence(page: Page) -> dict[str, object]:
    return {"page": page.name, "file": page.path, "properties": page.properties, "aliases": page.aliases, "blocks": [block.evidence(include_children=99) for block in page.blocks]}


def block(pages: list[Page], identifier: str) -> dict[str, object]:
    matches = [item for item in blocks(pages) if item.uuid == identifier]
    if len(matches) != 1:
        raise RetrievalError("not_found" if not matches else "ambiguous_block", f"block not uniquely found: {identifier}")
    item = matches[0].evidence(include_children=1)
    item["ancestors"] = [ancestor.evidence() for ancestor in reversed(list(_ancestors(matches[0])))]
    return item


def refs(pages: list[Page], name: str) -> list[dict[str, object]]:
    page = resolve(pages, name)
    return [item.evidence() for item in blocks([page]) if item.page_refs or item.block_refs]


def backlinks(pages: list[Page], name: str) -> list[dict[str, object]]:
    page = resolve(pages, name)
    names = {page.name, *page.aliases}
    return [item.evidence() for item in blocks(pages) if any(ref in names for ref in item.page_refs)]


def history(descriptor: VaultDescriptor, query: str, pages: list[Page]) -> list[dict[str, object]]:
    root = Path(descriptor.root)
    source = root / query
    if source.is_file():
        scope = [source.relative_to(root).as_posix()]
        search: list[str] = []
    else:
        try:
            scope = [resolve(pages, query).path]
            search = []
        except RetrievalError:
            scope = [descriptor.pages_directory, descriptor.journals_directory]
            search = ["-S", query]
    command = ["git", "-C", descriptor.root, "log", "--format=%H%x00%an%x00%aI%x00%s", "--name-only", *search, "--", *scope]
    try:
        output = subprocess.run(command, text=True, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        raise RetrievalError("history_unavailable", "Git history is unavailable for this vault") from error
    result: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in output.splitlines():
        fields = line.split("\0")
        if len(fields) == 4:
            current = {"commit": fields[0], "author": fields[1], "date": fields[2], "subject": fields[3], "files": []}
            result.append(current)
        elif line and current is not None:
            current["files"].append(line)
    return result
