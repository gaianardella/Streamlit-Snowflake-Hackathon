from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
import numpy as np
import uuid
# from io import StringIO
from PIL import Image
import snowflake.connector
# import base64
import io
# import os
from PIL import Image
import random
# import json
import matplotlib.image as mpimg


st.set_page_config(page_title="A Cloud Closet", page_icon=":dress:", layout="wide")
my_color_list=["Blue", "Red", "White", "Black", "Green", "Yellow", "Purple", "Pink"]
my_item_list=["Sweater", "Trousers", "T-Shirt", "Shorts"]

# Establish a connection to your Snowflake database
session = Session.builder.configs(st.secrets["snowflake"]).create()


# --- USER AUTHENTICATION ---

# Define the logout function
def logout():
    # Add logout logic here
    # For example, you can clear session data or redirect to a login page
    st.write("Logout clicked")

# Define username and password
CORRECT_USERNAME = "username"
CORRECT_PASSWORD = "password"


if 'login' not in st.session_state:
   # Create a title and subheader
    st.title("Login Page")
    st.subheader("Enter your credentials to log in.")
    login_form = st.form(key='login_form')
    username = login_form.text_input(label='username')
    password = login_form.text_input(label='password', type='password')
    submit_button = login_form.form_submit_button(label='submit')


    if submit_button:
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.session_state.username = username
            st.session_state['login'] = True
            st.success("You have successfully logged in.")
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')

if 'login' in st.session_state:
    st.empty()
    # Display the sidebar menu
    with st.sidebar:
        option_icons = {
            "Home": "house",
            "Upload Clothes": "box-arrow-in-up",
            "Pick me an outfit": "palette-fill",
            "Give me some stats": "bar-chart-fill",
            "Settings": "gear"
        }
        selected = st.selectbox("Main Menu", options=list(option_icons.keys()), index=0)

    # Display the selected page
    if selected == "Home":
        st.title("Home page")
        st.header("This is the Home page.")
        st.subheader("1) Upload your photos")
        st.write("Upload your clothes photos in the app")
        st.subheader("2) Generate an outfit")
        st.write("Click to generate an outfit")
        st.subheader("3) Manage your wardrobe")
        st.write("See which clothes you never wear")
    elif selected == "Upload Clothes":
        st.title("Upload your clothes")
        st.subheader("This is the Upload Clothes page.")
        
        # Let's put a pick list here so they can pick the fruit they want to include
        st.subheader("1) Pick Item")
        item_selected = st.multiselect("Pick item:", list(my_item_list), ['Sweater'])
        if len(item_selected) == 1:
            st.write("You selected: " + item_selected[0])
    
        else:
            st.error("Select only one item")
                
        st.subheader("2) Pick Color")   
        colors_selected = st.multiselect("What color is the item:", list(my_color_list), ['Blue','Red'])
        if len(colors_selected) > 0:
            if len(colors_selected)>1:
                # Join the colors with commas, except for the last on
                colors_string = ', '.join(colors_selected[:-1])
                # Add the last color to the string
                colors_string += ' and ' + colors_selected[-1]
            else:
                colors_string = colors_selected[0]
            # Write color string
            st.write("You selected: "+ colors_string)
                
        else:
            st.error("Insert Colors")
        
        st.subheader("3) Upload Photo")  
        #single file uploader (doesn't accept more than one file)
        
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
          
           
            # Convert image base64 string into hex 
            bytes_data_in_hex = uploaded_file.getvalue().hex()
            # Generate new image file name
            file_name = 'img_' + str(uuid.uuid4())

            
            #Add a button to load the photo
            if st.button("Submit Photo"):
                if len(item_selected) == 1 and len(colors_selected)>0:   
                    st.success("Photo Uploaded")
                    
                    # Write image data in Snowflake table
                    df = pd.DataFrame({"ID": [file_name], "ITEM": [bytes_data_in_hex], "TYPE": [item_selected[0]], "COLORS": [np.array(colors_selected)]})
                    session.write_pandas(df, "CLOTHES_TABLE")
                    
                    # Prepare a SQL query to insert the photo data and colors into the appropriate table
                    # Use a dynamic SQL query to generate the appropriate number of columns based on the length of the colors_selected list
