import streamlit as st
import pandas as pd
import altair as alt

from supabase import create_client

st.set_page_config(page_title="Transaction Data", page_icon="💵", layout="wide")


@st.cache_resource
def initialize_supabase_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


supabase = initialize_supabase_connection()


def query_tx_data(month):
    return (
        supabase.table(st.secrets["SUPABASE_TX_TABLE_KEY"])
        .select()
        .like("tx_date", f"%-{month}-%")
        .execute()
        .data
    )


def daily_sum_data_transformer(tx_df):
    daily_sum = tx_df.groupby("tx_date").aggregate({"tx_amount": "sum"})
    daily_sum.index = pd.to_datetime(daily_sum.index)
    daily_sum.index = daily_sum.index.strftime("%d")
    return daily_sum


def category_sum_data_transformer(tx_df):
    category_sum = tx_df.groupby("category").aggregate({"tx_amount": "sum"})
    return category_sum


def main():
    st.title("Transaction Data")
    st.selectbox(
        "Month",
        range(1, 13),
        key="month",
    )
    tx_df = pd.DataFrame(query_tx_data(st.session_state.month))
    tx_df["tx_date"] = pd.to_datetime(tx_df["tx_date"])

    c1, c2 = st.columns(2)
    if tx_df.empty:
        st.warning("No data found for the selected month.")
        return

    with c1:
        st.write("Total transaction(s):", len(tx_df))
        st.write(
            "Total transaction(s) amount:",
            tx_df["tx_amount"].sum(),
        )
        st.write("Transaction(s):")
        edit_df = c1.data_editor(
            tx_df,
            column_config={"id": None},
            width=(1440),
            height=((len(tx_df) + 1) * 35 + 3),
        )

        difference = (
            tx_df.merge(edit_df, how="outer", indicator=True)
            .loc[lambda x: x["_merge"] == "right_only"]
            .drop(columns="_merge")
        )

        if not difference.empty:
            supabase.table(st.secrets["SUPABASE_TX_TABLE_KEY"]).upsert(
                difference.to_dict(orient="records")
            ).execute()
            st.rerun()

    with c2:


            st.write("Total daily transaction(s}:")
            category_sum = category_sum_data_transformer(tx_df)
            category_sum.reset_index(inplace=True)
            category_sum_chart = (
                alt.Chart(category_sum)
                .mark_arc()
                .encode(
                    theta="tx_amount",
                    color="category",
                )
                .properties(height=480)
            )
            st.altair_chart(category_sum_chart, use_container_width=True)


            st.write("Total transaction(s) daily:")
            daily_sum = daily_sum_data_transformer(tx_df)
            daily_sum.reset_index(inplace=True)
            daily_sum_chart = (
                alt.Chart(daily_sum)
                .mark_bar()
                .encode(
                    x=alt.X("tx_date", title="Date"),
                    y=alt.Y("tx_amount", title="Amount"),
                )
                .properties(height=480)
            )
            st.altair_chart(daily_sum_chart, use_container_width=True)


main()
