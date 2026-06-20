---
name: read-kaggle
description: Kaggle のコンペ情報や discussion を、ブラウザなし（curl + XSRF トークン）で内部 JSON API から読む。Kaggle ページが JS レンダリングで WebFetch だと本文が取れないときに使う。
---

# read-kaggle スキル

Kaggle のページは JS で本文を描画するため WebFetch では中身が取れない。
このスキルは Kaggle の内部 JSON API を直接叩いて構造化データを取得する。

## 仕組み

1. Kaggle のページに GET すると `XSRF-TOKEN` Cookie が返る
2. その値を `x-xsrf-token` ヘッダに付けて `https://www.kaggle.com/api/i/<endpoint>` に POST
3. JSON が返る

この一連を `fetch.sh` がやる。

## 使い方

```bash
bash .claude/skills/read-kaggle/fetch.sh <competition-name> <endpoint> '[json-body]'
```

読みやすく整形するなら末尾に `| python3 -m json.tool` を付ける。

## 確認済みエンドポイント

### コンペのメタデータ

```bash
bash .claude/skills/read-kaggle/fetch.sh \
  pokemon-tcg-ai-battle-challenge-strategy \
  competitions.CompetitionService/GetCompetition \
  '{"competitionName":"pokemon-tcg-ai-battle-challenge-strategy"}' | python3 -m json.tool
```

返る主な項目: `title` / `briefDescription` / `deadline` / `reward` /
`maxDailySubmissions` / `maxTeamSize` / `forumId` など。

### discussion 一覧

`forumId` は上の GetCompetition のレスポンスに含まれる。

```bash
bash .claude/skills/read-kaggle/fetch.sh \
  pokemon-tcg-ai-battle-challenge-strategy \
  discussions.DiscussionsService/GetTopicListByForumId \
  '{"forumId":10272044}' | python3 -m json.tool
```

## 既知の制限

- overview / rules の**長文本文**を返す RPC は未特定。GetCompetition の
  `briefDescription`（短い説明）までしか取れていない。本文が必要なときは
  エンドポイント名の特定か、別手段（ヘッドレスブラウザ等）が要る。
- 新しいエンドポイントを使うときは、ブラウザの DevTools Network で
  `api/i/...` のリクエスト名と body を確認して、このスキルに追記する。
- 非公式の内部 API なので、Kaggle 側の変更で動かなくなる可能性がある。
