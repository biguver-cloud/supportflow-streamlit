# SupportFlow（CS業務管理ツール）

Streamlit + SQLite を用いて作成した、  
**カスタマーサポート向けのチケット管理ツール（MVP）** です。

問い合わせ対応を  
「作成 → 一覧管理 → ステータス更新 → CSV / Excel出力」  
まで一通り行える構成になっています。

---

## 📌 主な機能

- チケットの新規作成
- チケット一覧表示（フィルタ対応）
  - ステータス
  - カテゴリ
  - 顧客区分
  - 担当者
  - キーワード検索
- チケットの更新（ステータス・担当者・メモ）
- データ出力
  - CSV（UTF-8 / Excel向け）
  - Excel（.xlsx）

---

▼実際の画面▼

<img width="1902" height="870" alt="image" src="https://github.com/user-attachments/assets/8414fa69-3d2c-470a-b4c7-30a97d8d511f" />

---

## 🛠 使用技術

- Python 3.x
- Streamlit
- SQLite
- Pandas
- Git / GitHub

---

## 📂 ディレクトリ構成

supportflow-streamlit/
├─ app.py # メインUI（Streamlit）
├─ db/
│ └─ database.py # DB初期化・接続
├─ repository/
│ └─ ticket_repository.py # DB操作（CRUD）
├─ constants/
│ └─ master.py # マスタ定義
├─ requirements.txt
├─ README.md


---

## 🚀 ローカル実行方法

Plaintext

pip install -r requirements.txt
streamlit run app.py

ブラウザで以下にアクセス：
http://localhost:8501

---

## 📤 データ出力について

CSV（UTF-8 / BOM付き）
Googleスプレッドシート向け

CSV（Excel向け / CP932）
Windows Excelで文字化けしにくい形式

Excel（.xlsx）
文字化けを完全回避したい場合に推奨

---

## 📤 データ出力について
CSV（UTF-8 / BOM付き）
Googleスプレッドシート向け

CSV（Excel向け / CP932）
Windows Excelで文字化けしにくい形式

Excel（.xlsx）
文字化けを完全回避したい場合に推奨

---

## 🌐 デプロイについて（Streamlit Cloud）
本アプリは Streamlit Cloud でのデプロイを想定しています。

デプロイ手順概要
1. GitHub にリポジトリを push
2. Streamlit Cloud にログイン
3. 「New app」 → GitHubリポジトリを選択
4. app.py を指定
5. デプロイ

※ SQLite は Streamlit Cloud では「一時保存」扱いになるため、
　本番利用では外部DB（PostgreSQL等）への移行が推奨されます。

---

## 🧠 今後の拡張アイデア
- ユーザー認証（管理者 / オペレーター）
- 対応履歴ログ
- 優先度（高・中・低）
- SLA / 対応時間の可視化
- 外部DB（Cloud SQL / Supabase 等）連携

📄 ライセンス
MIT License

