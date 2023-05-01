from snowflake.snowpark.session import Session
import streamlit as st
import pandas as pd
import numpy as np
import uuid
from PIL import Image
import snowflake.connector
import io

st.set_page_config(page_title="A Cloud Closet", page_icon=":dress:", layout="wide")
my_color_list = ["Blue", "Red", "White", "Black", "Green", "Yellow", "Purple", "Pink", "Grey"]
my_item_list = ["Sweater", "Trousers", "T-Shirt", "Shorts"]

def connect_to_snowflake():
    """Establishes a connection to your Snowflake database"""
    return Session.builder.configs(st.secrets["snowflake"]).create()

def logout():
    """Logs out the user"""
    st.write("Logout clicked")

def login():
    """Logs in the user"""
    CORRECT_USERNAME = "username"
    CORRECT_PASSWORD = "password"

    if 'login' not in st.session_state:
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
        """Displays the sidebar menu"""
        with st.sidebar:
            option_icons = {
                "Home": "house",
                "Upload Clothes": "box-arrow-in-up",
                "Pick me an outfit": "palette-fill",
                "Give me some stats": "bar-chart-fill",
                "Settings": "gear"
            }
            selected = st.selectbox("Main Menu", options=list(option_icons.keys()), index=0, key="sidebar")
            return selected

# def sidebar():
#     """Displays the sidebar menu"""
#     with st.sidebar:
#         option_icons = {
#             "Home": "house",
#             "Upload Clothes": "box-arrow-in-up",
#             "Pick me an outfit": "palette-fill",
#             "Give me some stats": "bar-chart-fill",
#             "Settings": "gear"
#         }
#         selected = st.selectbox("Main Menu", options=list(option_icons.keys()), index=0, key="sidebar")
#         return selected

def home():
    """Displays the Home page"""
    st.title("Home page")
    st.header("This is the Home page.")
    st.subheader("1) Upload your photos")
    st.write("Upload your clothes photos in the app")
    st.subheader("2) Generate an outfit")
    st.write("Click to generate an outfit")
    st.subheader("3) Manage your wardrobe")
    st.write("See which clothes you never wear")

def upload_clothes():
    """Displays the Upload Clothes page"""
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

    # Upload photo
    st.subheader("3) Upload Photo")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Convert image base64 string into hex
        bytes_data_in_hex = uploaded_file.getvalue().hex()
        # Generate new image file name
        file_name = 'img_' + str(uuid.uuid4())
        # Add a button to load the photo
        if st.button("Submit Photo"):
            if len(item_selected) == 1 and len(colors_selected) > 0:
                st.success("Photo Uploaded")
                # Write image data in Snowflake table
                df = pd.DataFrame({"ID": [file_name], "ITEM": [bytes_data_in_hex], "TYPE": [item_selected[0]], "COLORS": [np.array(colors_selected)]})
                session.write_pandas(df, "CLOTHES_TABLE")
                # Prepare a SQL query to insert the photo data and colors into the appropriate table
                # Use a dynamic SQL query to generate the appropriate number of columns based on the length of the colors_selected list
                # query = "INSERT INTO clothes_table (id, item, type"
                # for i in range(len(colors_selected)):
                #     query += f", color{i+1}"
                # query += ") VALUES ('{id}', '{bytes_data}', '{item_selected}'"
                # for color in colors_selected:
                #     query += f", '{color}'..."
                # query += ")"
                

                    # Close the database connection
#                     cnx.close()
            else:
                st.error("Error")
                
                
def generate_top(cnx, top_type):
    with cnx.cursor() as my_cur:
        my_cur.execute(f"SELECT item FROM clothes_table sample row (1 rows) WHERE type = '{top_type}'")
        random_row = my_cur.fetchone()
        hex_str = random_row[0].strip('"')
        byte_str = bytes.fromhex(hex_str)
        image = Image.open(io.BytesIO(byte_str))
        img_top = np.array(image)

        # Check the shape of the image arrays and rotate them if necessary
        if img_top.shape[0] < img_top.shape[1]:
            img_top = np.rot90(img_top, k=3)

        st.image(img_top)