#                     query = "INSERT INTO clothes_table (id, item, type"
#                     for i in range(len(colors_selected)):
#                         query += f", color{i+1}"
#                     query += ") VALUES ('{id}', '{bytes_data}', '{item_selected}'"
#                     for color in colors_selected:
#                         query += f", '{color}'"
#                     query += ")"
                    
#                     # Execute the SQL query using the established connection and the photo data
#                     cnx.cursor().execute(query)

                    # Close the database connection
#                     cnx.close()
                else:
                    st.error("Error")
            
                

    elif selected == "Pick me an outfit":
        st.title("Generate an outfit")
        st.subheader("This is the Pick me an outfit page.")
        temperature = st.radio("What\'s the temperature?",('Hot', 'Cold'))

        if temperature == 'Hot':
            st.write('You selected hot.')
        else:
            st.write('You selected cold.')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Top")
            if temperature == 'Hot':
                # Execute the SQL query to select a random record with type = 'Sweater'
#                 df =session.sql("SELECT item FROM clothes_table WHERE type = 'Sweater'")
#                 df = session.table("clothes_table").filter(col("TYPE")=="Sweater").select(col("ITEM"))
#                 row=df.sample(n = 1).collect()[0].ITEM
                

                # Establish a connection to your Snowflake database
                cnx = snowflake.connector.connect(**st.secrets["snowflake"])

                with cnx.cursor() as my_cur:
                    my_cur.execute("SELECT item FROM clothes_table sample row (1 rows) WHERE type = 'Sweater'")
                    random_row = my_cur.fetchone()
                    hex_str = random_row[0].strip('"')                    
                    byte_str = bytes.fromhex(hex_str)
                    image = Image.open(io.BytesIO(byte_str))
                    
                    img2 = np.array(image)

                    # Check the shape of the image arrays and rotate them if necessary
                    if img2.shape[0] < img2.shape[1]:
                        img2 = np.rot90(img2, k=3)



                        st.image(img2)
                    st.stop()
                    
                     








                # Establish a connection to your Snowflake database
#                 cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#                 with cnx.cursor() as my_cur:
#                     my_cur.execute("SELECT * FROM clothes_table WHERE type = 'Sweater'")
#                     byte_array=my_cur.fetchall()
#                     random_byte_array = random.choice(byte_array)
#                     st.write(random_byte_array[1])
#                     li=[]
#                     st.stop()
#                     for el in byte_array:
# #                         if el[0] == id:
#                             byte_array=el[1]
#                             li.append(byte_array)
#                     st.write(str(li))
#                             item=el[2]
#                             colors=el[3]
#                             #se più di un colore
#                             #if "," or "and" in colors
#                             st.write(colors.split(","))
#                             image = Image.open(io.BytesIO(byte_array))
#                             st.image(image)


                st.stop()
                
                # Extract the binary data from the 'item' column
#                 bytes_data = bytes.fromhex(row['item'][0])
#                 st.write(row['item'][0])

                # Extract the 'item' value from the randomly selected row
                item_value = row['item'].collect()
                st.write(item_value)
                st.stop()
                top = Image.open('sweater.jpeg')
                st.image(top, width=340)
                
                
            

        with col2:
            st.header("Bottom")
            bottom = Image.open('trousers.jpeg')
            st.image(bottom, width=340)

      
        with col3:
            var=-1
            # if st.button("I don't like it", key="dislike"):
            #     show_generate=True
            # if st.button("I like it", key="like"):
            #     show_generate=False

            st.markdown("""
                <style>
                    div.stButton > button:first-child {
                        text-align:center;
                        background-color: #FF6347;
                        padding-left: 20px;
                        padding-right: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%; /* set the height of the container to 100% */
                    }
                </style>
            """, unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            if st.button("Disike"):
                var = 0

            st.markdown("""
                <style>
                    div.stButton > button:first-child {
                        text-align:center;
                        background-color: #00FF00;
                        padding-left: 20px;
                        padding-right: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%; /* set the height of the container to 100% */
                    }
                </style>
            """, unsafe_allow_html=True)
            if st.button("Like"):
                var = 1
        
        if var==1:
            st.write("Cool!")
        elif var == 0:
            st.write("generate again")
            

     
    elif selected == "Give me some stats":
        st.title("Stats")
        st.subheader("This is the Give me some stats page.")
    elif selected == "Settings":
        st.title("Settings")
        st.subheader("This is the Settings page.")

#cnx.close()





