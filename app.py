import streamlit as st
import polars as pl

from supabase import create_client

st.set_page_config(
    page_title="Transaction Data Visualizer", page_icon="💵", layout="wide"
)


@st.cache_resource
def initialize_supabase_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


supabase = initialize_supabase_connection()


@st.cache_data(ttl=60)
def query_tx_data(month):
    return (
        supabase.table(st.secrets["SUPABASE_TX_TABLE_KEY"])
        .select()
        .like("tx_date", f"%-{month}-%")
        .execute()
        .data
    )


def main():
    st.write(st.session_state)
    st.title("Transaction Data Visualizer")
    st.selectbox(
        "Month:",
        range(1, 13),
        key="month",
    )
    tx_data = query_tx_data(st.session_state.month)
    if tx_data:
        st.write(pl.DataFrame(tx_data))
    else:
        st.write("No data found for this month")


main()