def generate_bottom(cnx, bottom_type):
    with cnx.cursor() as my_cur:
        my_cur.execute(f"SELECT item FROM clothes_table sample row (1 rows) WHERE type = '{bottom_type}'")
        random_row = my_cur.fetchone()
        hex_str = random_row[0].strip('"')
        byte_str = bytes.fromhex(hex_str)
        image = Image.open(io.BytesIO(byte_str))
        img_bottom = np.array(image)

        # Check the shape of the image arrays and rotate them if necessary
        if img_bottom.shape[0] < img_bottom.shape[1]:
            img_bottom = np.rot90(img_bottom, k=3)

        st.image(img_bottom)

def generate_outfit(flag_top, flag_bottom):
    st.title("Generate an outfit")
    st.subheader("This is the Pick me an outfit page.")
#     temperature = st.radio("What's the temperature?", ('Hot', 'Cold'))

#     if temperature == 'Hot':
#         top_type = 'T-Shirt'
#         bottom_type = 'Shorts'
#     else:
#         top_type = 'Sweater'
#         bottom_type = 'Trousers'
    start_generate=False
    with st.expander("Choose temperature", expanded=False):
        hot = st.button("Hot")
        cold = st.button("Cold")
     
        if hot:
            st.write("You selected Hot")
           top_type = 'T-Shirt'
           bottom_type = 'Shorts'
           start_generate=True

        if cold:
           st.write("You selected Cold")
           top_type = 'Sweater'
           bottom_type = 'Trousers'
           start_generate=True
    
    if start_generate==True:
        col1, col2, col3 = st.columns(3)

        # Establish a connection to your Snowflake database
        cnx = snowflake.connector.connect(**st.secrets["snowflake"])

        with col1:
            st.header("Top")
            if flag_top == True:
                generate_top(cnx, top_type)

        with col2:
            st.header("Bottom")
            if flag_bottom == True:
                generate_bottom(cnx, bottom_type)

        with col3:
            placeholder_like = st.empty()
            placeholder_dislike = st.empty()
            if 'preference' not in st.session_state:
                st.session_state['preference'] = 0

            if 'button' not in st.session_state:
                col4, col5 = st.columns(2)

                with col4:
                    for i in range(16):
                        st.write("")

    #                 placeholder_like = st.empty()

                    with placeholder_like:
                        like = st.button("Like :thumbsup:", use_container_width=True)
                        if like:
                            st.session_state['button'] = True
                            st.session_state['preference'] = 1

                with col5:
                    for j in range(16):
                        st.write("")

    #                 placeholder_dislike = st.empty()

                    with placeholder_dislike:
                        dislike = st.button("Dislike :thumbsdown:", use_container_width=True)
                        if dislike:
                            st.session_state['button'] = True
                            st.session_state['preference'] = -1

            if 'button' in st.session_state:
                placeholder_like.empty()
                placeholder_dislike.empty()

                col6, col7, col8 = st.columns(3)

                with col6:
                    if st.session_state.preference == -1:
                        top = st.button("Generate Top", use_container_width=True)
                        if top:
                            generate_outfit(flag_top=True, flag_bottom=False)

                with col7:
                    if st.session_state.preference == 1:
                        st.success("Preference saved!")
                    if st.session_state.preference == -1:
                        bottom = st.button("Generate Bottom", use_container_width=True)
                        if bottom:
                            generate_outfit(flag_top=False, flag_bottom=True)

                with col8:
                   if st.session_state.preference == -1:
                        outfit = st.button("Generate Outfit", use_container_width=True)
                        if outfit:
                            generate_outfit(flag_top=True, flag_bottom=False)

                
# def generate_outfit():
#     st.title("Generate an outfit")
#     st.subheader("This is the Pick me an outfit page.")
#     temperature = st.radio("What's the temperature?", ('Hot', 'Cold'))

#     if temperature == 'Hot':
#         top_type = 'T-Shirt'
#         bottom_type = 'Shorts'
#     else:
#         top_type = 'Sweater'
#         bottom_type = 'Trousers'

