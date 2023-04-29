from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
# import snowflake.connector

st.write("ciao")

# Create Session object
# def create_session_object():
#    connection_parameters = {
#       "account": "<account_identifier>",
#       "user": "<username>",
#       "password": "<password>",
#       "role": "<role_name>",
#       "warehouse": "<warehouse_name>",
#       "database": "ENVIRONMENT_DATA_ATLAS",
#       "schema": "ENVIRONMENT"
#    }
#    session = Session.builder.configs(connection_parameters).create()
#    return session
