

# プロジェクト全体（ゴール）

* Excel の「まとめシート」を取り込み、SQLite に資産単位で保存する
* Streamlit ダッシュボードで横長レイアウト（左：全体／グループ、右：個別カード）を表示
* データは pandas ロジックで集計し、Plotly 等でグラフ描画
* UI は表示と基本的な手入力（新規レコード追加／編集／削除）ができる

---

# 優先度 A — 超重要（必ず最初にやる）

これらが動けば「見える」プロトタイプが完成する。

1. リポジトリ＆環境準備

   * 作業ブランチ命名例：`feat/prototype-streamlit`
   * ファイル構成テンプレ（以下に詳細）を作成
   * 必要パッケージの列挙（`requirements.txt`）

     * `streamlit`, `pandas`, `plotly`, `sqlite3`(標準), `sqlalchemy`（推奨）, `openpyxl`（Excel読込）
   * Acceptance Criteria: `pip install -r requirements.txt` が通って `streamlit run ui/app.py` の雛形が起動する

2. DB スキーマ（SQLite） & DB 接続モジュール

   * テーブル定義（SQLAlchemyモデル or raw SQL）：

     * `groups` (id, name)
     * `assets` (id, name, group_id, note)
     * `records` (id, asset_id, date, amount, note)
   * モジュール: `db/models.py`, `db/session.py`
   * AC: DB ファイル作成スクリプト `db/init_db.py` を実行すると空テーブルが作成される

3. Excel → DB インポータ（バッチ用スクリプト）

   * スクリプト: `scripts/import_excel.py`
   * 処理:

     * まとめシート読み込み（`pandas.read_excel(..., sheet_name='summary')` 前提）
     * 縦持ち変換（`melt`）
     * 資産マスタを `assets` に追加（既存チェック）
     * `records` に挿入
   * AC: 3つの年度ブック（テスト用サンプル）を与えると `assets` と `records` に正しくデータが入る

4. コア集計ロジック（ロジック層）

   * モジュール: `logic/analytics.py`
   * 関数群（公開API）:

     * `get_latest_snapshot(conn) -> DataFrame`（最新日付の資産残高）
     * `total_assets_by_date(conn, date=None) -> float`
     * `group_aggregation(conn, date=None) -> DataFrame`（グループ別合計）
     * `time_series_total(conn, start, end) -> DataFrame`（総資産推移）
     * `asset_timeseries(asset_id, start, end) -> DataFrame`
   * AC: ユニットテストで期待される DataFrame のカラムとサンプル値が得られる

5. Streamlit ダッシュボード（最小限の実装）

   * ファイル: `ui/app.py`
   * 機能:

     * 左カラム：総資産カード、グループ推移（Plotly エリアチャート）
     * 中央大：月次総資産推移（折れ線）
     * 右カラム：個別資産カードのグリッド（スパークライン）
     * 下部に「データ表（フィルタ可）」のトグル表示（最初はボタンで表示切替）
   * AC: ブラウザで `localhost:8501` にアクセス → ダッシュボードが表示される（モックデータでOK）

---

# 優先度 B — あると便利（次に着手）

プロトタイプを便利にする追加機能。

6. 入力画面 / CRUD（最小）

   * UI側で「日付」「資産（選択）」「金額」「備考」を入力して `records` に追加
   * 編集/削除はまずは一覧から1つずつ操作可能にする
   * AC: 追加した値が即ダッシュボードに反映される

7. マウスオーバーでの個別詳細オーバーレイ実装（右側カード）

   * Streamlit の `st.tooltip` 的な挙動はないので、代替案：

     * 右カードに「詳細▼」ボタンでモーダル風に `st.expander` or `st.modal` を開く
   * AC: 個別カードの「詳細」クリックで履歴表がモーダルに表示される

8. 設定 / 資産マスタ編集画面

   * 資産の追加・編集・グループ割当ができる管理画面を作る
   * AC: 新しい資産を追加 → 右カードに表示される

9. テスト & サンプルデータ

   * 単体テスト（ロジック層）と簡単な統合テスト（インポータがDBへ正しく入れる）
   * テスト用のCSV/XLSXサンプルを `data/sample/` に置く

---

# 優先度 C — 将来的/改善（移行フェーズ）

最初のリリース後に着手。

10. UIの改良（レスポンシブ、テーマ、更に高密度情報表示）
11. PyQt/PySide への移植計画（UI 層の差し替え）
12. バックアップ & エクスポート（DB → CSV/Excel）
13. ローカル内マルチユーザー（必要ならSQLiteからPostgresへ移行）

---

# タスクの粒度（チケット化例）

* `T-001` Init repo + requirements + readme
* `T-002` DB schema + init script
* `T-003` Excel import basic (single sheet)
* `T-004` analytics: total & group aggregation functions
* `T-005` Streamlit: dashboard skeleton + mock data
* `T-006` Connect dashboard to real DB
* `T-007` CRUD: add record
* `T-008` asset master management UI
* `T-009` tests + sample data
* `T-010` polish UI (colors, spacing, sparkline)

---

# 推奨ファイル構成（具体例）

```
my_assets_app/
├── README.md
├── requirements.txt
├── data/
│   └── sample/
│       └── 2023_summary.xlsx
├── db/
│   ├── init_db.py
│   ├── models.py
│   └── session.py
├── logic/
│   └── analytics.py
├── scripts/
│   └── import_excel.py
├── ui/
│   └── app.py        # Streamlit
├── tests/
│   └── test_analytics.py
└── assets.db
```

---

# 実装のヒント（vibe coding / Copilot向けのプロンプト例）

* 「pandasで日付をインデックスにして月次合計を返す関数を実装して」
* 「Plotlyで積み上げエリアチャートを描くコードをStreamlit用に書いて」
* 「SQLiteの`records`テーブルから最新日を取得して assetsごとに合計するSQLを書いて」

これらを小さな TODO コメントとしてソースに置けば、Copilot がスニペット候補を出しやすいよ。

---

# 受け入れ基準（Definition of Done） — 最小リリース

* Excel まとめシートを import できる
* ダッシュボードが Streamlit で表示され、総資産・グループ比率・総資産推移が見られる
* 右側に個別資産カードが並び、クリックで詳細が見られる
* 新規記録の追加ができ、即反映される

