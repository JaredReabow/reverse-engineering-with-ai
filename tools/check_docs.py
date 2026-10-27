#!/usr/bin/env python3
"""Validate this public research repository without network or device access.

Checks are intentionally bounded to the repository's plain Markdown dialect and
explicit publication inventory. They are not a full Markdown parser, a complete
secret scanner, or technical validation of the research claims.
"""

import argparse
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit


DOCS_ROOT = Path(__file__).resolve().parents[1]
DOCS_ALLOWED = {
    ".gitignore", "AGENTS.md", "CHANGELOG.md", "HISTORY.md", "README.md",
    "docs/ai-collaboration.md", "docs/evidence-framework.md", "docs/methods.md",
    "docs/public-source-case-studies.md", "docs/sources.md", "docs/workflow.md",
    "templates/investigation.md", "tools/check_docs.py",
}
DOCS_SKIP_DIRS = {".git", "__pycache__", ".venv"}
DOCS_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)")
DOCS_SENSITIVE = (
    ("private key block", re.compile(r"-----BEGIN (?:(?:RSA|EC|OPENSSH) )?PRIVATE KEY-----")),
    ("GitHub credential", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained credential", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("common API credential", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b")),
    ("local user directory", re.compile(r"/(?:Users|home)/[^\s/]+")),
    ("internal chat identifier", re.compile(r"(?:threadId|thread_id|rollout_path)\s*[:=]")),
)


def docs_inventory(root):
    """Return UTF-8 publication files and errors without following symlinks."""
    files, errors = {}, []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in DOCS_SKIP_DIRS for part in relative.parts):
            continue
        label = relative.as_posix()
        if path.is_symlink():
            errors.append(f"{label}: symlinks are outside the publication inventory")
            continue
        if not path.is_file():
            continue
        if label not in DOCS_ALLOWED:
            errors.append(f"{label}: unexpected publication file")
            continue
        if path.stat().st_size > 200_000:
            errors.append(f"{label}: unexpectedly large publication file")
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            errors.append(f"{label}: cannot read as UTF-8 ({type(exc).__name__})")
            continue
        if "\x00" in body:
            errors.append(f"{label}: binary content")
            continue
        files[label] = body
    for label in sorted(DOCS_ALLOWED - files.keys()):
        errors.append(f"{label}: required file missing or unreadable")
    return files, errors


def docs_without_code(body):
    """Remove fenced blocks so command examples are not interpreted as links."""
    return re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", body)


def docs_anchors(body):
    """Build anchors for the simple ATX headings used in this repository."""
    anchors, counts = set(), {}
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", docs_without_code(body)):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def docs_links(root, files):
    """Check relative targets and anchors, and validate external URL shape."""
    errors, count = [], 0
    for name, body in files.items():
        if not name.endswith(".md"):
            continue
        for target in DOCS_LINK.findall(docs_without_code(body)):
            count += 1
            parsed = urlsplit(target)
            if parsed.scheme:
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    errors.append(f"{name}: unsupported or credential-bearing URL")
                continue
            if parsed.netloc or parsed.path.startswith("/") or parsed.query:
                errors.append(f"{name}: invalid local link {target}")
                continue
            resolved = ((root / name).parent / unquote(parsed.path)).resolve() if parsed.path else root / name
            try:
                relative = resolved.relative_to(root.resolve()).as_posix()
            except ValueError:
                errors.append(f"{name}: link escapes repository")
                continue
            if relative not in files:
                errors.append(f"{name}: missing local link target {target}")
            elif parsed.fragment and unquote(parsed.fragment) not in docs_anchors(files[relative]):
                errors.append(f"{name}: missing local anchor {target}")
    return errors, count


def docs_privacy(files):
    """Flag selected accidental-publication patterns without printing matches."""
    errors = []
    for name, body in files.items():
        # Patterns and synthetic negative fixtures in the checker are not data.
        # Review that one source file directly before publication.
        if name == "tools/check_docs.py":
            continue
        for label, pattern in DOCS_SENSITIVE:
            if pattern.search(body):
                errors.append(f"{name}: possible {label}")
    return errors


