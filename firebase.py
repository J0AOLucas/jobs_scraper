# pip install pyrebase4
# python -m pip install --upgrade setuptools

import pyrebase

def send_data(params):
    config = {
        'apiKey': "AIzaSyA-C3GSk81MxGtKLkrl7i092WzODoQoawI",
        'authDomain': "byu-i-project.firebaseapp.com",
        'projectId': "byu-i-project",
        'databaseURL': 'https://byu-i-project-default-rtdb.firebaseio.com/',
        'storageBucket': "byu-i-project.firebasestorage.app",
        'messagingSenderId': "429391777029",
        'appId': "1:429391777029:web:07efacfa2c512166067b6c",
        'measurementId': "G-D38H8NSC0T"
    }

    firebase = pyrebase.initialize_app(config)

    data_base = firebase.database()
    data_base.child("jobs").push(params)


