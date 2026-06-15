#!/usr/bin/env python3
"""Minimal Mermaid compliance checker for diagram-spec-kit.

This linter enforces core rules from diagram-spec.yaml and
checklists/review-checklist.md for shared diagrams under docs/diagrams/.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_ROOT = ROOT / "docs" / "diagrams"
SPEC_PATH = ROOT / "diagram-spec.yaml"
CHECKLIST_PATH = ROOT / "checklists" / "review-checklist.md"

DEFAULT_NODE_ID_REGEX = r"^[a-z0-9]+(-[a-z0-9]+)*$"
DEFAULT_MAX_NODES = 15
DEFAULT_FORBIDDEN_EDGE_LABELS = {"handle", "process", "do stuff"}
DISALLOWED_TOKENS = ["style", "classDef", "click", "img:", "icon:", "%%{ }%%"]
ALLOWED_DECLARATIONS = ("flowchart LR", "sequenceDiagram")
ALLOWED_FLOWCHART_ARROWS = ("-->", "-.->", "--x")
ALLOWED_SEQUENCE_ARROWS = ("->>", "-->>", "-)", "--x")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_spec_values(spec_text: str) -> tuple[str, int, set[str]]:
    node_id_regex = DEFAULT_NODE_ID_REGEX
    max_nodes = DEFAULT_MAX_NODES
    forbidden_labels = set(DEFAULT_FORBIDDEN_EDGE_LABELS)

    node_match = re.search(r"node_id_regex:\s*\"([^\"]+)\"", spec_text)
    if node_match:
        node_id_regex = node_match.group(1)

    max_match = re.search(r"max_nodes_per_diagram:\s*(\d+)", spec_text)
    if max_match:
        max_nodes = int(max_match.group(1))

    label_block = re.search(
        r"forbidden_edge_labels:\s*((?:\n\s*-\s*.+)+)",
        spec_text,
        flags=re.MULTILINE,
    )
    if label_block:
        forbidden_labels = {
            line.strip().lstrip("-").strip().strip('"').strip("'").lower()
            for line in label_block.group(1).splitlines()
            if line.strip().startswith("-")
        }

    return node_id_regex, max_nodes, forbidden_labels


def _find_diagram_files() -> list[Path]:
    if not DIAGRAM_ROOT.exists():
        return []

    files = list(DIAGRAM_ROOT.rglob("*.mmd")) + list(DIAGRAM_ROOT.rglob("*.md"))
    return sorted({path for path in files if path.is_file()})


def _find_changed_diagram_files(base_ref: str) -> list[Path]:
    """Return changed diagram files compared with base_ref...HEAD."""
    cmd = ["git", "diff", "--name-only", f"{base_ref}...HEAD"]
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        fallback_cmd = ["git", "diff", "--name-only", "HEAD~1...HEAD"]
        result = subprocess.run(
            fallback_cmd,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    if result.returncode != 0:
        return []

    files: list[Path] = []
    for raw in result.stdout.splitlines():
        rel = raw.strip().replace("\\", "/")
        if not rel:
            continue
        if not rel.startswith("docs/diagrams/"):
            continue
        if not (rel.endswith(".mmd") or rel.endswith(".md")):
            continue
        candidate = ROOT / Path(rel)
        if candidate.is_file():
            files.append(candidate)

    return sorted(set(files))


def _first_declaration(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("---"):
            continue
        if stripped.startswith("flowchart") or stripped.startswith("sequenceDiagram"):
            return stripped
    return None


def _contains_scope_boundary(text: str, declaration: str) -> bool:
    if declaration.startswith("flowchart"):
        return "subgraph " in text
    if declaration.startswith("sequenceDiagram"):
        return bool(re.search(r"^\s*box\s+", text, flags=re.MULTILINE))
    return False


def _node_ids_flowchart(text: str) -> set[str]:
    ids: set[str] = set()
    pattern = re.compile(
        r"^\s*([A-Za-z0-9_-]+)\s*(?:\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}|\(\([^\)]*\)\))",
        flags=re.MULTILINE,
    )
    for match in pattern.finditer(text):
        ids.add(match.group(1))
    return ids


def _labeled_edges(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"\|([^|]+)\|", text)]


def _validate_mermaid_syntax(text: str) -> list[str]:
    """Check for common Mermaid parse errors."""
    errors: list[str] = []
    
    # Check for self-closing HTML tags (invalid in Mermaid)
    if "<br/>" in text:
        errors.append("contains invalid HTML tag <br/> (use <br> without slash)")
    if "<hr/>" in text:
        errors.append("contains invalid HTML tag <hr/> (use <hr> without slash)")
    if "<img/>" in text:
        errors.append("contains invalid HTML tag <img/> (use img: prefix instead)")
    
    # Check for <br> in sequence diagram labels (not supported, unlike flowcharts)
    if "sequenceDiagram" in text:
        # Look for <br> in labels: ->>|...<br>...|
        br_labels = re.findall(r'\|[^|]*<br[^|]*\|', text)
        if br_labels:
            errors.append("sequence diagram labels do not support <br> tags - use dash or colon separators instead")
        
        # Look for unquoted labels in sequence diagrams (must use quotes for text with special chars)
        # Pattern: ->>|text without quotes| or -->>|text|, etc.
        # But allow: ->>|"text"| and ->>|"text with, commas"|
        unquoted = re.findall(r'(?:->>|-->>|-\)|--x)\|(?!")', text)
        if unquoted:
            errors.append("sequence diagram labels must be quoted (use |\"label text\"|)")
        
        # Look for parentheses: ->>|"...(...)"|
        paren_labels = re.findall(r'\|"[^"]*\([^"]*\|', text)
        if paren_labels:
            errors.append("sequence diagram labels cannot contain parentheses () - use plain descriptive text")
        # Look for braces: ->>|"...{...}"|
        brace_labels = re.findall(r'\|"[^"]*\{[^"]*\|', text)
        if brace_labels:
            errors.append("sequence diagram labels cannot contain braces {} - use plain descriptive text")
        
        # Look for dashes as separators in labels (can cause parse errors)
        dash_labels = re.findall(r'\|"[^"]*\s-\s[^"]*"\|', text)
        if dash_labels:
            errors.append("sequence diagram labels should avoid dashes as separators - use simple descriptive text")
    
    return errors


def _validate_arrows(text: str, declaration: str) -> list[str]:
    errors: list[str] = []
    if declaration.startswith("flowchart"):
        edge_lines = [ln for ln in text.splitlines() if "-->" in ln or "-.->" in ln or "--x" in ln]
        for line in edge_lines:
            if not any(token in line for token in ALLOWED_FLOWCHART_ARROWS):
                errors.append(f"uses non-approved flowchart arrow in line: {line.strip()}")
    elif declaration.startswith("sequenceDiagram"):
        arrow_hits = re.findall(r"(?:->>|-->>|-\)|--x)", text)
        if not arrow_hits:
            errors.append("has no recognized sequence arrows")
    return errors


def lint_file(path: Path, node_id_regex: str, max_nodes: int, forbidden_labels: set[str]) -> list[str]:
    errors: list[str] = []
    text = _read_text(path)

    declaration = _first_declaration(text)
    if declaration is None:
        return ["missing Mermaid declaration"]

    if not any(declaration.startswith(x) for x in ALLOWED_DECLARATIONS):
        errors.append("uses unsupported declaration (allowed: flowchart LR or sequenceDiagram)")

    if declaration.startswith("flowchart") and declaration != "flowchart LR":
        errors.append("flowchart direction must be LR")

    # Validate Mermaid syntax early to catch parse errors
    syntax_errors = _validate_mermaid_syntax(text)
    errors.extend(syntax_errors)

    if not re.search(r"^\s*title\s*:\s*.+$", text, flags=re.MULTILINE):
        errors.append("missing title in frontmatter")

    if not re.search(r"legend", text, flags=re.IGNORECASE):
        errors.append("missing legend section or legend comment")

    if not _contains_scope_boundary(text, declaration):
        errors.append("missing scope boundary (use subgraph for flowchart or box for sequence)")

    for token in DISALLOWED_TOKENS:
        if token in text:
            errors.append(f"contains disallowed token: {token}")

    labels = _labeled_edges(text)
    if not labels:
        errors.append("edge labels are missing (use verb phrases in |label|)")

    for label in labels:
        if label.lower() in forbidden_labels:
            errors.append(f"uses forbidden edge label: {label}")

    if declaration.startswith("flowchart"):
        ids = _node_ids_flowchart(text)
        if len(ids) > max_nodes:
            errors.append(f"diagram has {len(ids)} nodes; max is {max_nodes}")

        compiled = re.compile(node_id_regex)
        invalid = sorted(node_id for node_id in ids if not compiled.match(node_id))
        if invalid:
            errors.append("non-kebab-case node IDs: " + ", ".join(invalid))

    errors.extend(_validate_arrows(text, declaration))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Mermaid diagrams for team spec compliance")
    parser.add_argument(
        "--changed",
        action="store_true",
        help="lint only files changed versus base ref",
    )
    parser.add_argument(
        "--base",
        default="origin/main",
        help="base ref used with --changed (default: origin/main)",
    )
    args = parser.parse_args()

    spec_text = _read_text(SPEC_PATH) if SPEC_PATH.exists() else ""
    _ = _read_text(CHECKLIST_PATH) if CHECKLIST_PATH.exists() else ""
    node_id_regex, max_nodes, forbidden_labels = _extract_spec_values(spec_text)

    if args.changed:
        diagram_files = _find_changed_diagram_files(args.base)
    else:
        diagram_files = _find_diagram_files()

    if not diagram_files:
        if args.changed:
            print("diagram-lint: no changed diagram files found, skipping")
        else:
            print("diagram-lint: no files found under docs/diagrams, skipping")
        return 0

    total_errors = 0
    for file_path in diagram_files:
        rel = file_path.relative_to(ROOT)
        errors = lint_file(file_path, node_id_regex, max_nodes, forbidden_labels)
        if errors:
            total_errors += len(errors)
            print(f"\nFAIL: {rel}")
            for idx, err in enumerate(errors, 1):
                print(f"  {idx}. {err}")
        else:
            print(f"PASS: {rel}")

    if total_errors:
        print(f"\ndiagram-lint: failed with {total_errors} issue(s)")
        return 1

    print("\ndiagram-lint: all diagrams passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
