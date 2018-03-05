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

app = Flask(__name__)

upload_folder = "static/"
app.config['UPLOAD_FOLDER'] = upload_folder

DATABASE = 'database.db'

db = sqlite3.connect(DATABASE)
db.execute('create table if not exists patients (case_num TEXT, name TEXT, age TEXT, assessment TEXT, binary BINARY, filename TEXT, model_prediction TEXT)')
db.close()

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
   print("good" + img_url)
   '''image_data = re.sub('^data:image/.+;base64,', '', img_url).decode('base64')
   image_PIL = Image.open(cStringIO.StringIO(img_url))
   image_np = np.array(image_PIL)
   '''
   
   im = Image.open(BytesIO(base64.b64decode(img_url)))
   im.save('test.png')
   #print 'Image received: {}'.format(im.shape)
   
   
   return 's' 
   #img = Image.open(io.StringIO(img_data))
   #print(img_data)
   #return img_data
       
         
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
   
        
    
    
    
'''
Pass blob data onto the database to get to python code so you can convert to PIL and diagnose using cnn


'''