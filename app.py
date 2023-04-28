import streamlit as st
# from streamlit_option_menu import option_menu
# from snowflake.snowpark.session import Session
# from urllib.error import URLError

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="A Cloud Closet", page_icon=":dress:", layout="wide")

my_color_list=["Blue", "Red", "White", "Black", "Green", "Yellow", "Purple", "Pink"]
my_item_list=["Sweater", "Trousers", "T-Shirt", "Shorts"]
# my_color_list = my_color_list.set_index('Color')

# Define the logout function
def logout():
    # Add logout logic here
    # For example, you can clear session data or redirect to a login page
    st.write("Logout clicked")

# --- USER AUTHENTICATION ---

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
            # show_question = True
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')
            # show_question = False
    # else:
    #     show_question = False

if 'login' in st.session_state:
    st.empty()
    # st.write(f"hello, {CORRECT_USERNAME}")
    # if show_question:
    # Display the main page
    # st.title("Hello world!")
    # st.write("Welcome to the main page.")
    
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

#         selected = option_menu("Main Menu", ["Home", "Upload Clothes", "Pick me an outfit", "Give me some stats", "Settings"], 
#             icons=['house', 'box-arrow-in-up', 'palette-fill', 'bar-chart-fill', 'gear'], menu_icon="cast", default_index=0)
