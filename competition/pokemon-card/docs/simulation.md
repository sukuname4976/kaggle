# シミュレーション詳細

Simulation 部門（`pokemon-tcg-ai-battle`）の前提・ルール・環境のまとめ。
出典は公式 overview と cabt Engine ドキュメント（<https://matsuoinstitute.github.io/cabt/>）。

## 概要

ポケモンカードゲーム（PTCG）を自動でプレイする AI エージェントを作り、自動対戦で
競う部門。学習・テスト用のシミュレータ（SDK）が提供され、Kaggle の対戦環境と同じ
ロジックなのでローカルでのデバッグや強化学習に使える。

## ゲームの特徴（難しさ）

- **不完全情報**: 相手の手札やデッキの中身が分からない。これが core challenge。
- **ランダム性**: カードドロー、コイントスなどの確率要素。
- **多様性**: 多数のポケモンタイプ・カード組み合わせ・デッキ構成があり、同じ試合は2つとない。
- ルールベースのみでは上位は難しく、先読み・リアルタイム適応・最適な意思決定が要る。

## 評価・ランキング方式

- 1チームあたり**1日最大5エージェント**を提出できる。
- 提出エージェントはラダー上の**近いレーティングの相手**と Episode（対戦）を繰り返す。
- スキルレーティングはガウス分布 N(μ, σ²) でモデル化。μ=推定スキル、σ=不確実性（時間とともに減少）。初期値 **μ₀ = 600**。
- アップロード時にまず**自己対戦のバリデーション Episode** を実行。失敗すると Error 扱い（ログDL可）。
- Episode 終了ごとに参加エージェントの μ を更新（勝ち→μ増、負け→μ減、引き分け→平均へ寄せる）。更新幅は期待結果からの乖離と σ に比例。**勝敗の点差はレーティングに影響しない**。
- リーダーボードには**自分の最高スコアのエージェント**のみ表示。全提出の進捗は Submissions ページで追える。
- 最終評価は**最新2提出**を対象にする。
- 締切（2026-08-16）後は新規提出ロック。そこから約2週間（〜08-31頃、収束まで）対戦を継続してリーダーボード確定。

## 環境（cabt Engine）

- `kaggle-environments` 向けに作られた PTCG 対戦シミュレータ。環境名は `cabt`。
- 公式 PTCG ルールとシミュレータ挙動には**いくつか差異**がある（要・ドキュメント確認）。
- エンジンは常に**合法手のみ**を提示する。
- 参考: kaggle-environments 1.14.10 時点のコード／設定（<https://github.com/Kaggle/kaggle-environments>）。

## エージェントの書き方

各手番で observation（dict）を受け取り、選んだ選択肢の**インデックスのリスト**を返す。

```python
def agent(obs_dict: dict) -> list[int]:
    # select.option の中から maxCount 個のインデックスを返す
    return random.sample(
        list(range(len(obs_dict["select"]["option"]))),
        obs_dict["select"]["maxCount"],
    )
```

### observation の構造

- `logs`: イベント履歴・過去の行動
- `current`: 盤面状態（各プレイヤーの状態、ターン情報、スタジアムカード）。デッキ選択中は `None` のことがある
- `select`: 選択肢。option のインデックスが行動に対応。初期セットアップ中は `None` のことがある

プレイヤー情報の主な中身: バトル場のポケモン、ベンチ、手札、サイド、トラッシュ、状態異常。

## 提出形式

- `.tar.gz` バンドル。**トップ階層に `main.py`**（ネスト不可）と **`deck.csv`** を含める。
- 作成例: `tar -czvf submission.tar.gz *`
- My Submissions タブからアップロード。最初に自己対戦が走って正常動作を確認後、マッチメイクのプールに入る。

### deck.csv

- カードID を**60行**（1行1ID）。
- カードIDは `all_card_data()` で確認できる。

## ローカル実行

```python
from kaggle_environments import make
from agent import agent

with open("deck.csv") as f:
    deck = [int(line) for line in f.readlines() if line.strip()]

env = make("cabt", configuration={"decks": [deck, deck]})
env.run([agent, agent])

with open("result.html", "w") as f:
    f.write(env.render(mode="html"))
```

- インストール: `kaggle-environments`（`cabt` 環境を含む）

## スケジュール

- 開始: 2026-06-16 11:00 UTC
- 参加・ルール同意 / チーム合流締切: 2026-08-09
- 最終提出: 2026-08-16
- 対戦継続・リーダーボード確定: 2026-08-17 〜 約08-31

## 補足（公式データで確認済み）

データ一式は `input/`（gitignore 済み）に取得済み。詳細は実ファイル参照。

### カードデータ

- `input/EN_Card_Data.csv` / `JP_Card_Data.csv`（約2100種）。列: Card ID, Name, Stage/Type, HP, Type, Weakness, Resistance, Retreat, Move, Cost, Damage, Effect ほか。
- 全カード一覧 PDF: `input/Card_ID List_EN.pdf` / `_JP.pdf`。
- プログラムからは `all_card_data()` / `all_attack()` で取得（→ `CardData` / `Attack`）。

### エントリポイント / 提出

- 最小サンプル: `input/sample_submission/main.py`。`agent(obs_dict) -> list[int]` を定義するだけ。
- `deck.csv` の読み先: ローカルは同階層、提出時は `/kaggle_simulations/agent/deck.csv`。
- 返り値の制約: 各要素は `0 <= x < len(option)`、長さは `minCount <= len <= maxCount`、重複不可。初手（`select == None`）は60枚デッキIDを返す。
- `deck.csv` = カードID を60行。サンプル: `input/sample_submission/deck.csv`。

### observation / select スキーマ

**完全な定義は `input/sample_submission/cg/api.py`**（dataclass + Enum）。要点のみ:

- `Observation` = `select`(SelectData|None) / `logs`(list[Log]) / `current`(State|None)。初手は select・current が None。
- `State` = turn, yourIndex, firstPlayer, supporterPlayed, energyAttached, result, stadium, players[2]。
- `PlayerState` = active, bench, deckCount, discard, prize, handCount, hand(自分のみ), 状態異常(poisoned 等)。
- `SelectData` = type(SelectType), context(SelectContext), minCount/maxCount, option(list[Option])。
- `Option` は `type`(OptionType) により使うフィールドが変わる（area/index/inPlayArea/attackId/cardId など）。
- 主要 Enum: AreaType / EnergyType / CardType / SelectType / `SelectContext`（場面、0〜48）/ OptionType / LogType。
- 注意: Enum・各クラスは**競技中に要素が追加されうる**（api.py に明記）。

### ルール差異・勝敗理由

- 公式 PTCG とシミュの差異は cabt ドキュメント参照: <https://matsuoinstitute.github.io/cabt/>
- 勝敗理由（`LogType.RESULT` の reason）: 1=サイド0枚 / 2=山札0枚でターン開始 / 3=バトル場にポケモン無し / 4=カード効果。

### バージョン / 実行環境

- 公式参照は kaggle-environments 1.14.10。本リポジトリは **1.30.1** を導入済み（`cabt` 環境同梱）。
- 同梱エンジンは `libcg.so`(Linux) / `cg.dll`(Windows) のみ。**macOS 用バイナリは無く、ローカル実行は Docker(linux/amd64) 必須**。
- Search API（`search_begin/step/end`）で「この手を選んだらどうなるか」を先読み可能（`cg/api.py` 参照）。
