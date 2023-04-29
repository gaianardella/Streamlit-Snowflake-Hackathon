from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
# import snowflake.connector

uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, label_visibility='hidden')
if uploaded_file is not None:
  # Convert image base64 string into hex 
  bytes_data_in_hex = uploaded_file.getvalue().hex()
  cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  id=1
  item_selected="sweater"
  with cnx.cursor() as my_cur:
    my_cur.execute("insert into clothes_table values ('" +id+ "', '" +bytes_data_in_hex+ "', '" +item_selected+ "')")

  # Generate new image file name
#   file_name = 'img_' + str(uuid.uuid4())

  # Write image data in Snowflake table
#   df = pd.DataFrame({"id": "1", "item": [bytes_data_in_hex]})
#   session.write_pandas(df, "clothes_table")
