import pyrebase

firebaseConfig = {
        'apiKey': "AIzaSyDn4S_FA587a_09_zMkfONBOSf_EpasAzI",
        'authDomain': "mu-project-908d8.firebaseapp.com",
        'projectId': "mu-project-908d8",
        'databaseURL': "https://mu-project-908d8-default-rtdb.europe-west1.firebasedatabase.app/",
        'storageBucket': "mu-project-908d8.appspot.com",
        'messagingSenderId': "452647811998",
        'appId': "1:452647811998:web:fed05a918164f55b2f748f",
        'measurementId': "G-DMTTK0QV0S"
    }


firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
storage = firebase.storage()




def insert_admin(name,email_id,pwd):
        data={'username':name,'Id':email_id,'password':pwd}
        return db.child("Admins").push(data)

def get_all_admins():
        result = db.child("Admins").get()
        return  result.val()

def get_admin_info(email_id):
        admins = db.child("Admins").order_by_child("Id").equal_to(email_id).get()
        for admin in admins.each():
                a_data= admin.val()
        return a_data

def update_admin(email_id,updates):
        admins = db.child("Admins").get()
        for admin in admins.each():
                if admin.val()["Id"]==email_id:
                        db.child("Admins").child(admin.key()).update(updates)

def get_admin_data(field):
        admins = db.child("Admins").get()
        data =[]
        for admin in admins.each():
                data.append(admin.val()[field])
        return data

# ----------------------------------------------------------------------------------------------------------------------

def add_entites(fname,lname,id,dept,img):
        data = {'first_name': fname, 'last_name': lname,'Id': id, 'Department': dept,'Image':img}
        return db.child("Entities").push(data)

# ----------------------------------------------------------------------------------------------------------------------

def insert_image(image,fname,lname):
        return storage.child(f"Entities_Images/{fname}_{lname}.jpg").put(image)







# db.child("Entities").remove()





# admins = get_all_admins()





# a_names = get_all_admin_names('username')
# print(a_names)
# print(get_all_admins())




# insert_admin("sky",'sy123@gmail.com','12345678')
# print(get_all_admins())
# sdata= get_admin_info('suraj04@gmail.com')
# print(sdata)
# update_admin('sy123@gmail.com',updates={'password':"asdfghjkl"})


### Adding admins to database
import streamlit_authenticator as stauth

# admins = ["surajkumar yadav","sky"]
# email_id = ["suraj04@gmail.com","sy123@gmail.com"]
# passwords =["abcd1234","asdfghjkl"]
# hashed_passwords = stauth.Hasher(passwords).generate()
#
# for (admin,e_id,hashed_password) in zip(admins, email_id, hashed_passwords):
#         insert_admin(admin,e_id,hashed_password)

# admins = ["Admin_01","Admin_02"]
# email_id = ["admin01@gmail.com","admin02@gmail.com"]
# passwords =["admin01","admin02"]
# hashed_passwords = stauth.Hasher(passwords).generate()
#
# for (admin,e_id,hashed_password) in zip(admins, email_id, hashed_passwords):
#         insert_admin(admin,e_id,hashed_password)














