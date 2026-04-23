# リサーチ: 社員詳細機能

**フィーチャー**: 社員詳細機能（#10）
**作成日**: 2026-04-20
**ブランチ**: `feature/issues-10`

## 技術的決定事項

### 1. エンドポイント設計

**決定**: `GET /api/employees/<int:id>`

**理由**:
- RESTful原則に従いリソースパスにIDを含める
- Flaskの型変換 `<int:id>` を使うことで文字列IDは自動的に404になる（追加バリデーション不要）
- 既存の `/api/employees` との一貫性

**検討した代替案**:
- `GET /api/employees?id=N`: クエリパラメータ方式は詳細取得には不適切

---

### 2. 404エラーレスポンス形式

**決定**: `{"error": "社員が見つかりません"}` + HTTP 404

**理由**:
- Constitution III（シンプリシティ）に従い最小限のエラー形式
- 社員一覧との一貫性（JSONレスポンス）
- 存在しないIDと退職済みIDは同じ404で統一（FR-004, FR-006）

**検討した代替案**:
- エラーコードを含む詳細エラー形式: 現時点では不要（YAGNI）

---

### 3. Blueprint配置

**決定**: 既存の `app/api/presentation/employees.py` に詳細エンドポイントを追加

**理由**:
- Constitution II（1機能1ファイル）の「機能」はリソース（employees）単位
- 同リソースへの複数エンドポイントを同一Blueprintにまとめるのが自然

---

### 4. リポジトリ層の変更

**決定**: `app/api/infrastructure/employee_repository.py` に `find_active_employee_by_id(app, id)` を追加

**理由**:
- 既存の `find_active_employees(app)` と対称的な命名
- `status = '在籍中'` の絞り込みを同層で実施（FR-006対応）
- 見つからない場合は `None` を返し、ユースケース層で404判定

---

### 5. ユースケース層の変更

**決定**: `app/api/usecase/get_employee.py`（新規）を作成し `get_employee(app, id)` を定義

**理由**:
- 既存の `get_employees.py` は一覧用途。責務を分離してシンプルに保つ
- 見つからない場合は `None` を返し、presentation層で404レスポンスに変換

---

### 6. years_of_service の計算

**決定**: 既存の `Employee.years_of_service` プロパティをそのまま利用

**理由**:
- 社員一覧機能と同一ロジック（Constitution: 重複排除・シンプリシティ）
- domain層に定義済みのため変更不要
