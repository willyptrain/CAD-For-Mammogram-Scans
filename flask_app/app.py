from flask import Flask, render_template, g, request
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


app = Flask(__name__)

upload_folder = "static/"
app.config['UPLOAD_FOLDER'] = upload_folder

DATABASE = 'database.db'

db = sqlite3.connect(DATABASE)
db.execute('create table if not exists patients (case_num TEXT, name TEXT, age TEXT, assessment TEXT, binary BINARY, filename TEXT, model_prediction TEXT)')
db.close()


def get_pixels(img_source):
   image_data = imread(img_source).astype(np.float32)
   return image_data

        
def organize(source):
   x = [] 
   im = Image.open(source,'r')
   im = im.convert('L')
   im = im.resize((28,28),Image.ANTIALIAS)   
   pix = im.getdata()
   arr_pix = []
   w, h = 28,28
   print(pix.getpixel((27,27)))
   for s in range(0, w):
      arr_pix.append([])
      for c in range(0, h):
         arr_pix[s].append(pix.getpixel((s,c)))

   x.append(arr_pix)   
   return np.array(x) #shape (1,28,28)
   


def crop_out_lesion(source):
   image = cv2.imread(source,-1)
   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
   pix = get_pixels(source)
   coords = []
   for i in range(0,pix.shape[0]):
      for c in range(0,pix.shape[1]):
         r = pix[i][c][2]
         b = pix[i][c][0]
         g = pix[i][c][1]
         if(r == 255 and b == 0 and g == 0): #only apply to first identified lesion
            coords.append([c,i])

   
   
   if(len(coords) == 0):
      print(coords)
         
   mask = np.zeros(image.shape, dtype=np.uint8)
   roi_corners = np.array([coords], dtype=np.int32)
 
   channel_count = image.shape[2] 
   ignore_mask_color = (255,)*channel_count
   cv2.fillPoly(mask, roi_corners, ignore_mask_color)
   
   lesion_with_border = cv2.bitwise_and(image, mask)
   
   #im = cv2.split(lesion_with_border)
   
   for i in range(0, lesion_with_border.shape[0]):
      for c in range(0, lesion_with_border.shape[1]):
         red = pix[i][c][2]
         green = pix[i][c][0]
         blue = pix[i][c][1]
         if(red == 255 and green == 0 and blue == 0): 
            lesion_with_border[i][c] = [0., 0., 0., 0.]
            lesion_with_border[i+1][c+1] = [0., 0., 0., 0.]
            lesion_with_border[i-11][c+1] = [0., 0., 0., 0.]
            lesion_with_border[i+1][c-1] = [0., 0., 0., 0.]
            lesion_with_border[i-1][c-1] = [0., 0., 0., 0.]
         #else:
         #   lesion_with_border[i][c] = [255., 255., 255., 0]         
   for i in range(0, lesion_with_border.shape[0]):
      for c in range(0, lesion_with_border.shape[1]):
         red = pix[i][c][2]
         green = pix[i][c][0]
         blue = pix[i][c][1]
         if(red == 0. and blue == 0. and green == 0.):
            lesion_with_border[i][c] = [0., 0., 0., 0.]
           
   min_x = coords[0][0]
   min_y = coords[0][1]
   max_x = coords[0][0]
   max_y = coords[0][1]
   for i in range(0, len(coords)):
      if(coords[i][0] < min_x):
         min_x = coords[i][0]
      if(coords[i][1] < min_y):
         min_y = coords[i][1]
      if(coords[i][0] > max_x):
         max_x = coords[i][0]
      if(coords[i][1] > max_y):
         max_y = coords[i][1]

   min_x, min_y = min_x+5, min_y+5
   max_x, max_y = max_x-5, max_y-5
   lesion_with_border = lesion_with_border[min_y:max_y,min_x:max_x]
   lesion_with_border = cv2.cvtColor(lesion_with_border, cv2.COLOR_RGBA2GRAY)
   cv2.imwrite("static/test2.png", lesion_with_border)
   
def load_model():
   json_file = open('../model.json', 'r')
   model_json = json_file.read()
   json_file.close()
   
   model = model_from_json(model_json)
   # load weights into new model
   model.load_weights("../weights.h5")
       
   # evaluate loaded model on test data
   model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
   
   '''x = crop_out_lesion('static/test.png')
   cv2.imwrite('static/test.png', x)
   '''
   x = organize('static/test2.png')
   x = x.transpose(1,2,0)
   x = np.array([x])
   #x = np.rollaxis(np.array(x), 1, 2)
 
   #(1,28,28,1)
   pred = model.predict([x])
   print(pred)

@app.route("/")
def home():
   db = sqlite3.connect(DATABASE)
   db.row_factory = sqlite3.Row
   cur = db.cursor()
   cur.execute("select * from patients")
   rows = cur.fetchall()
   return render_template('index.html', rows = rows)
    
@app.route('/new_pat')
def new_patient():
   return render_template('new_patient.html') 
   
@app.route('/addpat',methods = ['POST', 'GET'])
def addpat(): 
   msg = ""
   if request.method == 'POST':
      try:
         case_num = request.form['case']
         name = request.form['name']
         age = request.form['age']
         assessment = request.form['assessment']
         file = request.files['scan']
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         model_prediction = ""
         try:              
            print("0")
            f = open(upload_folder+filename,"rb") #not working
            print("1")
            data = f.read()
            print("2")
            binary = sqlite3.Binary(data)
            print("3")
            f.close()
         except:
            print("nope sorry bud")
         with sqlite3.connect(DATABASE) as db:
            cur = db.cursor()
            print("1")
            cur.execute("INSERT INTO patients (case_num, name, age, assessment, binary, filename, model_prediction)  VALUES (?,?,?,?,?,?,?)",(case_num,name,age,assessment,binary, upload_folder+filename, "") )
            print("2")
            db.commit()
            msg = "Record successfully added"
      except:
         db.rollback()
         msg = "error in insert operation"
         
      finally:      
         return render_template("status_update.html",msg = msg)
         db.close()
         
@app.route('/edit_img',methods = ['POST', 'GET'])
def edit_img(): 
   file_name = request.args.get('file_name','')
   return render_template('edit.html', file=file_name)   
        
@app.route('/model_predict',methods = ['POST', 'GET'])
def model_predict():
   img_url = request.form['pixels'][21:]
   im = Image.open(BytesIO(base64.b64decode(img_url)))
   im = im.resize((480,360), Image.ANTIALIAS)
   im.save('static/test.png')  
   organize('static/test.png')
   return "worked"      
 
         
def writeImage(data, source):
    try:
        fout = open(source,'wb')    
        fout.write(data)
        shutil.move(source,"static/")
    except IOError, e:    
        print "not working:  %d: %s" % (e.args[0], e.args[1])
        
    finally:
        if fout:
            fout.close()       
    
 
if __name__ == "__main__":
   app.run(debug=True)
   #crop_out_lesion('static/test.png')
   #load_model()    
   