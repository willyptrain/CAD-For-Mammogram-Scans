from flask_login import LoginManager
from flask_login import UserMixin
from flask import Flask, request
from flask_login import current_user, login_user
from flask import Flask, render_template, g, request, session, flash
import sqlite3
import os
import shutil
from werkzeug.utils import secure_filename
from PIL import Image
import io
import re
import cStringIO
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv2 import *
from keras.models import model_from_json
from keras.utils import np_utils
import random
from sklearn.externals import joblib
from sklearn import preprocessing
from keras.utils import plot_model
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

DATABASE = 'users.db'
db = sqlite3.connect(DATABASE)
db.execute('create table if not exists users (user TEXT, password TEXT)')
db.close()

@app.route('/')
def home(): 
   return render_template('')
 
@app.route('/signup', methods=["POST"])  
def signup():
   username = request.form[]
   
   


if __name__ == "__main__":
   app.run(debug=True)
