import streamlit as st
import pandas as pd
import snowflake.connector
import pandas as pd
from snowflake.snowpark.session import Session

uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, label_visibility='hidden')
if uploaded_file is not None:
  # Convert image base64 string into hex 
  bytes_data_in_hex = uploaded_file.getvalue().hex()

  # Generate new image file name
  file_name = 'img_' + str(uuid.uuid4())

  # Write image data in Snowflake table
  df = pd.DataFrame({"id": [file_name], "item": [bytes_data_in_hex]})
  session.write_pandas(df, "clothes_table")
