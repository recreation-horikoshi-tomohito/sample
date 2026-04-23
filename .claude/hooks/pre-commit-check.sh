#!/bin/sh
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

echo "$command" | grep -q '^git commit' || exit 0

echo "[pre-commit] ruff format を実行..." >&2
if ! docker compose exec -T app-container ruff format .; then
  echo '{"continue": false, "stopReason": "ruff format に失敗しました。フォーマットエラーを確認してください。"}'
  exit 0
fi

echo "[pre-commit] ruff check を実行..." >&2
if ! docker compose exec -T app-container ruff check .; then
  echo '{"continue": false, "stopReason": "ruff check に失敗しました。Lint エラーを確認してください。"}'
  exit 0
fi

echo "[pre-commit] pytest を実行..." >&2
if ! docker compose exec -T app-container pytest -v; then
  echo '{"continue": false, "stopReason": "pytest に失敗しました。テストエラーを確認してください。"}'
  exit 0
fi

echo "[pre-commit] 全チェック通過 ✅" >&2
