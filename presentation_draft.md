# TableFlow — 10分デモ台本

> **方針**: 「動くものを見せる」→「証拠をサッと見せる」。コード一行ずつの解説は不要。

---

## 概要

| フェーズ | 時間 | 内容 | 網羅基準 |
|---|---|---|---|
| 1: 開発プロセス | ~2分 | GitHub Issues → AGENTS.md → git log | #1, #2 |
| 2: 実演・フロントエンド | ~4分 | バリデーション → HTMX動的更新 → テンプレート | #4, #5, #6, #7 |
| 3: バックエンド・品質 | ~3分 | pytest → Admin → デプロイ設定 | #3, #8, #9 |

---

## フェーズ1：開発プロセス証明（~2分）

### Step 1-1: Issue駆動開発（30秒）

ブラウザで GitHub → **Issues → Closed** を表示。

- 各 Issue がブランチ・コミットに紐づいていることを確認
- PR タブでコードレビューの形跡を一瞥

> 「Issue駆動開発を実践。ブランチ作成→PR→レビュー→マージのワークフローです」

### Step 1-2: AI活用環境（60秒）

エディタで以下をサッと表示:

- `AGENTS.md` — プロジェクト規約・コーディング規則・変更カップリングルール
- `pyproject.toml` の `[tool.ruff]` セクション
- `.opencode/skills/` ディレクトリ一覧

> 「AGENTS.md にプロジェクト規約を明文化。AIが一貫したコード生成を行う環境を整えました。リントは ruff」

### Step 1-3: コミット履歴（30秒）

ターミナルで `git log --oneline -10` を実行。

> 「小さく原子的なコミットを心がけています」

---

## フェーズ2：実演・フロントエンド（~4分）

### Step 2-1: バリデーションエラー（90秒）

ブラウザで `/reservations/new/` を開き、以下を順に実演:

1. **過去日時**: 過去の日時を設定 → エラー「過去の日時は予約できません」
2. **定員超過**: 4人テーブルに10人指定 → エラー「収容人数は○名まで」
3. **ダブルブッキング**: 同テーブル・同刻に2件目 → エラー「このテーブルは既に予約されています」

その後、エディタで `apps/reservations/forms.py` を表示:

- `clean_reservation_time()` — 過去日時チェック（57-60行目）
- `clean()` — 定員超過チェック（68-73行目）、ダブルブッキングチェック（77-84行目）

> 「ビジネスロジックはフォームの `clean()` に集約。3つの検証ルールを実装しています」

### Step 2-2: HTMX動的更新（90秒）

ブラウザのフォームで操作:

1. **人数を `5` に変更** → テーブル選択肢から4人以下のテーブルが消える
2. **日時を変更** → 予約済みテーブルが選択肢から消える
3. ブラウザ **DevTools → Network** で HTMX の GET リクエストを確認

その後、エディタで以下を一瞥:

- `forms.py:32-35` — `hx-get`, `hx-trigger`, `hx-target`, `hx-swap` 属性
- `views.py:41-64` — `available_tables_partial` 関数（容量フィルタ + 予約排除）
- `_table_options.html` — `<option>` を返す4行のHTMLフラグメント

> 「HTMXによりページリロードなしでテーブル選択肢を動的更新。人数・日時変更時に空きテーブルだけ返します」

### Step 2-3: テンプレート継承・レスポンシブ（30秒）

エディタで `templates/reservations/base.html` を表示:

- Bootstrap 5 の navbar（ハンバーガーメニュー対応）
- `{% block content %}` 継承構造

ブラウザ幅を狭めてモバイル表示に切り替え → ハンバーガーメニュー確認

> 「テンプレート継承でナビ・フッターを一元管理。Bootstrap 5でレスポンシブ対応」

---

## フェーズ3：バックエンド・品質（~3分）

### Step 3-1: テスト実行（60秒）

ターミナルで `uv run pytest` を実行 → 全パス、カバー率89%を表示。

エディタで以下を一瞥:

- `tests/test_forms.py` — `test_past_reservation_time`, `test_exceeds_table_capacity`, `test_double_booking`
- `tests/test_views.py` — `AvailableTablesPartialTests`
- `tests/test_models.py` — テストクラス

> 「14件のテストでカバー率89%。特にダブルブッキング防止の検証が重要です」

### Step 3-2: DBスキーマとAdmin（60秒）

1. エディタで `apps/reservations/models.py` を表示:
   - `Table` モデル — `table_number`, `capacity`, `is_active`
   - `Reservation` モデル — `ForeignKey(Table, on_delete=CASCADE)`, `STATUS_CHOICES`
2. ブラウザで Django Admin (`/admin/`) を開き、Table・Reservation レコードを確認

> 「Table と Reservation は ForeignKey で1対多。CASCADE でテーブル削除時に予約も自動削除」

### Step 3-3: デプロイ設定（60秒）

エディタで以下をサッと表示:

- `pyproject.toml:11-12` — `whitenoise`, `waitress` 依存関係
- `config/settings.py` — `WhiteNoiseMiddleware`, `STATICFILES_STORAGE`
- `README.md` — Deployment セクション

> 「デプロイは Waitress をWSGIサーバーとして使用。WhiteNoise で静的ファイルを圧縮配信」

---

## クロージング（10秒）

> 「以上、TableFlowのデモでした。Django + HTMX で構成し、Issue駆動開発・AI活用・テストカバー率89%を達成しています。ご質問があればお願いします」

---

## 付録: デモ前に確認すること

- [ ] `uv run python manage.py migrate` が完了している
- [ ] テスト用データが Admin に投入済み（Table 2〜3件、Reservation 1件以上）
- [ ] `uv run pytest` が全パスする状態
- [ ] ブラウザの DevTools が開ける状態（Network タブ）
- [ ] GitHub リポジトリが公開状態（Issues/PR が閲覧可能）

---

## 付録: 評価基準と対応表

| # | 評価基準 | フェーズ | 対象ファイル |
|---|---|---|---|
| 1 | Tools/AI Setup | 1 | `AGENTS.md`, `pyproject.toml`, `.opencode/skills/` |
| 2 | Managerial Practices | 1 | GitHub Issues/PR, `git log` |
| 3 | Database Schema | 3 | `apps/reservations/models.py`, Admin |
| 4 | Business Logic | 2 | `apps/reservations/forms.py`, `apps/reservations/views.py` |
| 5 | Use of Templates | 2 | `templates/reservations/*.html` |
| 6 | User Input | 2 | `apps/reservations/forms.py`, `form.html` |
| 7 | Rich Interface/HTMX | 2 | `forms.py`, `_table_options.html` |
| 8 | Tests/Specs/Docs | 3 | `apps/reservations/tests/`, `openspec/`, `README.md` |
| 9 | Deployment | 3 | `pyproject.toml`, `config/settings.py` |
| 10 | Presentation | 全体 | 本台本 |
