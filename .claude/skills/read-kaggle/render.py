"""Kaggle など JS レンダリングのページを開いて、描画後のテキストを出力する。

Usage:
    uv run --with playwright --no-project --python 3.12 \
        python .claude/skills/read-kaggle/render.py <url> [css-selector]

第2引数に CSS セレクタを渡すと、その要素のテキストだけを出力する
（省略時は body 全体）。
"""

import sys

from playwright.sync_api import sync_playwright


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: render.py <url> [css-selector]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    selector = sys.argv[2] if len(sys.argv) > 2 else "body"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        # XHR でコンテンツが入るまで待つ（失敗しても続行）
        try:
            page.wait_for_load_state("networkidle", timeout=30000)
        except Exception:
            pass
        print(page.inner_text(selector))
        browser.close()


if __name__ == "__main__":
    main()
