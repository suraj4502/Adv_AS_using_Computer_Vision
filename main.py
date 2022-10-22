import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import csv
from datetime import datetime, timedelta

import cv2
import face_recognition
import os


import database as dbp
import helper as hp


st.set_page_config(page_title="A Sk_Y product", page_icon="🐼", layout="centered")
st.title("Advanced Attendance System 📋..")
st.markdown("---")
hide_st_style = """
            <style>
            
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


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

# if authentication_status:
#     try:
#         if authenticator.reset_password(username, 'Reset password'):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)

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
      # print(myList)
      for cl in myList:
          curImg = cv2.imread(f'{path}/{cl}')
          images.append(curImg)
          classNames.append(os.path.splitext(cl)[0])
      # print(classNames)


      def findEncodings(images):
          encodeList = []
          for img in images:
              img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
              encode = face_recognition.face_encodings(img)[0]
              encodeList.append(encode)
          return encodeList





      def markAttendence(Id):
          field_names = ["ID",'Fname','lname', 'Department', 'Time','Date']
          vals = dbp.get_info_of_entities(Id)
          ct = datetime.now()
          ct = ct.strftime('%H:%M')
          cd = datetime.today()
          cd = cd.strftime("%d/%m/%Y")
          dict = {"ID":vals[1],"Fname":vals[3],"lname":vals[4],"Department":vals[0],"Time":ct,"Date":cd}

          with open('data.csv', 'a') as csv_file:
              dict_object = csv.DictWriter(csv_file, fieldnames=field_names)

              dict_object.writerow(dict)



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
              try:
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
              except:
                    st.info("###### Please click a clear Image.")

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
      import plotly.express as px
      df = pd.read_csv('data.csv')
      df.ID= df.ID.astype('str').str.replace(".0","",regex=False)
      df = df.dropna()
      da_option = st.radio("Reports :",["Today's","Particular Date","overall"],horizontal=True)
      if da_option == "Today's":
          st.header("Today's Report :")
          df_today = df[df["Date"] == datetime.today().strftime("%d/%m/%Y")]
          df_today.reset_index(inplace=True)
          df_today.drop("index",axis=1,inplace=True)
          df_today.drop_duplicates(subset=["ID","Date"],ignore_index=True,inplace=True)
          st.dataframe(df_today)
          st.info(f"###### Total no. of students : {df_today.ID.count()}.")

      if da_option=="Particular Date":
          date_input = st.date_input("Enter the Date:")
          date_input = date_input.strftime("%d/%m/%Y")
          st.header(f"{date_input} Report :")
          df_y = df[df["Date"] ==date_input]
          df_y.reset_index(inplace=True)
          df_y.drop("index", axis=1, inplace=True)
          df_y.drop_duplicates(subset=["Time"],ignore_index=True,inplace=True)
          st.dataframe(df_y)
          st.info(f"###### Total no. of students : {df_y.ID.count()}.")

      elif da_option=="overall":
          st.header("Overall Report :")
          df.reset_index(inplace=True)
          df.drop("index", axis=1, inplace=True)
          df.drop_duplicates(subset=["ID","Date"],ignore_index=True,inplace=True)
          st.dataframe(df)
          st.markdown("---")
          st.header("Histogram Of the Data.")
          ft_btn = st.checkbox("In depth.")
          fig = px.histogram(df,x='Date',title="Daywise Attendence.",color_discrete_sequence= ["#CC3636"])
          fig.update_layout(
            xaxis=dict(showgrid=False),   #disabling grids
            yaxis=dict(showgrid=False),

            showlegend = False,
              title_x=0.4,  # adjusting title
              title_font=dict(  # working with font
                  family="Helvetica",
                  size=20,
              )
            )
          fig.update_xaxes(rangeslider_visible=False)
          st.plotly_chart(fig)

          if ft_btn:
              fig = px.histogram(df, x='Date', title="Daywise Attendence[Indepth].", color="ID")
              fig.update_layout(
                  xaxis=dict(showgrid=False),  # disabling grids
                  yaxis=dict(showgrid=False),

                  showlegend=True,
                  title_x=0.4,  # adjusting title
                  title_font=dict(  # working with font
                      family="Helvetica",
                      size=20,
                  )
              )
              fig.update_xaxes(rangeslider_visible=False)
              st.plotly_chart(fig)

          df.to_csv('finaldata.csv')
          dbp.update_data()



















  st.sidebar.markdown("---")
  authenticator.logout("Logout","sidebar")









st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")







st.sidebar.markdown("- Developed by `SKY`.   ⇨[github ](https://github.com/suraj4502), "
                    "[Linkedin](https://www.linkedin.com/in/surajkumar-yadav-6ab2011a4/),"
                    " [Ig](https://www.instagram.com/suraj452/).")











