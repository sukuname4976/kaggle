---
name: read-kaggle
description: Kaggle のページをヘッドレスブラウザ（Playwright）でレンダリングして本文テキストを読む。Kaggle は JS 描画で WebFetch だと中身が取れないため、overview・rules・discussion などを読むときに使う。
---

# read-kaggle スキル

Kaggle のページは JS で本文を描画するため WebFetch では中身が取れない。
このスキルは Playwright で実際にブラウザでページを開き、描画後のテキストを取る。
公開ページなら「人間がブラウザで見えるもの」と同じ内容が読める。

## 前提（初回のみ）

Chromium バイナリを1度だけ入れる（~150MB、`~/.cache/ms-playwright` に共有保存）。

```bash
uv run --with playwright --no-project --python 3.12 python -m playwright install chromium
```

## 使い方

```bash
uv run --with playwright --no-project --python 3.12 \
  python .claude/skills/read-kaggle/render.py <url> [css-selector]
```

- `<url>`: 読みたい Kaggle ページの URL
- `[css-selector]`: 省略可。指定するとその要素のテキストだけ出す（省略時は body 全体）

### 例: コンペ overview を読む

```bash
uv run --with playwright --no-project --python 3.12 \
  python .claude/skills/read-kaggle/render.py \
  https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/overview
```

discussion・rules・leaderboard なども同じく URL を渡すだけ。

## ログインが要るページ

データタブ（ルール同意後）や本人確認後のコンテンツは未ログインだと見れない。
その場合はログイン済みセッションの Cookie を Playwright に渡す必要がある
（`storage_state` 等）。実装は未対応。必要になったら追加する。

## 注意

- 出力は本文テキスト。表組みやコードブロックの整形は崩れることがある。
- ページによっては `networkidle` 待ちでタイムアウトすることがある（その場合も
  取得できた範囲を出力する）。
