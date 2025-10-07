# GitHubへのアップロード完全ガイド

## 📋 準備

### 必要なもの
- ✅ GitHubアカウント（[無料登録](https://github.com/join)）
- ✅ Git または GitHub Desktop
- ✅ このプロジェクト

---

## 🎯 方法1: GitHub Desktop（初心者向け・推奨）

### ステップ1: GitHub Desktop のインストール

1. **ダウンロード**
   - [GitHub Desktop](https://desktop.github.com/) にアクセス
   - 「Download for Windows」をクリック
   - インストーラーを実行

2. **サインイン**
   - GitHub Desktop を起動
   - 「Sign in to GitHub.com」をクリック
   - GitHubアカウントでログイン

### ステップ2: リポジトリの作成

1. **新しいリポジトリを作成**
   ```
   File → Add local repository
   ```

2. **プロジェクトフォルダを選択**
   ```
   c:\scripts\CascadeProjects\remote-productivity
   ```

3. **「create a repository」をクリック**

4. **リポジトリ情報を入力**
   - **Name**: `life-management-app`（または任意の名前）
   - **Description**: `Comprehensive Life Management App - Privacy-first productivity tool`
   - **Git Ignore**: `Python`
   - **License**: `MIT License`

5. **「Create repository」をクリック**

### ステップ3: 初回コミット

1. **変更を確認**
   - 左側にすべてのファイルが表示されます
   - チェックマークがついていることを確認

2. **コミットメッセージを入力**
   ```
   Summary: Initial commit - Life Management App v1.0
   Description: 
   - Complete productivity and life management features
   - Privacy-first design (100% local storage)
   - Security enhancements
   - Multi-language support (Japanese/English)
   ```

3. **「Commit to main」をクリック**

### ステップ4: GitHubに公開

1. **「Publish repository」をクリック**

2. **公開設定**
   - **Name**: リポジトリ名（確認）
   - **Description**: 説明（確認）
   - **Keep this code private**: 
     - ✅ チェック = プライベート（自分だけ）
     - ☐ チェック外す = パブリック（誰でも見れる）

3. **「Publish repository」をクリック**

4. **完了！**
   - ブラウザで GitHub を開いて確認
   - `https://github.com/あなたのユーザー名/life-management-app`

---

## 🖥️ 方法2: コマンドライン（Git経験者向け）

### ステップ1: Gitのインストール確認

```bash
git --version
```

**インストールされていない場合：**
- Windows: [Git for Windows](https://git-scm.com/download/win)
- Mac: `brew install git`
- Linux: `sudo apt-get install git`

### ステップ2: Git設定（初回のみ）

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### ステップ3: ローカルリポジトリの初期化

```bash
# プロジェクトフォルダに移動
cd c:\scripts\CascadeProjects\remote-productivity

# Gitリポジトリを初期化
git init

# ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit - Life Management App v1.0"
```

### ステップ4: GitHubでリポジトリを作成

1. **GitHubにログイン**
   - [GitHub](https://github.com) にアクセス

2. **新しいリポジトリを作成**
   - 右上の「+」→「New repository」をクリック

3. **リポジトリ情報を入力**
   - **Repository name**: `life-management-app`
   - **Description**: `Comprehensive Life Management App - Privacy-first productivity tool`
   - **Public/Private**: 選択
   - **Initialize this repository with**: すべてチェックを外す（既にファイルがあるため）

4. **「Create repository」をクリック**

### ステップ5: リモートリポジトリに接続してプッシュ

```bash
# リモートリポジトリを追加（URLは自分のものに変更）
git remote add origin https://github.com/あなたのユーザー名/life-management-app.git

# ブランチ名を main に変更（必要な場合）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

**認証が求められた場合：**
- ユーザー名: GitHubのユーザー名
- パスワード: Personal Access Token（後述）

---

## 🔑 Personal Access Token の作成（コマンドライン使用時）

GitHubはパスワード認証を廃止したため、トークンが必要です。

### 手順

1. **GitHubにログイン**

2. **Settings に移動**
   - 右上のアイコン → Settings

3. **Developer settings**
   - 左メニュー最下部の「Developer settings」

4. **Personal access tokens**
   - 「Personal access tokens」→「Tokens (classic)」

5. **Generate new token**
   - 「Generate new token (classic)」をクリック

6. **トークン設定**
   - **Note**: `Life Management App`
   - **Expiration**: `90 days`（または任意）
   - **Select scopes**: 
     - ✅ `repo`（すべてにチェック）

7. **「Generate token」をクリック**

8. **トークンをコピー**
   - ⚠️ 表示されるのは1回だけ！
   - 安全な場所に保存

9. **使用方法**
   - `git push` 時のパスワード欄にトークンを貼り付け

---

## 📝 アップロード前のチェックリスト

### 必須項目
- [ ] `.gitignore` ファイルがある
- [ ] `LICENSE` ファイルがある
- [ ] `README.md` が更新されている
- [ ] 個人情報が含まれていない
- [ ] データベースファイル（.db）が除外されている
- [ ] `.env` ファイルが除外されている

### 推奨項目
- [ ] `README_EN.md`（英語版）がある
- [ ] `SECURITY.md` がある
- [ ] `TERMINOLOGY.md` がある
- [ ] メールアドレスを実際のものに変更
- [ ] GitHubリポジトリURLを更新

---

## 🔄 更新をプッシュする方法

### GitHub Desktop の場合

1. **変更を確認**
   - 自動的に変更が検出されます

2. **コミット**
   - Summary に変更内容を入力
   - 「Commit to main」をクリック

3. **プッシュ**
   - 「Push origin」をクリック

### コマンドラインの場合

```bash
# 変更を確認
git status

# 変更をステージング
git add .

# コミット
git commit -m "Update: 機能追加の説明"

# プッシュ
git push
```

---

## 🌟 リポジトリを魅力的にする

### README.md の充実
- ✅ スクリーンショットを追加
- ✅ バッジを追加（License, Python, Flask）
- ✅ デモGIFを追加
- ✅ 詳細な使い方を記載

### GitHub設定
1. **About セクション**
   - リポジトリページの右上「⚙️」をクリック
   - Description を入力
   - Website を追加（あれば）
   - Topics を追加：
     - `productivity`
     - `flask`
     - `python`
     - `life-management`
     - `privacy-first`
     - `pomodoro`

2. **README の表示**
   - リポジトリのトップに自動表示されます

---

## 🚨 注意事項

### アップロードしてはいけないもの
- ❌ `productivity.db`（データベース）
- ❌ `.env`（環境変数）
- ❌ `__pycache__/`（Pythonキャッシュ）
- ❌ 個人情報
- ❌ APIキー
- ❌ パスワード

### 公開前の確認
1. **個人情報のチェック**
   ```bash
   # ファイル内を検索
   grep -r "your-email" .
   grep -r "password" .
   ```

2. **機密情報のチェック**
   - メールアドレス
   - APIキー
   - データベースの内容

---

## 📚 参考リンク

- [GitHub Desktop ドキュメント](https://docs.github.com/ja/desktop)
- [Git 公式ドキュメント](https://git-scm.com/doc)
- [GitHub ヘルプ](https://docs.github.com/ja)
- [.gitignore テンプレート](https://github.com/github/gitignore)

---

## ❓ トラブルシューティング

### Q: プッシュ時に認証エラーが出る
**A**: Personal Access Token を使用してください（上記参照）

### Q: ファイルが多すぎてアップロードできない
**A**: `.gitignore` を確認し、不要なファイルを除外

### Q: データベースファイルがアップロードされた
**A**: 
```bash
git rm --cached productivity.db
git commit -m "Remove database file"
git push
```

### Q: 間違ったファイルをコミットした
**A**: 
```bash
# 最後のコミットを取り消し
git reset --soft HEAD~1

# ファイルを修正してから再コミット
git add .
git commit -m "Correct commit"
```

---

## 🎉 完了後

### リポジトリの確認
1. GitHubでリポジトリを開く
2. すべてのファイルが表示されているか確認
3. README が正しく表示されているか確認

### 共有
- リポジトリURLを共有
- `https://github.com/あなたのユーザー名/life-management-app`

### 次のステップ
- [ ] GitHub Actions でCI/CD設定
- [ ] Issues でバグ管理
- [ ] Projects でタスク管理
- [ ] Wiki でドキュメント作成
- [ ] Releases でバージョン管理

---

**おめでとうございます！🎊**

あなたのプロジェクトがGitHubで公開されました！
