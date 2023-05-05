from snowflake.snowpark.session import Session
import streamlit as st
import pandas as pd
import numpy as np
import uuid
from PIL import Image
import snowflake.connector
import io
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

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
        st.title("Welcome to you cloud closet! :cloud:")
        st.subheader("Enter your credentials to log in :closed_lock_with_key:")
        login_form = st.form(key='login_form')
        username = login_form.text_input(label='**Username**', value="username")
        password = login_form.text_input(label='**Password**', type='password', value="password")
        submit_button = login_form.form_submit_button(label='Submit')

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
#         """Displays the sidebar menu"""
        with st.sidebar:
            option_icons = {
                "Home": "house",
                "Upload Clothes": "box-arrow-in-up",
                "Pick me an outfit": "palette-fill",
                "Give me some stats": "bar-chart-fill",
                "Manage your closet": "gear"
            }
            selected = st.selectbox("Main Menu", options=list(option_icons.keys()), index=0, key="sidebar")
            return selected

def home():
    """Displays the Home page"""
    st.title("Home page :house:")
    st.header("Welcome to your cloud closet! :cloud: :dress:")
    st.write("Welcome to our clothing management app! With our app, you can easily upload your clothing photos and save them to our secure Snowflake database. Here's a step-by-step guide to using our app:")
    st.divider()
    st.subheader(":one: Upload your photos :camera_with_flash:")
    st.write("    Start by choosing the type of clothing and its color that you want to upload. Simply click on the 'Upload' button and select the photo from your device. Your photo will be saved securely in our Snowflake database.")
    st.divider()
    st.subheader(":two: Generate an outfit :tshirt: :jeans:")
    st.write("    Our app allows you to generate an outfit for both hot and cold temperatures. You can select the temperature and choose from a variety of clothing items to create the perfect outfit for any occasion.")
    st.divider()
    st.subheader(":three: Manage your wardrobe :hammer_and_wrench:")
    st.write("    With our app, you can easily manage your wardrobe by checking which items you like the most and the least. You can also remove items that you no longer need or add new items to your collection.")
    st.write("Our clothing management app is designed to make it easy for you to manage your wardrobe and create stylish outfits for any occasion. Start using our app today to simplify your clothing management process!")
def upload_clothes():
    """Displays the Upload Clothes page"""
    st.title("Upload your clothes :camera_with_flash:")
    st.subheader("This is the Upload Clothes page.")
        
    # Let's put a pick list here so they can pick the fruit they want to include
    #vedere se usare st.form()
#     st.subheader("1) Pick Item")
    item_selected = st.multiselect("**1) Pick Item :womans_clothes: :shorts:**", list(my_item_list), ['Sweater'])
    if len(item_selected) == 1:
        st.write(f"You selected: _{item_selected[0]}_") #inserire icona vestito

    else:
        st.error("Select only one item")
    
    st.divider()
                
#     st.subheader("2) Pick Colors")   
    colors_selected = st.multiselect("**2) Pick Colors :large_yellow_square: :large_green_square:**", list(my_color_list), ['Blue','Red'])
    if len(colors_selected) > 0:
        if len(colors_selected)>1:
            # Join the colors with commas, except for the last on
            colors_string = ', '.join(colors_selected[:-1])
            # Add the last color to the string
            colors_string += ' and ' + colors_selected[-1]
        else:
            colors_string = colors_selected[0]
        # Write color string
        st.write(f"You selected: _{colors_string}_") #:blue[colors] per scrivere la parola colors di colore blu
    else:
        st.error("Insert Colors")
        
    st.divider()

    # Upload photo
#     st.subheader("3) Upload Photo")
    uploaded_file = st.file_uploader("**3) Upload Photo :outbox_tray:**") #Choose a file
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
                df = pd.DataFrame({"ID": [file_name], "ITEM": [bytes_data_in_hex], "TYPE": [item_selected[0]], "COLORS": [np.array(colors_selected)], "LIKES":[0], "DISLIKES":[0]})
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
                st.error("Please select an item and color(s) before uploading a photo.")

def choose_temperature():
    st.title("Generate an outfit :dress::necktie:")
    st.subheader("This is the Pick me an outfit page.")
    with st.expander("**Select Temperature** :fire: :snowflake:", expanded=True):
        temperature = st.radio("What's the temperature?", ('Hot', 'Cold'))
        if temperature == 'Hot':
            st.write("**You selected: Hot :fire:**")
        elif temperature == 'Cold':
            st.write("**You selected: Cold :snowflake:**")
    st.divider()
    return temperature


def colors(colors_top,colors_bottom):
    # Convert the color names into numerical values
    color_dict = {'black': 0, 'white': 1, 'grey': 2, 'red': 3, 'blue': 4, 'green': 5, 'yellow': 6, 'purple': 7, 'pink': 8}

    

