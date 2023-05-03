import streamlit as st 
import json
import pandas as pd
from hashlib import sha256

from pages import step1

def header():
    head = st.container()
    head.header("Welcome!")
    login = st.expander("Login")
    user = login.text_input("Username: ", key="user")
    psw = login.text_input("password: ", key="psw")
    log_btn = login.button("Log In")
    if(log_btn):
        #st.write("button pressed", user, psw)
        if(authenticate(user, psw)):
            st.balloons()

def authenticate(user, password) -> bool:
    auth = False
    with open("resource/users.json") as json_file:
        users = json.load(json_file)
        print(users)
    
        i = 0
        while(i < len(users) and not auth):
            print(users[i])
            if (users[i]["user_name"] == user and users[i]["password"]):
                auth = True
    return auth
def import_file_csv():
    my_file = st.file_uploader("Select the csv file:")
    if(my_file):
        try:
            df = pd.read_csv(my_file)
            st.write(df)
            
        except:
            st.markdown(f"""
            **Something went wrong**

            instead of mopping you can check what you trying to upload:
            - Type {my_file.type}
            - name {my_file.name}
            """)
        lnk = "streamlit/pages/step1.py"
        #go_on = st.button(lbl)
        st.markdown(f'''
        <a href={lnk}><button>Next Step</button></a>''',
        unsafe_allow_html=True)

def footer():
    st.write("Yo page is ended... useful stuff usually goes here!")

def main() -> None:

    header()
    
    #Between header and footer the juicy interiors
    input_data = st.container()
    method = input_data.selectbox("type of file/data you want to import: ", ["none", "csv", "copy/paste", "OCR"])
    if method == "csv":
        import_file_csv()
        

    elif method == "OCR":
        st.image("resource/tenor.gif")
        st.write("https://youtu.be/dQw4w9WgXcQ?t=42")

    


    footer()

if __name__ == '__main__': 
    main()