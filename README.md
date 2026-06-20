# kaggle

Kaggle コンペティション用のコード・ノートブック・実験管理リポジトリ。

## 概要

参加した Kaggle コンペごとに、データ処理・モデル学習・推論・実験記録をまとめています。

## ディレクトリ構成

```
.
├── competitions/   # コンペごとのディレクトリ
│   └── <competition-name>/
│       ├── notebooks/   # EDA・実験用ノートブック
│       ├── src/         # 学習・推論スクリプト
│       ├── input/        # データ（Git管理外）
│       └── output/       # 提出ファイル・モデル（Git管理外）
└── README.md
```

## セットアップ

```bash
# 仮想環境の作成（例: venv）
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## メモ

- `input/` や大容量データ、モデルの重みは `.gitignore` で除外しています。
- Kaggle API を使う場合は `~/.kaggle/kaggle.json` に認証情報を配置してください。
