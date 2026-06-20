# データ取得手順

Simulation 部門のデータ（`input/`）を Kaggle API で取得する手順。
`input/` は `.gitignore` 済みでコミットされないため、クローン直後はこの手順で再取得する。

## 前提: Kaggle API トークン

1. <https://www.kaggle.com/settings> → API → **「Create New API Token」**。新形式トークン `KAGGLE_API_TOKEN=KGAT_...` が得られる。
2. **値（`KGAT_...` の部分）だけ**をファイルに保存し、権限を絞る:

   ```bash
   mkdir -p ~/.kaggle
   # トークン値を ~/.kaggle/access_token に1行で保存（エディタ等で）
   chmod 600 ~/.kaggle/access_token
   ```

   - トークンは**コミットしない**。実行時にファイルから環境変数へ読み込む（下記コマンド参照）。

## 前提: kaggle CLI

dev 依存に追加済み（`pyproject.toml`）。`uv run kaggle ...` で実行する。
未導入なら:

```bash
uv add --dev kaggle
```

## 前提: ルール同意（手動・必須）

<https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/rules> で **ルールに同意**する。
このコンペは**本人確認（電話番号認証）必須**。同意・認証が済んでいないと
ダウンロードは `403 Forbidden` になる（ファイル一覧の閲覧は同意前でも可）。

## ダウンロード

```bash
cd competition/pokemon-card
mkdir -p input
KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token)" \
  uv run kaggle competitions download -c pokemon-tcg-ai-battle -p input/
```

- `KAGGLE_API_TOKEN="$(cat ...)"` でトークンを画面に出さずに渡す。
- 約300MB の zip（`input/pokemon-tcg-ai-battle.zip`）が落ちる。

## 展開

```bash
cd input
unzip -o pokemon-tcg-ai-battle.zip && rm pokemon-tcg-ai-battle.zip
```

## 取得物

展開後の構成は [simulation.md の「補足」](simulation.md) を参照。
主なもの: `EN_Card_Data.csv` / `JP_Card_Data.csv`、カード一覧 PDF、
`sample_submission/`（エンジン `cg/` + `deck.csv` + `main.py`）。

## 参考: 任意ファイルだけ取得

ファイル一覧と単体取得:

```bash
KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token)" \
  uv run kaggle competitions files -c pokemon-tcg-ai-battle
KAGGLE_API_TOKEN="$(cat ~/.kaggle/access_token)" \
  uv run kaggle competitions download -c pokemon-tcg-ai-battle -f EN_Card_Data.csv -p input/
```
