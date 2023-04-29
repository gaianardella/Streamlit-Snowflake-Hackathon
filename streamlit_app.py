from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
# import snowflake.connector

st.write("ciao")
# Establish a connection to your Snowflake database
# cnx = snowflake.connector.connect(**st.secrets["snowflake"])

session = Session.builder.configs(st.secrets["snowflake"]).create()
# Create Snowpark DataFrames that loads data
snow_df_co2 = session.table("clothes_table")










#cnx.close()
