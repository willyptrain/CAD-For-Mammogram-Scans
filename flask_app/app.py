from flask import Flask, render_template, g, request
import sqlite3
import os
import shutil

app = Flask(__name__)


DATABASE = 'database.db'

db = sqlite3.connect(DATABASE)
db.execute('create table if not exists patients (case_num TEXT, name TEXT, age TEXT, assessment TEXT, img BINARY, file_source TEXT)')
db.close()

@app.route("/")
def home():
   db = sqlite3.connect(DATABASE)
   db.row_factory = sqlite3.Row
   cur = db.cursor()
   cur.execute("select * from patients")
   rows = cur.fetchall()
   print(rows)
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
         img = request.form['scan']
         file_source = str(case_num)+".png"
         try:
            print("worked0000")
            f = open(img,"rb") #not working
            print("worked0")
            data = f.read()
            print("worked1")
            binary = sqlite3.Binary(data)
            print("worked2")
            writeImage(binary, file_source)
            print("worked")
            f.close()
         except:
            print("nope sorry bud")
         with sqlite3.connect(DATABASE) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO patients (case_num, name, age, assessment, img, file_source)  VALUES (?,?,?,?,?,?)",(case_num,name,age,assessment,img, file_source) )
            db.commit()
            msg = "Record successfully added"
      except:
         db.rollback()
         msg = "error in insert operation"
         
      finally:      
         return render_template("status_update.html",msg = msg)
         db.close()
         
def writeImage(data, source):
    try:
        fout = open(source,'wb')    
        print("average")
        fout.write(data)
        print("good")
        shutil.move(source,"static/")
        print("we good fam")
    except IOError, e:    
        print "not working:  %d: %s" % (e.args[0], e.args[1])
        
    finally:
        if fout:
            fout.close()       
    
 
if __name__ == "__main__":
   app.run(debug=True)
   
        
    