#     col1, col2, col3 = st.columns(3)

#     # Establish a connection to your Snowflake database
#     cnx = snowflake.connector.connect(**st.secrets["snowflake"])

#     with col1:
#         st.header("Top")
#         with cnx.cursor() as my_cur:
#             my_cur.execute(f"SELECT item FROM clothes_table sample row (1 rows) WHERE type = '{top_type}'")
#             random_row = my_cur.fetchone()
#             hex_str = random_row[0].strip('"')
#             byte_str = bytes.fromhex(hex_str)
#             image = Image.open(io.BytesIO(byte_str))
#             img_top = np.array(image)

#             # Check the shape of the image arrays and rotate them if necessary
#             if img_top.shape[0] < img_top.shape[1]:
#                 img_top = np.rot90(img_top, k=3)

#             st.image(img_top)

#     with col2:
#         st.header("Bottom")
#         with cnx.cursor() as my_cur:
#             my_cur.execute(f"SELECT item FROM clothes_table sample row (1 rows) WHERE type = '{bottom_type}'")
#             random_row = my_cur.fetchone()
#             hex_str = random_row[0].strip('"')
#             byte_str = bytes.fromhex(hex_str)
#             image = Image.open(io.BytesIO(byte_str))
#             img_bottom = np.array(image)

#             # Check the shape of the image arrays and rotate them if necessary
#             if img_bottom.shape[0] < img_bottom.shape[1]:
#                 img_bottom = np.rot90(img_bottom, k=3)

#             st.image(img_bottom)

#     with col3:
#         if 'preference' not in st.session_state:
#             st.session_state['preference'] = 0

#         if 'button' not in st.session_state:
#             col4, col5 = st.columns(2)

#             with col4:
#                 for i in range(16):
#                     st.write("")

#                 placeholder_like = st.empty()

#                 with placeholder_like:
#                     like = st.button("Like :thumbsup:", use_container_width=True)
#                     if like:
#                         st.session_state['button'] = True
#                         st.session_state['preference'] = 1

#             with col5:
#                 for j in range(16):
#                     st.write("")

#                 placeholder_dislike = st.empty()

#                 with placeholder_dislike:
#                     dislike = st.button("Dislike :thumbsdown:", use_container_width=True)
#                     if dislike:
#                         st.session_state['button'] = True
#                         st.session_state['preference'] = -1

#         if 'button' in st.session_state:
#             placeholder_like.empty()
#             placeholder_dislike.empty()

#             col6, col7, col8 = st.columns(3)

#             with col6:
#                 if st.session_state.preference == -1:
#                     st.button("Generate Top", use_container_width=True)

#             with col7:
#                 if st.session_state.preference == 1:
#                     st.success("Preference saved!")
#                 if st.session_state.preference == -1:
#                     st.button("Generate Bottom", use_container_width=True)

#             with col8:
#                if st.session_state.preference == -1:
#                     outfit = st.button("Generate Outfit", use_container_width=True)
                        
            
def stats():
    return
def settings():
    return
if __name__ == '__main__':
    # Connect to Snowflake
    session = connect_to_snowflake()

    # Log in the user
#     login()
    selected = login()
    if selected == "Home":
        home()
    elif selected == "Upload Clothes":
        upload_clothes()
    elif selected == "Pick me an outfit":
        generate_outfit(flag_top=True, flag_bottom=True)
    elif selected == "Give me some stats":
        stats()
    elif selected == "Settings":
        settings()

#     # If login is successful, display the sidebar menu
#     if 'login' in st.session_state and st.session_state['login']:
#         # Set page config
# #         st.set_page_config(page_title="A Cloud Closet", page_icon=":dress:", layout="wide")

#         # Display the sidebar menu
#         while True:
#             selected = sidebar()
#             if selected == "Home":
#                 home()
#             elif selected == "Upload Clothes":
#                 upload_clothes()
# #             elif selected == "Pick me an outfit":
# #                 pick_outfit()
# #             elif selected == "Give me some stats":
# #                 stats()
# #             elif selected == "Settings":
# #                 settings()

# cnx.close()
            
