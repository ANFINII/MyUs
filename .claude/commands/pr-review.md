# PRレビュー

現在のブランチのPull Requestに対してGitHub上でコードレビューを投稿します。

## 実行手順

### 1. PR情報の取得
以下を並列で実行：
- `gh pr view --json number,title,url,headRefName,baseRefName` - PR番号・タイトル・URL・ブランチ情報
- `git branch --show-current` - 現在のブランチ名

**中止条件：**
- 現在のブランチにPRが存在しない場合 → 「PRが見つかりません」と伝えて終了

### 2. 変更内容の分析
以下を実行して差分を把握：
- `gh pr diff` または `git diff main...HEAD` で詳細な差分を取得
- 変更ファイル・追加・削除・修正内容を把握
- 変更の目的・意図を理解

### 3. レビュー実施
差分を精査し、以下の観点でレビューコメントを作成：

**レビュー観点：**
- バグ・ランタイムエラーの可能性
- デッドコード・未使用のインポート
- パフォーマンス問題（N+1クエリ、不要なDBフェッチなど）
- 命名の不統一・不適切な変数名
- ハードコードされた値
- 層の分離違反（ドメイン層にリクエスト層の型が混在など）
- セキュリティ上の懸念

### 4. レビュー投稿
`gh api` でGitHub上にインラインコメント付きレビューを投稿：

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --method POST \
  --input - <<'PAYLOAD'
{
  "commit_id": "<HEAD commit SHA>",
  "body": "## レビュー\n\n総評をここに記載",
  "event": "COMMENT",
  "comments": [
    {
      "path": "対象ファイルパス",
      "line": 行番号,
      "side": "RIGHT",
      "body": "指摘内容。修正案がある場合は ```suggestion ブロックで提案"
    }
  ]
}
PAYLOAD
```

**注意事項：**
- `event` は `"COMMENT"` を使用（自分のPRには `REQUEST_CHANGES` が使えない）
- `commit_id` は `git rev-parse HEAD` で取得
- ファイルパスはリポジトリルートからの相対パス（`gh api repos/{owner}/{repo}/pulls/{pr_number}/files` で確認）
- `line` はファイル内の行番号（diffのhunk内にある行のみコメント可能）
- 指摘がない場合は「問題は見つかりませんでした」と報告して終了

### 5. 結果報告
- 成功時：レビューのURLを表示
- 失敗時：エラー内容と対処法を案内
