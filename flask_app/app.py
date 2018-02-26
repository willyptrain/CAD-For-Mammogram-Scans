from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)


DATABASE = 'database.db'

db = sqlite3.connect(DATABASE)
db.execute('create table if not exists patients (case_num TEXT, name TEXT, age TEXT, assessment TEXT)')
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
         
         with sqlite3.connect(DATABASE) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO patients (case_num, name, age, assessment)  VALUES (?,?,?,?)",(case_num,name,age,assessment) )
            print("2")  
            db.commit()
            print("3")
            msg = "Record successfully added"
      except:
         db.rollback()
         msg = "error in insert operation"
         
      finally:      
         return render_template("status_update.html",msg = msg)
         db.close()
 
if __name__ == "__main__":
    app.run(debug=True)
    
        
    