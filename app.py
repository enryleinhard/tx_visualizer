import os
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
supabase_url: str = os.getenv('SUPABASE_URL')
supabase_key: str = os.getenv('SUPABASE_KEY')
supabase_tx_table_key = 'transaction'

supabase: Client = create_client(supabase_url, supabase_key)
tx_table_response = supabase.table(supabase_tx_table_key).select().execute()

tx_df = pd.DataFrame(tx_table_response.data)

st.set_page_config(page_title='Transaction Visualizer', page_icon=':moneybag:', layout='wide')
st.title(f'Transaction Visualizer')
tx_df