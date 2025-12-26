import streamlit as st
import pandas as pd
from io import BytesIO

from db.database import init_db
from constants.master import STATUSES, CATEGORIES, CUSTOMER_TYPES
from repository.ticket_repository import fetch_tickets, create_ticket, update_ticket

st.set_page_config(page_title="SupportFlow", layout="wide")
init_db()

st.title("SupportFlow（CS業務管理ツール）")

left, center, right = st.columns([1, 2, 1])

# -----------------------
# 左：フィルタ
# -----------------------
with left:
    st.subheader("フィルタ")
    status = st.selectbox("ステータス", ["全て"] + STATUSES)
    category = st.selectbox("カテゴリ", ["全て"] + CATEGORIES)
    customer_type = st.selectbox("顧客区分", ["全て"] + CUSTOMER_TYPES)
    assignee = st.text_input("担当者（空なら全て）")
    keyword = st.text_input("キーワード（件名・内容・メモ）")

assignee_filter = assignee.strip() if assignee.strip() else "全て"
keyword_filter = keyword.strip() if keyword.strip() else None

# -----------------------
# 真ん中：一覧（選択・出力）
# -----------------------
with center:
    st.subheader("チケット一覧（選択して更新）")

    rows = fetch_tickets(
        status=status,
        category=category,
        customer_type=customer_type,
        assignee=assignee_filter,
        keyword=keyword_filter,
    )

    if len(rows) == 0:
        st.info("チケットがありません")
        selected_index = None
        df_view = pd.DataFrame()
    else:
        df = pd.DataFrame(rows)

        # 表示用（idは内部用）
        df_view = df[
            [
                "id",
                "created_at",
                "title",
                "customer_type",
                "category",
                "status",
                "assignee",
                "updated_at",
                "memo",
            ]
        ].copy()

        # --- 出力（フィルタ結果） ---
        export_df = df_view.drop(columns=["id"]).copy()

        # BOM付きShift-JIS CSV：Windows Excelで文字化けしない
        csv_sjis = export_df.to_csv(index=False, encoding="shift_jis", errors="replace")
        # BOM（Byte Order Mark）を先頭に追加
        csv_with_bom = b'\xef\xbb\xbf'.decode('utf-8') + '\ufeff' * 0  # UTF-8 BOM
        csv_sjis_bom = export_df.to_csv(index=False, encoding="shift_jis_2004", errors="replace")
        
        # シンプル版：Shift-JISのみ（Excelで開く→ウィザード→文字コードShift-JIS指定で対応）
        st.download_button(
            label="CSVダウンロード（Shift-JIS）",
            data=csv_sjis,
            file_name="supportflow_tickets.csv",
            mime="text/csv; charset=shift_jis",
        )

        # Excel形式（.xlsx）
        xlsx_buffer = BytesIO()
        with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="tickets")
        xlsx_buffer.seek(0)

        st.download_button(
            label="Excelダウンロード（.xlsx / 推奨）",
            data=xlsx_buffer,
            file_name="supportflow_tickets.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # 更新対象選択
        options = [f"{i}: {row['title']} ({row['status']})" for i, row in df_view.iterrows()]
        choice = st.selectbox("更新したいチケットを選択", ["選択しない"] + options)

        if choice == "選択しない":
            selected_index = None
        else:
            selected_index = int(choice.split(":")[0])

        # 一覧表示
        st.dataframe(
            df_view.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True,
        )

# -----------------------
# 右：新規作成 / 更新
# -----------------------
with right:
    if selected_index is None or df_view.empty:
        st.subheader("新規作成")

        new_customer_type = st.selectbox("顧客区分", CUSTOMER_TYPES, key="new_customer_type")
        new_category = st.selectbox("カテゴリ", CATEGORIES, key="new_category")
        new_title = st.text_input("件名（必須）", key="new_title")
        new_body = st.text_area("内容（必須）", key="new_body")
        new_assignee = st.text_input("担当者", key="new_assignee")
        new_memo = st.text_area("メモ", key="new_memo")

        if st.button("作成"):
            if not new_title.strip() or not new_body.strip():
                st.error("件名と内容は必須です")
            else:
                create_ticket(
                    title=new_title.strip(),
                    body=new_body.strip(),
                    customer_type=new_customer_type,
                    category=new_category,
                    assignee=new_assignee.strip(),
                    memo=new_memo.strip(),
                )
                st.success("チケットを作成しました")
                st.rerun()

    else:
        st.subheader("更新")

        row = df_view.loc[selected_index]
        ticket_id = row["id"]

        st.caption(f"選択中: {row['title']}")

        upd_status = st.selectbox(
            "ステータス（必須）",
            STATUSES,
            index=STATUSES.index(row["status"]),
        )
        upd_assignee = st.text_input("担当者", value=row.get("assignee", "") or "")
        upd_memo = st.text_area("メモ", value=row.get("memo", "") or "")

        if st.button("更新"):
            update_ticket(
                ticket_id=ticket_id,
                status=upd_status,
                assignee=upd_assignee.strip(),
                memo=upd_memo.strip(),
            )
            st.success("更新しました")
            st.rerun()
