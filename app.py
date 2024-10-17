import streamlit as st
import polars as pl

from supabase import create_client


@st.cache_resource
def initialize_supabase_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


supabase = initialize_supabase_connection()


@st.cache_data(ttl=60)
def query_tx_data():
    return supabase.table(st.secrets["SUPABASE_TX_TABLE_KEY"]).select().execute().data


def main():
    st.title("Transaction Data Visualizer")
    st.write(pl.DataFrame(query_tx_data()))


main()
