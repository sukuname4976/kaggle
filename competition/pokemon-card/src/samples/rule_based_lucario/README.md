# Rule-Based Agent — Mega Lucario ex Deck

公式サンプル（最多票）のルールベースエージェント。

- 出典: Kaggle ノートブック `kiyotah/a-sample-rule-based-agent-mega-lucario-ex-deck`
- 元ファイル: `*.ipynb`（オリジナル）/ `main.py`（抽出した提出本体）

## やっていること

- **機械学習なし**の完全なルールベース（ヒューリスティック）。
- `agent(obs_dict) -> list[int]` で、エンジンが渡す**合法手 `select.option` 全部に点数を付けて、上位を選ぶ**。
- 場面（`SelectContext`）と選択肢の種類（攻撃 / エネルギー付け / 進化 / 手札選び など）ごとに、手書きルールで加点・減点。
- 毎ターン `AttackPlan` を計算: 自分×相手×技を総当たりし、弱点・抵抗・与ダメ・取れるサイド数から**最良の攻撃**を決める。
- デッキ（60枚のカードID）は冒頭でハードコード＋`deck.csv` から読み込み。

## メモ

- 実行には `deck.csv`（カードID 60行）が別途必要（このフォルダには未取得）。
- 提出物は `main.py` + エンジン `cg` + `deck.csv` を `tar.gz` に固める（パッケージ化処理は元 `.ipynb` の最後のセル、Kaggle 環境前提）。
