# 顧客一覧API

## やること
customersドメインの一覧取得APIを実装する。
ディレクトリ・ファイルの雛形から作成すること。

## アーキテクチャルール

### 依存の方向
api → usecase（インターフェース経由） → repository（インターフェース経由）

### 命名規則
- インターフェースのクラス名はIから始める
- 具象クラスはインターフェース名からIを除いた名前

### 層の構成
- `app/api/{ドメイン}/` : ルーティング。usecaseのインターフェースに依存
- `app/usecase/{ドメイン}/` : `__init__.py` にInput/Output dataclassとIUseCase。ユースケース単位でファイルを作成
- `app/repository/{ドメイン}/` : `__init__.py` にdataclassとIRepository。具象クラスは別ファイル

### DIの仕組み
- flask-injectorを使用
- `app/module.py` の `AppModule` にbindを追加する
- `binder.bind(IXxx, to=Xxx)` の形式
- apiのhandlerでは `@inject` デコレータと型アノテーションで注入

## データ
DBは不要。インメモリの固定値で実装する。

## テスト方針
- テストを先に書く（TDD）
- usecaseのテストはインメモリの具象repositoryを直接使う（mockしない）
- `tests/usecase/{ドメイン}/` にテストを作成
