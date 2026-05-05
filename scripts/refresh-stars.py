#!/usr/bin/env python3
"""
refresh-stars.py — 用 `gh api` 把所有 GitHub repo 的星數抓最新值，比對 markdown 內標註的 `★ Xk+`。

用法：
    python scripts/refresh-stars.py              # 列出所有有變化的 entry
    python scripts/refresh-stars.py --threshold 20  # 只列差距 > 20% 的
    python scripts/refresh-stars.py --check      # 退出 code 1 如果任何 entry 過時超過門檻

環境需求：
    pip install requests
    PATH 上要有 `gh` (GitHub CLI) 並且已 `gh auth login`
"""

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_GLOB = "**/*.md"
EXCLUDE_DIRS = {".git", ".ai", "node_modules", "_build", ".venv"}

# 抓 GitHub repo URL：https://github.com/owner/repo
GITHUB_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+?)(?:[#?/)\s]|$)")
# 抓 markdown 內標註的 stars：`| Stars | ★ 12k+ |` 或 inline `★ 12k+`
STARS_RE = re.compile(r"★\s*([\d.]+)\s*([kKmM]?)\+?")

# 排除的假 / 範本 repo
PLACEHOLDER_REPOS = {
    "owner/repo",
    "example/repo",
    "your-org/your-repo",
    "user/repo",
}

# GitHub 上不是 repo 的特殊路徑（settings、marketplace、login 等）
NON_REPO_OWNERS = {
    "settings", "marketplace", "login", "logout", "join",
    "topics", "trending", "collections", "events", "explore",
    "issues", "pulls", "notifications", "search", "new",
    "organizations", "users", "blog", "about", "pricing",
    "features", "security", "enterprise", "customer-stories",
}

MAX_WORKERS = 10


def normalize_repo(owner: str, name: str) -> str | None:
    """正規化 repo identifier。回傳 None 表示應該跳過。"""
    # 去掉 .git 後綴
    name = name.removesuffix(".git")
    repo_id = f"{owner}/{name}"
    if repo_id in PLACEHOLDER_REPOS:
        return None
    # 排除 GitHub 上非 repo 的特殊路徑（settings/tokens 等）
    if owner in NON_REPO_OWNERS:
        return None
    # 如果 owner 或 name 太短 / 看起來不像真 repo，跳過
    if len(owner) < 1 or len(name) < 1:
        return None
    return repo_id


def find_md_files(root: Path) -> list[Path]:
    files = []
    for fp in root.glob(MD_GLOB):
        if any(part in EXCLUDE_DIRS for part in fp.parts):
            continue
        files.append(fp)
    return files


def parse_stars_text(s: str) -> int | None:
    """`12k+` -> 12000, `1.5k+` -> 1500"""
    m = STARS_RE.match(s)
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2).lower()
    if unit == "k":
        num *= 1000
    elif unit == "m":
        num *= 1_000_000
    return int(num)


def fetch_stars(repo: str) -> int | None:
    """gh api repos/<owner>/<repo>"""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq", ".stargazers_count"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None
        return int(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError):
        return None


def fmt_stars(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}m+"
    if n >= 10_000:
        return f"{n//1000}k+"
    if n >= 1_000:
        return f"{n/1000:.1f}k+".replace(".0k", "k")
    return str(n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=10,
                        help="只列出星數差距百分比超過此值的 entry（預設 10）")
    parser.add_argument("--check", action="store_true",
                        help="若有任何 entry 過時則退出 code 1")
    args = parser.parse_args()

    # 找所有 GitHub repo + 它在每個檔案中的標註 stars
    # entries: {repo: [(file_path, declared_stars_int, line_no, declared_text)]}
    entries: dict[str, list[tuple[Path, int | None, int, str]]] = {}

    for fp in find_md_files(REPO_ROOT):
        text = fp.read_text(encoding="utf-8")
        # 一個簡單的 state machine：找到 `[...](https://github.com/X/Y)`，
        # 然後在接下來 N 行裡找 `★ Xk+`
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m_repo = GITHUB_RE.search(line)
            if not m_repo:
                continue
            repo = normalize_repo(m_repo.group(1), m_repo.group(2))
            if repo is None:
                continue
            # 在接下來最多 12 行內找 stars。
            # 但若先碰到下一個 `### / #### / ## ` heading，就停（避免跨 entry 找錯）
            declared = None
            declared_text = None
            for j in range(i + 1, min(i + 12, len(lines))):
                stripped = lines[j].lstrip()
                if stripped.startswith(("### ", "#### ", "## ", "---", "# ")):
                    break  # 撞到下一個 entry 邊界
                m_stars = STARS_RE.search(lines[j])
                if m_stars:
                    declared = parse_stars_text(m_stars.group(0))
                    declared_text = m_stars.group(0)
                    break
            entries.setdefault(repo, []).append((fp, declared, i + 1, declared_text or "(no stars line)"))

    # 去重 repo（每個 repo 只查一次）
    unique_repos = list(entries.keys())
    print(f"Found {len(unique_repos)} unique GitHub repos referenced.", file=sys.stderr)
    print(f"Querying gh api...", file=sys.stderr)

    # 並行查 stars
    actual: dict[str, int | None] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(fetch_stars, r): r for r in unique_repos}
        for i, fut in enumerate(as_completed(futures), start=1):
            repo = futures[fut]
            actual[repo] = fut.result()
            if i % 10 == 0:
                print(f"  {i}/{len(unique_repos)}", file=sys.stderr)

    # 比對
    drift = []
    missing = []
    not_found = []

    for repo, occurrences in entries.items():
        latest = actual[repo]
        if latest is None:
            not_found.append(repo)
            continue

        for fp, declared, line_no, declared_text in occurrences:
            if declared is None:
                missing.append((repo, fp, line_no))
                continue

            if declared == 0:
                pct_diff = 100
            else:
                pct_diff = abs(latest - declared) / declared * 100

            if pct_diff >= args.threshold:
                drift.append((
                    repo, fp, line_no, declared, latest, pct_diff, declared_text
                ))

    # 報告
    print()
    print("=" * 60)
    print(f"Total repos checked:   {len(unique_repos) - len(not_found)}")
    print(f"Drift (>={args.threshold}%):     {len(drift)}")
    print(f"Missing stars line:    {len(missing)}")
    print(f"Repo not found (404):  {len(not_found)}")
    print()

    if drift:
        print("=== Drifted entries ===")
        for repo, fp, line_no, declared, latest, pct, text in sorted(drift, key=lambda x: -x[5]):
            rel = fp.relative_to(REPO_ROOT)
            arrow = "↑" if latest > declared else "↓"
            print(f"  {repo}  declared={text} actual={fmt_stars(latest)} "
                  f"(diff {arrow}{pct:.0f}%)  →  {rel}:{line_no}")

    if not_found:
        print()
        print("=== Repos not found / private / renamed ===")
        for repo in not_found:
            print(f"  {repo}")
            for fp, _, line_no, _ in entries[repo]:
                rel = fp.relative_to(REPO_ROOT)
                print(f"    {rel}:{line_no}")

    if args.check and (drift or not_found):
        # CI 模式：只有 drift 或 404 算失敗。
        # `missing` 是 by design（article / spec / catalog entry 不需要 Stars row，見 style-guide §1）
        sys.exit(1)


if __name__ == "__main__":
    main()
