# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 17:15:08 2022

@author: Thisu
"""
import pyrebase
import streamlit as st
from datetime import datetime
import joblib
import requests
from streamlit_lottie import st_lottie
import base64

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="SmartCare", page_icon=":elephant:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#lottieMain = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fmgfy8rq.json")
lottieMain = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_xverp39j.json")
lottieSetting = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_qchvuplk.json")
lottieDiab = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_mvdqkcvo.json")

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("data:image/png;base64,%s");
      background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def main():
    
    set_png_as_page_bg('microsoft-surface-duo-2-2560x1440-windows-11-se-microsoft-4k-23875.png')
    # Configuration Key
    
firebaseConfig = {
  'apiKey': "AIzaSyDRwWtwfI7dDiAUxmUDBgfA-fGyoi3jNB8",
  'authDomain': "drbigbot-36eb7.firebaseapp.com",
  'projectId': "drbigbot-36eb7",
  'databaseURL': "https://drbigbot-36eb7-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "drbigbot-36eb7.appspot.com",
  'messagingSenderId': "823848117287",
  'appId': "1:823848117287:web:e820416700ce7c24721a02",
  'measurementId': "G-JR1ZFSXQVB"
};

    
    # Firebase Authentication
    
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
    
    # Database
    
db = firebase.database()
storage = firebase.storage()
    
    #side bar logo
    
st.sidebar.title('SmartCare System')
    #st.sidebar.image("logos/Dr BigBot-logos.jpg", width=300)
    
st_lottie(lottieMain, height=400, key= "main")
    
    # Authentication
    
choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign Up'])
    
email = st.sidebar.text_input('Please input your email')
password = st.sidebar.text_input('Please enter your password', type = 'password')
    
    # App
    
    # Sign up Block
    
if choice == 'Sign Up':
        handle = st.sidebar.text_input('Please input your app handle name', value= 'Default')
        submit = st.sidebar.button('Create my account')
        
        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.success('Your account is created sucsessfully')
            st.balloons()
            #sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome ' + handle)
            st.info('login via login drop down selection')
    
    # Login Block
            
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
        bio = st.radio('Jump to', ['Home', 'Recomandation', 'Settings'])
            
            # SETTINGS PAGE 
#if bio == 'Settings':  
exp1 = st.expander('Input/Change Bio details')
with exp1:   
                    
                      p1 = st.slider('Enter Your Age',18,100)
        
                      p2 = st.number_input("Enter your Fasting Blood Sugar level(mmol/L):")
    
                      p3 = st.number_input("Enter your HbA1c(mmol/mol):")
                                    
save_bio = st.button('Save')
                        
                        
                            
                            
           #sending Diabetes types user data to DB
                            
if save_bio:
          age = db.child(user['localId']).child("p1").push(p1)
          bs_fast = db.child(user['localId']).child("p2").push(p2)
          hb1ac = db.child(user['localId']).child("p3").push(p3)
           
clf = joblib.load('Diabetes_Type_model4')
                
if st.button('Predict', key = "783b046e-7a62-47a7-a64a-c01e8529c03d"):      
 
   db_age = db.child(user['localId']).child("p1").get().val()         
   if db_age is not None:
       val = db.child(user['localId']).child("p1").get()
       for child_val in val.each():
            p1_get = child_val.val()   
   else:
       st.info("No bio data shown yet. Go to setting and provide bio data!")
                              
   db_bs_fast = db.child(user['localId']).child("p2").get().val()         
   if db_bs_fast is not None:
       val = db.child(user['localId']).child("p2").get()
       for child_val in val.each():
            p2_get = child_val.val()   
   else:
       st.info("No bio data shown yet. Go to setting and provide bio data!")
         
                           
   db_hba1c = db.child(user['localId']).child("p3").get().val()
   if db_hba1c is not None:
        val = db.child(user['localId']).child("p3").get()
        for child_val in val.each():
            p3_get = child_val.val()
   else:
        st.info("No bio data shown yet. Go to setting and provide bio data!")                           
               # st_lottie(lottieSetting, height=300, key= "setting")            
                            
                        
     # HOME PAGE
elif save_bio == 'Home':
                
                #st_lottie(lottieMain, height=400, key= "main")
                
                with st.container():
                    
                    st.write("---")
                    left_column, right_column = st.columns(2)
                    
                    with left_column:
                        
                        #st.header("Heart Failure")
                        
                        #st.subheader("\nProbability of having Heart Failure:")
                        
                       # with st.container():
                    
                   #st.write("---")
                    #left_column, right_column = st.columns(2)
                    
                    #with left_column:
                        
                        st.header("Diabetes")
                        
                        st.subheader("\nProbability of having Diabetes:")
                           #calling db user bio data 
                           
                           
                           
                           
                           #run diabetes type model
prediction = clf.predict([[p1_get,p2_get,p3_get]])
st.success('Diabetes Type is: {} '.format(prediction[0]))
                          
                           

#if st.button('Predict', key = "783b046e-7a62-47a7-a64a-c01e8529c03d"):
                            
                           
                        ##with right_column:
                        
                        # load the model
                        #st_lottie(lottieMain, height=400, key= "main")
                       ## st.write("")
                       ## st.write("")
                        ##st.write("")
                        ##st.write("")

         