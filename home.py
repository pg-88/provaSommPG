import seaborn as sns
import streamlit as st 
import json
import pandas as pd
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




        


        #st.write(df)
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

def get_eq_str(intercept, betas, datafrtame):
    eq_str = f"{round(intercept, 2)} "
    for c in range(betas.size):
        beta = round(betas[c],2)
        col = datafrtame.columns[c]
        eq_str += f"+ {beta} * {col}"

    return eq_str

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
            sns.scatterplot(x=df["crim"], y=df["price"])
            st.pyplot(fig2)

            st.markdown("## Creazione Modello: ")
            X = df.drop(columns="price") # feature
            y = df["price"] # target
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.33)

            price_model = LinearRegression(fit_intercept=True)
            price_model.fit(X_train, y_train)
            coeff = price_model.coef_
            intercept = price_model.intercept_

            st.write(get_eq_str(intercept,coeff,df))

            joblib.dump(price_model, "price.pkl")
            st.write("model at: price.pkl")

            y_pred = price_model.predict(X_test)
            y_arr = y_test.to_numpy()
            test = pd.DataFrame(y_test.to_numpy(), columns=["Test Set"])
            pred = pd.DataFrame(y_pred, columns=["Prediction Set"])

            fig3 = plt.figure()
            sns.lineplot(y_pred)
            sns.lineplot(y_arr)
            st.pyplot(fig3)

            st.metric("Model Errors R²", round(r2_score(y_test, y_pred),4))
            st.metric("Mean Absolute Error", round(mean_absolute_error(y_test, y_pred), 3))
            st.metric("Mean Squared Error", round(mean_squared_error(y_test, y_pred),3))
            st.metric("Root Mean Square Root", round(mean_squared_error(y_test, y_pred, squared=True),3))

            model = joblib.load("price.pkl")
            
            inserted = []
            cols = df.columns
            st.write(cols)

            for c in range(cols.size):
                inserted.append(st.number_input(f"Value for {cols[c]}"))
                

            ins = pd.DataFrame(inserted)

            st.write(ins)
            
            model.predict()
    


    footer()

if __name__ == '__main__': 
    main()