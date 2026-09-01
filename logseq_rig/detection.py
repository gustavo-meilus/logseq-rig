"""Read-only detection for supported Logseq OG file graphs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


class DetectionError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class GraphDescriptor:
    version: int
    root: str
    pages_directory: str
    journals_directory: str
    page_filename_mode: str
    journal_filename_format: str
    evidence: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class EdnReader:
    """Small EDN reader for config maps; only set literals are accepted reader forms."""

    def __init__(self, text: str) -> None:
        self.text, self.position = text, 0

    def read(self) -> object:
        value = self._value()
        self._space()
        if self.position != len(self.text):
            raise ValueError("unexpected trailing EDN")
        return value

    def _space(self) -> None:
        while self.position < len(self.text):
            if self.text[self.position].isspace():
                self.position += 1
            elif self.text[self.position] == ";":
                newline = self.text.find("\n", self.position)
                self.position = len(self.text) if newline < 0 else newline + 1
            else:
                return

    def _value(self) -> object:
        self._space()
        if self.position >= len(self.text):
            raise ValueError("unexpected end of EDN")
        char = self.text[self.position]
        if self.text.startswith("#{", self.position):
            self.position += 1
            return self._collection("}")
        if char == "#":
            raise ValueError("EDN reader forms are unsupported")
        if char == "{":
            return self._map()
        if char == "[":
            return self._collection("]")
        if char == "(":
            return self._collection(")")
        if char == '"':
            return self._string()
        if char in "}])":
            raise ValueError(f"unexpected {char}")
        return self._atom()

    def _map(self) -> dict[str, object]:
        self.position += 1
        result: dict[str, object] = {}
        while True:
            self._space()
            if self.position >= len(self.text):
                raise ValueError("unterminated map")
            if self.text[self.position] == "}":
                self.position += 1
                return result
            key = self._value()
            if not isinstance(key, str):
                raise ValueError("map key is not scalar")
            self._space()
            if self.position >= len(self.text) or self.text[self.position] == "}":
                raise ValueError("map value is missing")
            result[key] = self._value()

    def _collection(self, end: str) -> list[object]:
        self.position += 1
        result: list[object] = []
        while True:
            self._space()
            if self.position >= len(self.text):
                raise ValueError("unterminated collection")
            if self.text[self.position] == end:
                self.position += 1
                return result
            result.append(self._value())

    def _string(self) -> str:
        self.position += 1
        result: list[str] = []
        while self.position < len(self.text):
            char = self.text[self.position]
            self.position += 1
            if char == '"':
                return "".join(result)
            if char == "\\":
                if self.position >= len(self.text):
                    break
                char = self.text[self.position]
                self.position += 1
                result.append({"n": "\n", "r": "\r", "t": "\t"}.get(char, char))
            else:
                result.append(char)
        raise ValueError("unterminated string")

    def _atom(self) -> str:
        start = self.position
        while self.position < len(self.text) and not self.text[self.position].isspace() and self.text[self.position] not in "{}[]();\"":
            self.position += 1
        if start == self.position:
            raise ValueError("invalid EDN atom")
        return self.text[start:self.position]


def _directory(root: Path, value: object, key: str) -> tuple[Path, str]:
    if not isinstance(value, str) or not value or value.startswith(":"):
        raise DetectionError("malformed_config", f"{key} must be a non-empty string")
    candidate = (root / value).resolve()
    try:
        relative = candidate.relative_to(root)
    except ValueError as error:
        raise DetectionError("path_escape", f"{key} escapes the selected graph") from error
    if not candidate.is_dir():
        raise DetectionError("missing_evidence", f"configured {key} directory is missing")
    return candidate, relative.as_posix()


def detect(root: Path) -> GraphDescriptor:
    root = root.resolve()
    if not root.is_dir():
        raise DetectionError("non_graph", "target folder does not exist")
    if (root / "db.sqlite").exists():
        raise DetectionError("db_graph", "Logseq DB graphs are unsupported")
    config = root / "logseq" / "config.edn"
    if not config.is_file():
        raise DetectionError("non_graph", "missing logseq/config.edn")
    try:
        values = EdnReader(config.read_text(encoding="utf-8")).read()
    except (OSError, UnicodeError, ValueError) as error:
        raise DetectionError("malformed_config", f"cannot read supported config EDN: {error}") from error
    if not isinstance(values, dict):
        raise DetectionError("malformed_config", "config.edn must contain a map")

    _, pages = _directory(root, values.get(":pages-directory", "pages"), ":pages-directory")
    _, journals = _directory(root, values.get(":journals-directory", "journals"), ":journals-directory")
    page_mode = values.get(":file/name-format", ":triple-lowbar")
    if page_mode != ":triple-lowbar":
        raise DetectionError("unsupported_filename_mode", "only :triple-lowbar page filenames are supported")
    journal_format = values.get(":journal/file-name-format", "yyyy_MM_dd")
    if journal_format not in {"yyyy_MM_dd", "yyyy-MM-dd"}:
        raise DetectionError("unsupported_journal_format", "journal filename format is unsupported")

    return GraphDescriptor(
        version=1,
        root=str(root),
        pages_directory=pages,
        journals_directory=journals,
        page_filename_mode=page_mode.removeprefix(":"),
        journal_filename_format=journal_format,
        evidence=("logseq/config.edn", pages, journals),
    )
