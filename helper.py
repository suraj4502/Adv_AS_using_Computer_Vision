import streamlit as st
import cv2
import numpy as np
import database as dbp
def adding_Entities():
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
    if 'ss' not in st.session_state:
        st.session_state.ss = False

    col1, col2, col3 = st.columns([1, 1.2, 0.1])
    with col2:
        button = st.button("Submit")
        if button:
            cv2.imwrite(f'Entities_Images/{fname}_{lname}.jpg', cv2_img)
            img = f'Entities_Images/{fname}_{lname}.jpg'
            dbp.add_entites(fname, lname, Id, Class, img[16:len(img)])
            dbp.insert_image(img, fname, lname)
            st.balloons()
            st.session_state.ss = True

    if st.session_state.ss == True:
        st.success(f"###### Succesfully added  *{fname} {lname}* to the Database.")
        st.markdown(" ")
        st.markdown(" ")
        st.info("###### *To add Another Entity Please refresh the page.*")
