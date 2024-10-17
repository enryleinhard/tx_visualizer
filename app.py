import json
import os
import streamlit as st
import polars as pl 

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
supabase_url: str = os.getenv('SUPABASE_URL')
supabase_key: str = os.getenv('SUPABASE_KEY')
supabase_tx_table_key = 'transaction'

supabase: Client = create_client(supabase_url, supabase_key)
tx_table_response = supabase.table(supabase_tx_table_key).select().execute()

tx_df = pl.DataFrame(tx_table_response.data)

st.set_page_config(page_icon=':moneybag:', layout='wide')
st.title(f'Transaction Visualizer')
tx_df