@st.cache_resource
def generate_top_bottom(top_type,bottom_type):
    #     # Establish a connection to your Snowflake database
    items_strings=[top_type,bottom_type]
    top_colors=[]
    bottom_colors=[]
    items={"items_hex":[], "items_bytes":[]}
    cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    with cnx.cursor() as my_cur:
        for item in items_strings:
            my_cur.execute(f"SELECT item,colors FROM clothes_table sample row (1 rows) WHERE type = '{item}'")
            random_row = my_cur.fetchone()
            colors = random_row[1].strip("[").strip("]").split(",")
            colors = colors.replace('"','')
            for color in colors:
                strip_color=color.strip('"')
                if item == "Sweater" or item=="T-Shirt":
                    top_colors.append(strip_color)
                elif item == "Trousers" or item=="Shorts":
                    bottom_colors.append(strip_color)
            st.write(top_colors)
            st.write(bottom_colors)
                
#             st.write(colors)
             #SELEZIONARE COLORI
           #funzione contorllo colori e restituisce true e continua oppure false e richiama generate_top_bottom
            #colors=[]
            #VEDERE RECORD TARGET
            hex_str = random_row[0].strip('"')
            items["items_hex"].append(hex_str)
            byte_str = bytes.fromhex(hex_str)
            image = Image.open(io.BytesIO(byte_str))
            img = np.array(image)
            # Check the shape of the image arrays and rotate them if necessary
            if img.shape[0] < img.shape[1]:
                img = np.rot90(img, k=3)
            items["items_bytes"].append(img)
    cnx.close()    
    return items


def generate_outfit(temperature, flag_top, flag_bottom):
    if temperature == 'Hot':
        top_type = 'T-Shirt'
        bottom_type = 'Shorts'
    elif temperature == 'Cold':
        top_type = 'Sweater'
        bottom_type = 'Trousers'
        
    if 'top_bottom' not in st.session_state:
            st.session_state.top_bottom = True
    #devo ancora generare
    if st.session_state.top_bottom==True:  #(if st.session_state.top == True)
        #lista [top,bottom]
        images=generate_top_bottom(top_type,bottom_type)    
            
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Top :tshirt:")
        st.image(images["items_bytes"][0])
    with col2:
        st.header("Bottom :jeans:")
        st.image(images["items_bytes"][1])
    with col3:
        for i in range(16):
            st.write("")
        like = st.button("**Like :thumbsup:**", use_container_width=True)
        if like:
            st.session_state.top_bottom=False
            st.success("Preference saved!")
            cnx = snowflake.connector.connect(**st.secrets["snowflake"])
            with cnx.cursor() as my_cur:
                my_cur.execute(f"UPDATE clothes_table SET LIKES = LIKES + 1 WHERE ITEM = '{images['items_hex'][0]}'")
                my_cur.execute(f"UPDATE clothes_table SET LIKES = LIKES + 1 WHERE ITEM = '{images['items_hex'][1]}'")
            cnx.close()
#             home_button=st.button("Return home :arrow_right:", use_container_width=True)
#             if home_button:
#                 home()
            
        dislike = st.button("**Dislike :thumbsdown:**", use_container_width=True)
        if dislike:
            cnx = snowflake.connector.connect(**st.secrets["snowflake"])
            with cnx.cursor() as my_cur:
                my_cur.execute(f"UPDATE clothes_table SET DISLIKES = DISLIKES + 1 WHERE ITEM = '{images['items_hex'][0]}'")
                my_cur.execute(f"UPDATE clothes_table SET DISLIKES = DISLIKES + 1 WHERE ITEM = '{images['items_hex'][1]}'")
            cnx.close()
            st.cache_resource.clear()
            
            

#     with col2:
#         st.header("Bottom")
#         if flag_bottom == True:
# #             generate_bottom(cnx, bottom_type)
#             img_bottom=generate_bottom(bottom_type)
#         st.image(img_bottom)
#     with col3:
#         for i in range(15):
#             st.write("")
# #         placeholder_like = st.empty()
# #         placeholder_dislike = st.empty()
#         if 'preference' not in st.session_state:
#             st.session_state['preference'] = 0

#         if 'button' not in st.session_state:
#             col4, col5 = st.columns(2)

#             with col4:
# #                 for i in range(60):
# #                     st.write("")

#                 placeholder_like = st.empty()
#                 with placeholder_like:
#                     like = st.button("Like :thumbsup:", use_container_width=True, on_click=callback())
#                     if like:
#                         st.session_state['button'] = True
#                         st.session_state['preference'] = 1

#             with col5:
# #                 for j in range(16):
# #                     st.write("")

