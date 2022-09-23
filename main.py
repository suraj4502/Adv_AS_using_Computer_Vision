import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import random
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration,VideoTransformerBase
import av
import threading

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
      path = 'Entities_Images'
      images = []
      classNames = []
      myList = os.listdir(path)
      print(myList)
      for cl in myList:
          curImg = cv2.imread(f'{path}/{cl}')
          images.append(curImg)
          classNames.append(os.path.splitext(cl)[0])
      print(classNames)


      def findEncodings(images):
          encodeList = []
          for img in images:
              img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
              encode = face_recognition.face_encodings(img)[0]
              encodeList.append(encode)
          return encodeList

      def markAttendence(Id):
          with open('Attendance.csv', 'r+') as f:
              myDataList = f.readlines()
              nameList = []
              for line in myDataList:
                  entry = line.split(',')
                  nameList.append(entry[0])
              if name not in nameList:
                  now = datetime.now()
                  dtString = now.strftime('%H:%M')
                  today = datetime.today()
                  d1 = today.strftime("%d/%m/%Y")
                  f.writelines(f'\n{Id},{dtString},{d1}')


      encodeListKnown = findEncodings(images)

      if 'id_key' not in st.session_state:
          st.session_state['id_key'] =1

      if 'image_key' not in st.session_state:
          st.session_state['image_key'] =101
      def main(id_key,image_key):
          input_id=st.text_input("Enter the Roll no/ID: ",key=id_key)
          img_file_buffer = st.camera_input("Click your photo.. ",key = image_key)
          if img_file_buffer is not None:
              # To read image file buffer with OpenCV:
              bytes_data = img_file_buffer.getvalue()
              image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

              face_test = face_recognition.face_locations(image)
              encode_test = face_recognition.face_encodings(image)
              # print(encode_test)
              # print(len(encodeListKnown))
              face_dis_list = []
              for i in encodeListKnown:
                  match = face_recognition.compare_faces(i, encode_test)
                  face_dis = face_recognition.face_distance(i, encode_test)
                  face_dis_list.append(face_dis)
              # print(face_dis_list)
              index = np.argmin(face_dis_list)
              Id = classNames[index]
              if input_id==Id:
                  markAttendence(input_id)
                  st.success("Attendence Marked")
              else:
                  st.error("Invalid Credentials...")

      main(st.session_state.id_key,st.session_state.image_key)
      st.markdown("---")
      col1,col2,col3 = st.columns([1,1,0.01])
      with col3:
          button = st.button("Mark another Attendence.")

      if button :
          st.session_state.id_key = st.session_state.id_key +1
          st.session_state.image_key = st.session_state.image_key +2
          main(st.session_state.id_key, st.session_state.image_key)

  if selected =='Add a new student/employee':
      hp.adding_Entities()

  if selected =='Data Analysis':
      st.write("data")
















  st.sidebar.markdown("---")
  authenticator.logout("Logout","sidebar")


















