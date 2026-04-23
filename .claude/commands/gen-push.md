# /gen-push — Push & PR コマンド生成

現在のブランチを push して PR を作るためのコマンドを生成します。
Claude 自身は実行せず、ターミナルにペーストできる形で出力します。

## 手順

1. 以下の情報を取得する:
   - `git branch --show-current` で現在のブランチ名
   - `git remote get-url origin` でリモート URL
   - `git log develop..HEAD --oneline` でブランチの変更概要
   - `git diff develop..HEAD --name-only` で変更ファイル一覧

2. 取得した情報をもとに、以下の2つのコマンドブロックをユーザーに出力する:

**ステップ 1: Push**
```
git push -u origin <ブランチ名>
```

**ステップ 2: PR 作成**
変更内容を分析して適切な PR タイトルと本文を生成し、以下の形式で出力する:
```
gh pr create \
  --title "<タイトル>" \
  --body "$(cat <<'EOF'
## Summary

- <変更内容の箇条書き>

## Test plan

- [ ] <確認項目>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

3. 「上記をターミナルにペーストして実行してください」と案内する。