#                 placeholder_dislike = st.empty()
# #                 with placeholder_dislike:
# #                     dislike = st.button("Dislike :thumbsdown:", use_container_width=True)
# #                     if dislike:
# #                         st.session_state['button'] = True
# #                         st.session_state['preference'] = -1

#         if 'button' in st.session_state:
# #             placeholder_like.empty()
# #             placeholder_dislike.empty()
# #             st.empty()

#             col6, col7, col8 = st.columns(3)
# #             placeholder_like.empty()
# #             placeholder_dislike.empty()

# #             with col6:
# #                 if st.session_state.preference == -1:
# #                     top = st.button("Generate Top", use_container_width=True)
# #                     if top:
# #                         for key in st.session_state.keys():
# #                             del st.session_state[key]
# #                         generate_outfit(temperature, flag_top=True, flag_bottom=False)

#             with col7:
#                 if st.session_state.preference == 1:
#                     st.success("Preference saved!")
#                 if st.session_state.preference == -1:
#                     bottom = st.button("Generate Bottom", use_container_width=True)
#                     if bottom:
#                         for key in st.session_state.keys():
#                             if key=="button" or key=="preference":
#                                 del st.session_state[key]
#                         generate_outfit(temperature, flag_top=False, flag_bottom=True)

#             with col8:
#                if st.session_state.preference == -1:
#                     outfit = st.button("Generate Outfit", use_container_width=True)
#                     if outfit:
#                         for key in st.session_state.keys():
#                             del st.session_state[key]
#                         generate_outfit(temperature, flag_top=True, flag_bottom=False)
                        

    
def stats():
    st.title("Stats Page :bar_chart:")
    st.header("This is the Stats page.")
    #Ordina sql in base a lke/dislike e scegli i primi 3
    # Execute the query
    cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    with cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM clothes_table ORDER BY LIKES DESC LIMIT 3")
        likes=[]
        rows=my_cur.fetchall()
        for row in rows:
            file=row[1]
#             st.write(id)
            hex_str = file.strip('"')
            byte_str = bytes.fromhex(hex_str)
            image = Image.open(io.BytesIO(byte_str))
            img = np.array(image)
            # Check the shape of the image arrays and rotate them if necessary
            if img.shape[0] < img.shape[1]:
                img = np.rot90(img, k=3)
            likes.append(img)
        
        my_cur.execute("SELECT * FROM clothes_table ORDER BY LIKES ASC LIMIT 3")
        dislikes=[]
        rows=my_cur.fetchall()
        for row in rows:
            file=row[1]
#             st.write(id)
            hex_str = file.strip('"')
            byte_str = bytes.fromhex(hex_str)
            image = Image.open(io.BytesIO(byte_str))
            img = np.array(image)
            # Check the shape of the image arrays and rotate them if necessary
            if img.shape[0] < img.shape[1]:
                img = np.rot90(img, k=3)
            dislikes.append(img)
    
#     st.write("Your favourite items: ")
    with st.expander("**Your favourite items :heart: :dress:**", expanded=True):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.image(likes[0], width=300)
        with col2:
            st.image(likes[1], width=300)
        with col3:
            st.image(likes[2], width=300)
    st.divider()
#     st.write("Your least favourite items: ")
    with st.expander("**Your least favourite items :x: :dress:**", expanded=True):
        col4,col5,col6 = st.columns(3)
        with col4:
            st.image(dislikes[0], width=300)
        with col5:
            st.image(dislikes[1], width=300)
        with col6:
            st.image(dislikes[2], width=300)
    st.divider()
    #controllo colori
    st.write("**Your favourite colors :heart: :rainbow:**")
    st.divider()
    st.write("**Your least favourite colors :x: :rainbow:**")
    # Close the connection
    cnx.close()
    
    return
