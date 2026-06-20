#!/usr/bin/env bash
# Kaggle の内部 JSON API をブラウザなしで叩く。
# XSRF トークンを Cookie から取り、x-xsrf-token ヘッダに付けて POST する。
#
# Usage: fetch.sh <competition-name> <endpoint> [json-body]
#   competition-name : 例 pokemon-tcg-ai-battle-challenge-strategy
#   endpoint         : 例 competitions.CompetitionService/GetCompetition
#   json-body        : 省略時は {}
set -euo pipefail

COMP="$1"
EP="$2"
if [ "$#" -ge 3 ]; then BODY="$3"; else BODY='{}'; fi

CJAR="$(mktemp)"
trap 'rm -f "$CJAR"' EXIT

# 1. 任意の Kaggle ページに GET して XSRF-TOKEN Cookie を取得
curl -s -c "$CJAR" "https://www.kaggle.com/competitions/${COMP}/overview" -o /dev/null

# 2. Cookie ファイル(タブ区切り)の name=XSRF-TOKEN の value を取り出す
TOKEN="$(awk -F'\t' '$6=="XSRF-TOKEN"{print $7}' "$CJAR")"
if [ -z "$TOKEN" ]; then
  echo "XSRF-TOKEN を取得できませんでした" >&2
  exit 1
fi

# 3. トークンを付けて内部 API を叩く
curl -s "https://www.kaggle.com/api/i/${EP}" \
  -b "$CJAR" \
  -H "content-type: application/json" \
  -H "x-xsrf-token: ${TOKEN}" \
  --data "$BODY"
