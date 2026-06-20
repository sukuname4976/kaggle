# 概要

## 全体概要

「The Pokémon Company - PTCG AI Battle Challenge」。ポケモンカードゲームを自動でプレイする AI を競うチャレンジ。1つのチャレンジが2つの Kaggle コンペ（部門）に分かれている。

- **Simulation 部門**: AI エージェントを作って自動対戦し、勝率（レーティング）を競う。実装勝負。賞金なし（ポイント・メダルのみ）。
- **Strategy 部門（Hackathon）**: 戦略を説明する Writeup を提出し、人が審査する。賞金 $240,000 はこちら。

両部門は連結しており、Strategy に参加するには Simulation への参加が必須。エージェントの実装は Simulation 側、その説明レポートが Strategy 側にあたる。

- 開始: 2026-06-16 11:00 UTC（両部門共通）
- チーム最大5人

## ストラテジー

- 正式名: The Pokémon Company - PTCG AI Battle Challenge Strategy
- 提出: Kaggle Writeup（レポート。タイトル・サブタイトル・分析を含む。Track 選択、**2000語以内**）＋ Media Gallery（画像・動画）
- 評価: Model Score 70% / Deck Score 20% / Report Score 10%
- 賞: ファイナリスト8名に各 $30,000（計 $240,000）。東京での対面トーナメント招待の可能性あり
- 参加条件: Simulation 部門への参加が必須
- 締切: 参加・ルール同意 2026-09-06 / 最終提出 2026-09-13 / 審査 2026-09-14〜10-11

## シミュレーション

- 正式名: The Pokémon Company - PTCG AI Battle Challenge Simulation
- 提出: `.tar.gz`（トップ階層に `main.py` と `deck.csv` を含める）
- 評価: 自動対戦のスキルレーティング（ガウス分布）。**1日最大5提出**、最新2つが評価対象
- 賞金: なし（Knowledge コンペ。ポイント・メダルのみ）
- 環境: cabt Engine（kaggle-environments ベースの対戦シミュレータ、SDK 提供）。API ドキュメント: <https://matsuoinstitute.github.io/cabt/>
- 締切: 参加・ルール同意 2026-08-09 / 最終提出 2026-08-16 / リーダーボード確定 〜約08-31
