import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from streamlit_webrtc import webrtc_streamer


import cv2
from PIL import Image
import face_recognition
import os
from datetime import datetime


import database as dbp
import helper as hp


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
      webrtc_streamer(key="example")

  if selected =='Add a new student/employee':
      hp.adding_Entities()

  if selected =='Data Analysis':
      st.write("data")
















  st.sidebar.markdown("---")
  authenticator.logout("Logout","sidebar")


















