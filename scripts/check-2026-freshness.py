#!/usr/bin/env python3
"""
2026 model freshness check.

掃所有 .md 找 stale model references (Claude 3.5 / GPT-4o / Gemini 2.0 / etc.)
that lack a 'lineage' / '前身' / '歷史' qualifier within ±N lines context.

Config: scripts/freshness-models.yml (whitelist + stale pattern list)

Usage:
    python scripts/check-2026-freshness.py              # exit 1 on stale
    python scripts/check-2026-freshness.py --warn-only  # exit 0, prefix ::warning::

Exit codes:
    0 — no stale refs OR --warn-only mode
    1 — stale refs found in strict mode
"""

from __future__ import annotations

import argparse
import re
import sys
from fnmatch import fnmatch
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        '❌ PyYAML required. Install: pip install pyyaml',
        file=sys.stderr,
    )
    sys.exit(2)


EXCLUDE_DIRS = {'.ai', 'book', 'node_modules', '.git', 'archives', '.coord'}
EXCLUDE_MIRROR_SUFFIXES = ['.en.md', '.zh-Hans.md']  # focus on zh-TW canonical


def load_config(repo_root: Path) -> dict:
    cfg_path = repo_root / 'scripts' / 'freshness-models.yml'
    with open(cfg_path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def matches_exclude(path: Path, repo_root: Path, exclude_patterns: list[str]) -> bool:
    """Check if file path matches any exclude glob pattern."""
    rel = path.relative_to(repo_root).as_posix()
    for pat in exclude_patterns:
        if fnmatch(rel, pat) or fnmatch(rel + '/', pat):
            return True
    return False


def has_qualifier(
    lines: list[str], idx: int, terms: list[str], window: int
) -> bool:
    """Check if any qualifier term appears in ±window lines around idx."""
    start = max(0, idx - window)
    end = min(len(lines), idx + window + 1)
    context = ' '.join(lines[start:end])
    return any(q in context for q in terms)


def scan_file(
    path: Path,
    cfg: dict,
    repo_root: Path,
) -> list[tuple[Path, int, str, str, str]]:
    """
    Scan one file for stale model refs.

    Returns list of (file, line_no, matched_text, pattern, note).
    """
    findings: list[tuple[Path, int, str, str, str]] = []
    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')

    window = cfg.get('qualifier_context_lines', 2)

    # Check per-file context override
    rel = path.relative_to(repo_root).as_posix()
    for override in cfg.get('exclude_files_pattern_specific', []):
        if fnmatch(rel, override.get('file', '')):
            # Accept both new (qualifier_window) and legacy (skip_patterns_with_context)
            # field names for backward compat
            window = override.get(
                'qualifier_window',
                override.get('skip_patterns_with_context', window),
            )
            break

    # Check stale_patterns
    for entry in cfg.get('stale_patterns', []):
        pat_str = entry['pattern']
        try:
            pat = re.compile(pat_str)
        except re.error as e:
            print(f'⚠ Invalid regex in freshness-models.yml: {pat_str!r}: {e}', file=sys.stderr)
            continue
        terms = entry.get('qualifier_terms', [])
        note = entry.get('note', '')
        for idx, line in enumerate(lines):
            m = pat.search(line)
            if m and not has_qualifier(lines, idx, terms, window):
                findings.append((path, idx + 1, m.group(0), pat_str, note))

    # Check stale_date_phrases
    for entry in cfg.get('stale_date_phrases', []):
        pat_str = entry['pattern']
        try:
            pat = re.compile(pat_str)
        except re.error as e:
            print(f'⚠ Invalid regex: {pat_str!r}: {e}', file=sys.stderr)
            continue
        terms = entry.get('qualifier_terms', [])
        note = entry.get('note', '')
        for idx, line in enumerate(lines):
            m = pat.search(line)
            if m:
                # Date phrases either need qualifier OR no qualifier needed (different rule)
                if terms and has_qualifier(lines, idx, terms, window):
                    continue
                findings.append((path, idx + 1, m.group(0), pat_str, note))

    return findings


def should_skip(path: Path, repo_root: Path, cfg: dict) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    for suffix in EXCLUDE_MIRROR_SUFFIXES:
        if path.name.endswith(suffix):
            return True
    exclude_files = cfg.get('exclude_files', [])
    return matches_exclude(path, repo_root, exclude_files)


def main() -> int:
    # Force UTF-8 stdout
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--warn-only',
        action='store_true',
        help='Exit 0 even if stale refs found, print ::warning:: prefix',
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    cfg = load_config(repo_root)

    all_findings: list[tuple[Path, int, str, str, str]] = []
    for md in sorted(repo_root.rglob('*.md')):
        if should_skip(md, repo_root, cfg):
            continue
        try:
            all_findings.extend(scan_file(md, cfg, repo_root))
        except Exception as e:
            print(f'⚠ scan error {md.relative_to(repo_root)}: {e}', file=sys.stderr)

    if not all_findings:
        print('✓ No stale model references detected (against 2026 frontier whitelist).')
        return 0

    prefix = '::warning::' if args.warn_only else '❌ '
    for path, lineno, matched, pat, note in all_findings:
        rel = path.relative_to(repo_root).as_posix()
        print(f'{prefix}{rel}:{lineno}: stale "{matched}" — {note} [pattern: {pat}]')

    print(f'\nFound {len(all_findings)} stale model reference(s).')
    print(
        'Tip: add a qualifier ("前身" / "歷史" / "lineage" / "baseline" / "原始")'
        ' nearby to mark as historical reference.'
    )
    return 0 if args.warn_only else 1


if __name__ == '__main__':
    sys.exit(main())
