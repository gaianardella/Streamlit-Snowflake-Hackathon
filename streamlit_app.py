from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
import uuid
# import snowflake.connector

st.write("ciao")
# Establish a connection to your Snowflake database
# cnx = snowflake.connector.connect(**st.secrets["snowflake"])

session = Session.builder.configs(st.secrets["snowflake"]).create()
# Create Snowpark DataFrames that loads data
# snow_df_co2 = session.table("clothes_table")

# Convert Snowpark DataFrames to Pandas DataFrames for Streamlit
# pd_df_co2 = snow_df_co2.to_pandas()

uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, label_visibility='hidden')
if uploaded_file is not None:
  # Convert image base64 string into hex 
  bytes_data_in_hex = uploaded_file.getvalue().hex()

  # Generate new image file name
  file_name = 'img_' + str(uuid.uuid4())

  # Write image data in Snowflake table
  df = pd.DataFrame({"id": [file_name], "item": [bytes_data_in_hex]})
  session.write_pandas(df, "clothes_table")








#cnx.close()