def docs_structure(files):
    """Check method coverage, source-index coverage, and version records."""
    errors = []
    methods = re.findall(r"\| \*\*(\d+)\. ", files.get("docs/methods.md", ""))
    if methods != [str(number) for number in range(1, 32)]:
        errors.append("docs/methods.md: expected methods 1 through 31 exactly once in order")
    referenced = set()
    for name, body in files.items():
        if name.endswith(".md") and name != "docs/sources.md":
            referenced.update(link for link in DOCS_LINK.findall(body) if link.startswith("https://"))
    indexed = set(DOCS_LINK.findall(files.get("docs/sources.md", "")))
    for url in sorted(referenced - indexed):
        errors.append(f"docs/sources.md: missing referenced URL {url}")
    readme = files.get("README.md", "")
    version = re.search(r"Current documentation version: \*\*(\d+\.\d+\.\d+)\*\*", readme)
    if not version:
        errors.append("README.md: documentation version missing")
    else:
        for name in ("CHANGELOG.md", "HISTORY.md"):
            if version.group(1) not in files.get(name, ""):
                errors.append(f"{name}: current version missing")
    for name, body in files.items():
        if name.endswith(".md"):
            if not body.startswith("# "):
                errors.append(f"{name}: document title missing")
            if body.count("\n```") % 2:
                errors.append(f"{name}: unbalanced code fences")
            if "\ue200" in body or "<oai-mem-citation>" in body:
                errors.append(f"{name}: internal citation markup")
    return errors, len(referenced)


def docs_self_test():
    """Use controlled defects to confirm broken links and unsafe inputs fail."""
    checks = 0
    with tempfile.TemporaryDirectory(prefix="research-docs-check-") as folder:
        root = Path(folder)
        samples = {"README.md": "# Start\n\n[valid](docs/page.md#target)\n", "docs/page.md": "# Target\n"}
        assert not docs_links(root, samples)[0]
        checks += 1
        for target in ("missing.md", "docs/page.md#absent", "../outside.md", "https://name:secret@example.com/file"):
            broken = dict(samples, **{"README.md": f"# Start\n\n[broken]({target})\n"})
            assert docs_links(root, broken)[0], target
            checks += 1
        for body in ("gh" + "p_" + "A" * 36, "/" + "Users" + "/example/private", "-----BEGIN " + "PRIVATE KEY-----"):
            assert docs_privacy({"README.md": body})
            checks += 1
        assert not docs_privacy({"README.md": "# Safe\n\nA public methodology guide.\n"})
        checks += 1
        for name in DOCS_ALLOWED:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Fixture\n", encoding="utf-8")
        assert not docs_inventory(root)[1]
        checks += 1
        (root / "unexpected.bin").write_bytes(b"\x00\x01")
        assert any("unexpected publication" in error for error in docs_inventory(root)[1])
        checks += 1
        (root / "unexpected.bin").unlink()
        (root / "README.md").unlink()
        (root / "README.md").symlink_to(root / "HISTORY.md")
        assert any("symlink" in error for error in docs_inventory(root)[1])
        checks += 1
    print(f"PASS: {checks} controlled positive and negative validation checks")


def docs_main():
    """Run all local checks, or their synthetic regression fixtures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run controlled validation fixtures")
    args = parser.parse_args()
    if args.self_test:
        docs_self_test()
        return 0
    files, errors = docs_inventory(DOCS_ROOT)
    link_errors, link_count = docs_links(DOCS_ROOT, files)
    structure_errors, source_count = docs_structure(files)
    errors.extend(link_errors + structure_errors + docs_privacy(files))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} publication files; {link_count} links; 31 methods; {source_count} indexed source URLs")
    print("PASS: version records, local anchors, text-only inventory and selected privacy checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(docs_main())
