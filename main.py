import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import cv2
from PIL import Image

import database as dbp


st.set_page_config(page_title="A Sk_Y product", page_icon="🌄", layout="centered")
st.title("Advanced Attendence System 📋..")
st.markdown("---")



# ---Authentication---
usernames = dbp.get_admin_data("Id")
names = dbp.get_admin_data("username")
passwords = dbp.get_admin_data("password")



credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

# print(credentials)

authenticator = stauth.Authenticate(credentials,'ck', 'rk',cookie_expiry_days=5)
name,authentication_status, username = authenticator.login("Admin login😎","main")

#   ---Sidebar---
st.sidebar.header(f"Welcome {name}.")
st.sidebar.markdown("---")

if authentication_status ==False:
  st.error("Invalid Credentials🙄.")

# if authentication_status==None:
#   st.warning("Enter your Credentials.")

if authentication_status:

  with st.sidebar:
    selected =option_menu(
      menu_title=None,
      options =['Take attendence','Add a new student/employee','Data Analysis'],
      icons=['camera-video-fill', 'person-plus-fill', 'calendar3'],
      styles={
        # "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": { "font-size": "14px"},
        "nav-link": {"font-size": "12px", "text-align": "left", "margin": "0px",},
        # "nav-link-selected": {"background-color": "green"},
      },
      default_index=0
    )

  if selected =='Take attendence':
      input=st.camera_input("camera input")

  if selected =='Add a new student/employee':
      st.header("Adding a New Entity.")
      # st.markdown(" ")
      col1, col2 = st.columns(2)
      with col1:
        fname = st.text_input("Enter First Name : ")
        fname = fname.strip()

        Id = st.text_input("Enter the roll.no/ID :")


      with col2:
          lname = st.text_input("Enter Last Name : ")
          Class = st.text_input("Enter Class/Department : ")

      method = st.selectbox("Add an Image : ", ['Take from webcam', 'Upload from device'])
      if method == 'Take from webcam':
          img_file_buffer = st.camera_input("Click on the 'Take photo' button to capture.")
          if img_file_buffer is not None:
              # To read image file buffer with OpenCV:
              bytes_data = img_file_buffer.getvalue()
              cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)


      else:
          img_file_buffer = st.file_uploader("upload here [only  .jpg files are allowed]", type=".jpg")
          if img_file_buffer is not None:
              # To read image file buffer with OpenCV:
              bytes_data = img_file_buffer.getvalue()

              cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)


      st.markdown(" ")

      # st.write(cv2_img)
      # st.write(type(cv2_img))

      col1,col2,col3 = st.columns([1,1.2,0.1])
      with col2:
        button = st.button("Submit")
        if button:
            cv2.imwrite(f'Entities_Images/{fname}_{lname}.jpg', cv2_img)
            img = f'Entities_Images/{fname}_{lname}.jpg'
            dbp.add_entites(fname,lname,Id,Class,img[16:len(img)])
            dbp.insert_image(img,fname,lname)


            st.write(img)
            st.write(type(img))


  if selected =='Data Analysis':
      st.write("data")
















  st.sidebar.markdown("---")
  authenticator.logout("Logout","sidebar")


