def delete_clothes():
    st.title("Manage your wardrobe :hammer_and_wrench:")
    st.header("Here you can delete the clothes you don't wear anymore")
    clothes_selected = st.multiselect("**Pick Clothes :womans_clothes: :shorts:**", list(my_item_list), ['Sweater'])
    if len(clothes_selected) > 0:
        if len(clothes_selected)>1:
            # Join the colors with commas, except for the last on
            clothes_string = ', '.join(clothes_selected[:-1])
            # Add the last color to the string
            clothes_string += ' and ' + clothes_selected[-1]
        else:
            clothes_string = clothes_selected[0]
        # Write color string
        st.write(f"You selected: _{clothes_string}_")
    else:
        st.error("Select Items")
        
    cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    with cnx.cursor() as my_cur:
        column=[]
        for item in clothes_selected:
            my_cur.execute(f"SELECT item FROM clothes_table WHERE type = '{item}'")
            rows=my_cur.fetchall()
            for row in rows:
                file=row[0]
                hex_str = file.strip('"')
                byte_str = bytes.fromhex(hex_str)
                image = Image.open(io.BytesIO(byte_str))
                img = np.array(image)
                # Check the shape of the image arrays and rotate them if necessary
                if img.shape[0] < img.shape[1]:
                    img = np.rot90(img, k=3)
                column.append(img)
                
    cnx.close()
    col1,col2,col3 = st.columns(3)
    checked=[]
    with col1:
        index=1
        for item in column:
            if index == 1:
                st.image(item, width=300)
                box = st.checkbox(label="", value=False, key=item)
                if box:
                    checked.append(item)
            if index ==3:
                index=1
            else:
                index+=1
    with col2:
        index=1
        for item in column:
            if index == 2:
                st.image(item, width=300)
                box = st.checkbox(label="", value=False, key=item)
                if box:
                    checked.append(item)
            if index ==3:
                index=1
            else:
                index+=1
    with col3:
        index=1
        for item in column:
            if index == 3:
                st.image(item, width=300)
                box = st.checkbox(label="", value=False, key=item)
                if box:
                    checked.append(item)
                index=1
            else:
                index+=1
        delete = st.button("Delete")
        cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        if delete:
            with cnx.cursor() as my_cur:
                for item in checked:
                    my_cur.execute(f"DELETE FROM clothes_table WHERE item = '{item}'")
                    #non elimina record, controllare item
            cnx.close()
            st.success("Items succesfully deleted")
            st.experimental_rerun()

# def model():
    
#     url = 'https://github.com/gaianardella/Streamlit-Snowflake-Hackathon/blob/main/color_pairs.csv'
#     df = pd.read_csv(url)
#     # Convert the DataFrame to a Snowpark DataFrame
# #     session.create_dataframe(df)
#     session.write_pandas(df, "COLOR_PAIRS")

    
        # Write image data in Snowflake table
#         df = pd.DataFrame({"ID": [file_name], "ITEM": [bytes_data_in_hex], "TYPE": [item_selected[0]], "COLORS": [np.array(colors_selected)], "LIKES":[0], "DISLIKES":[0]})
                

if __name__ == '__main__':
    # Connect to Snowflake
    session = connect_to_snowflake()
    
    # Convert the DataFrame to a Snowpark DataFrame
#     url = 'https://github.com/gaianardella/Streamlit-Snowflake-Hackathon/blob/main/color_pairs.csv?raw=true'
#     df = pd.read_csv(url)
#     for index, row in df.iterrows():
#         col1 = row['color_1']
#         col2 = row['color_2']
#         col3 = row['target']
#         df = pd.DataFrame({"COLOR_1": [col1], "COLOR_2": [col2], "TARGET": [col3]})
#         session.write_pandas(df, "COLOR_PAIRS")
    
        # Query the data from Snowflake
#         cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#         with cnx.cursor() as cur:
#             cur.execute('SELECT color_1, color_2, target FROM COLOR_PAIRS')
#             rows = cur.fetchall()
#             col_names = [desc[0] for desc in cur.description]

        # Convert the resultset to a pandas DataFrame
#         df = pd.DataFrame(rows, columns=col_names)
        
    
        # Split the data into training and testing sets
#         X_train, X_test, y_train, y_test = train_test_split(df[['color_1', 'color_2']], df['target'], test_size=0.2, random_state=42)


#         # Convert the color names into numerical values
#         color_dict = {'black': 0, 'white': 1, 'grey': 2, 'red': 3, 'blue': 4, 'green': 5, 'yellow': 6, 'purple': 7, 'pink': 8}
#         X_train = X_train.replace(color_dict)
#         X_test = X_test.replace(color_dict)

#         # Create a logistic regression model and fit it to the training data
#         model = LogisticRegression()
#         model.fit(X_train, y_train)

#         serialized_model=pickle.dumps(model)


    # Log in the user
#     login()
    selected = login()
    if selected == "Home":
        home()
    elif selected == "Upload Clothes":
        upload_clothes()
    elif selected == "Pick me an outfit":
        temp=choose_temperature()
        generate_outfit(temp, flag_top=True, flag_bottom=True)
    elif selected == "Give me some stats":
        stats()
    elif selected == "Manage your closet":
        delete_clothes()
        
        #st.experimental_memo

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

#MANCANO: ALGORITMO COLORI, STATISTICHE, RENDERE BELLA L'APP
#CREA USER, DATABASE UTENTI, GLI ITEM DEVONO ESSERE ASSOCIATI AGLI UTENTI, PAGINA DI ELIMINAZIONE ITEM (con checkbox per selezione)
#SCONTORNARE IMMAGINI, DIRE IN HOMEPAGE CHE APP E' CONNESSA A STREAMLIT
