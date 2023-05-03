import streamlit as st 
import json
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import matplotlib.pyplot as plt


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
    '''non fa nulla oltre che controllare un json'''
    auth = False
    with open("resource/users.json") as json_file:
        users = json.load(json_file)
        print(users)
    
        i = 0
        while(i < len(users) and not auth):
            print(users[i])
            if (users[i]["user_name"] == user and users[i]["password"] == password):
                auth = True
    return auth

def import_file_csv():
    '''carica file csv in un pandas dataframe'''
    my_file = st.file_uploader("Select the csv file:")
    imported = pd.DataFrame()
    if(my_file):
        try:
            df = pd.read_csv(my_file)
            st.write(df)
            imported = df
        except:
            st.markdown(f"""
            **Something went wrong**

            you can check what you trying to upload:
            - Type {my_file.type}
            - name {my_file.name}
            """, unsafe_allow_html=True)
        lnk = "streamlit/pages/step1.py"
        #go_on = st.bu
        #st.write(df)




def footer():
    st.write("page is ended... useful stuff usually goes here!")

def main() -> None:

    header()
    
    #Between header and footer the juicy interiors
    input_data = st.container()
    method = input_data.selectbox("type of file/data you want to import: ", ["none", "file csv", "link csv", "copy/paste", "OCR"])
    
    if method == "file csv":
        import_file_csv()
        
    elif method == "OCR":
        st.image("resource/tenor.gif")
    
    elif method == "link csv":
        url = st.text_input("Link to csv file")
        df = pd.DataFrame()
        if url != '':
            try:
                df = pd.read_csv(url)
            except:
                st.write("something went wrong, check the link please!")
        
        ##ripulisco il dataframe
        df = df.iloc[0:-1] # elimino la rocket science
        df = df.rename(columns={"medv": "price"}) # rinomino la colonna
        df = df.astype(dtype="float64") # conversione dei tipi 
        print(df.info())

        st.write(df)

        st.header("EDA:")
        st.markdown("## Correlation Matrix")

        df.corr()
        fig = plt.figure()
        sns.heatmap(df.corr(), annot=True)
        st.pyplot(fig)

        # fig1 = plt.figure()
        # sns.pairplot(df, hue="price")
        # st.pyplot(fig1)
        

        st.markdown("Crim against Price:")
        fig2 = plt.figure()
        sns.jointplot(x=df["crim"], y=df["price"])
        st.pyplot(fig2)

        st.markdown("## Creazione Modello: ")

        X = df.drop(columns="price") # feature
        y = df["price"] # target
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.33)

        


        


        #st.write(df)


    


    footer()

if __name__ == '__main__': 
    main()