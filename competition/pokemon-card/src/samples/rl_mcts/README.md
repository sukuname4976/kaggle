# Reinforcement Learning and MCTS sample

公式サンプルの強化学習 + MCTS 実装。Search API / Battle Start・Finish API の使用例も兼ねる。

- 出典: Kaggle ノートブック `kiyotah/reinforcement-learning-and-mcts-sample-code`
- 元ファイル: `*.ipynb`（オリジナル）/ `train.py`（抽出したコード）

## やっていること

- **Transformer 風のモデル**（自作 `MyModel`: EmbeddingBag + Encoder/Decoder）で、盤面の価値（value）と各手の方策（policy）を推定。
- **MCTS**（`mcts_agent`）でモデルを使いながら探索し、行動を選ぶ。同時に学習データも生成。
- **self-play**（自己対戦）でデータを集め、価値・方策を教師に**学習ループ**を回す。
- 学習したモデルは `out/modelN.pth` に保存。

## メモ

- これは**学習用スクリプト**で、そのまま提出物（`main.py`）ではない。提出するには学習済みモデルを読み込んで `agent(obs_dict) -> list[int]` を返す本体を別途用意する必要がある。
- `torch` 依存。GPU（CUDA）があれば自動で使う。
- 盤面のダメージ計算や手の実行結果を調べる **Search API**（`search_begin/step/end`）の実例として、ルールベース改良の参考にもなる。
