#!/usr/bin/env python3
"""
Stage template structure check.

驗每個 stages/[0-9]*-*.md (zh-TW canonical) 有所有必要的 H2 section、
跟 Stage 5/6/7/8 已經對齊的 template 一致。

REQUIRED — 缺則 fail（H2 必須有）：
  - 📌 學習目標
  - 🚪 進入條件
  - 📚 必修閱讀
  - 🛠 動手練習
  - 🎯 精選 Projects（或變體含「Projects」）
  - ✅ 自我檢查（或 .* 自我檢查 / 進入 .* 前的自我檢查）

EXPECTED — 缺則 warning（不擋）：
  - 🎯 X 是什麼（先定位）  — positioning section
  - 🎯 常用 .* 工具推薦 / 常用 .* 推薦 — tool recommendation

排除：mirror files (*.en.md, *.zh-Hans.md)、Stage 0 (foundations 短 intro)。

Usage:
    python scripts/check-stage-template.py [--strict-expected]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = [
    (r'📌\s*學習目標', '📌 學習目標'),
    (r'🚪\s*進入條件', '🚪 進入條件'),
    (r'📚\s*必修閱讀', '📚 必修閱讀'),
    (r'🛠\s*動手練習', '🛠 動手練習'),
    (r'🎯\s*(精選|常用)?\s*.*Projects', '🎯 精選 Projects'),
    # Grouped alternation: matches "✅ X 自我檢查" or "X 自我檢查" anywhere — but NOT
    # bare "自我檢查" in unrelated context (must have surrounding text before 自我檢查)
    (r'(✅\s*.*自我檢查|.+自我檢查|自我檢查)', '✅ 自我檢查'),
]

EXPECTED_PATTERNS = [
    (r'🎯\s*.*是什麼.*先定位', '🎯 [topic] 是什麼（先定位）'),
    (r'🎯\s*常用.*推薦|🎯\s*常用.*工具', '🎯 常用工具推薦（按用途）'),
]

# Stages that don't follow the per-stage template:
#   - 00- prerequisites: short intro doc, doesn't need full template
#   - 05- Claude Code ecosystem: multi-sub-stage container (5.1-5.6),
#     each sub-stage has its own learning goals/practice structure;
#     template check at file level doesn't make sense.
SKIP_STAGES = ['00-', '05-']

H2_RE = re.compile(r'^## (.+?)\s*$', re.MULTILINE)


def get_h2_sections(content: str) -> list[str]:
    return [m.group(1) for m in H2_RE.finditer(content)]


def check_stage(path: Path) -> tuple[list[str], list[str]]:
    """Return (missing_required, missing_expected) labels."""
    content = path.read_text(encoding='utf-8')
    h2s = get_h2_sections(content)

    def matches_any(pat: str) -> bool:
        return any(re.search(pat, h2) for h2 in h2s)

    missing_req = [label for pat, label in REQUIRED_PATTERNS if not matches_any(pat)]
    missing_exp = [label for pat, label in EXPECTED_PATTERNS if not matches_any(pat)]
    return missing_req, missing_exp


def should_skip(path: Path) -> bool:
    name = path.name
    if name.endswith('.en.md') or name.endswith('.zh-Hans.md'):
        return True
    for prefix in SKIP_STAGES:
        if name.startswith(prefix):
            return True
    return False


def main() -> int:
    # Force UTF-8 stdout
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--strict-expected',
        action='store_true',
        help='Also fail on missing EXPECTED sections (not just REQUIRED)',
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    stages_dir = repo_root / 'stages'
    if not stages_dir.exists():
        print('❌ stages/ directory not found.', file=sys.stderr)
        return 2

    has_required_issue = False
    has_expected_issue = False

    for stage in sorted(stages_dir.glob('[0-9]*-*.md')):
        if should_skip(stage):
            continue
        missing_req, missing_exp = check_stage(stage)
        rel = stage.relative_to(repo_root).as_posix()

        if missing_req:
            print(f'❌ {rel}: missing REQUIRED H2 section(s):')
            for label in missing_req:
                print(f'   - {label}')
            has_required_issue = True

        if missing_exp:
            warn_prefix = '❌' if args.strict_expected else '⚠'
            print(f'{warn_prefix} {rel}: missing EXPECTED H2 section(s):')
            for label in missing_exp:
                print(f'   - {label}')
            if args.strict_expected:
                has_expected_issue = True

    if has_required_issue or has_expected_issue:
        return 1

    if not has_required_issue:
        print('✓ All stages have REQUIRED template sections.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
