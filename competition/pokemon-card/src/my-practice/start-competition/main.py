"""ルカリオデッキの最初の練習エージェント。

方針はシンプルに「基本ルールに沿って素直に動く」だけ:

1. 手番(MAIN)では、まず場を整える行動(特性 → 進化 → エネルギー → カードを出す)を
   済ませてから攻撃し、何も無ければターンを終える。
2. それ以外の選択(最初に出すポケモン、捨てるカード等)は、合法な選択肢の先頭を選ぶ。

ランダムではなく「準備してから殴る」という最低限の戦略を持たせている。
どの技・どのカードが最善かまでは見ておらず、改善の余地は多い。
"""

import os

from cg.api import Observation, OptionType, SelectContext, to_observation_class

# MAIN フェーズでの行動優先度(大きいほど先に選ぶ)。
# 「場を整えてから攻撃し、最後にターン終了」という基本の流れを表す。
MAIN_PRIORITY = {
    OptionType.ABILITY: 6,  # 特性は基本的に使う
    OptionType.EVOLVE: 5,   # 進化できるなら進化する
    OptionType.ATTACH: 4,   # エネルギーを付ける(攻撃の準備)
    OptionType.PLAY: 3,     # 手札のポケモン・カードを場に出す
    OptionType.ATTACK: 2,   # 準備が済んだら攻撃する
    OptionType.RETREAT: 1,  # 逃げは消極的なので低め
    OptionType.END: 0,      # 何も無ければターン終了
}


def read_deck_csv() -> list[int]:
    """deck.csv(カードID 60行)を読む。提出時は /kaggle_simulations/agent/ から読む。"""
    path = "deck.csv"
    if not os.path.exists(path):
        path = "/kaggle_simulations/agent/" + path
    with open(path) as f:
        return [int(line) for line in f if line.strip()][:60]


def agent(obs_dict: dict) -> list[int]:
    obs: Observation = to_observation_class(obs_dict)

    # 初手はデッキ(60枚のカードID)を返す
    if obs.select is None:
        return read_deck_csv()

    select = obs.select
    options = select.option

    # 手番(MAIN): 優先度が最も高い行動を1つ選ぶ
    if select.context == SelectContext.MAIN:
        priorities = [MAIN_PRIORITY.get(o.type, -1) for o in options]
        return [priorities.index(max(priorities))]

    # それ以外の選択: 合法な選択肢の先頭から必要数を選ぶ(最低限の素直な選択)
    return list(range(select.maxCount))
