from flask import Flask, render_template, request, url_for, redirect
import csv  
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
 
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Entry(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   index = db.Column(db.Integer)
   col1 = db.Column(db.Integer)
   col2 = db.Column(db.Integer)

def __init__(self, index, col1, col2):
   self.index = index
   self.col1 = col1
   self.col2 = col2


@app.route('/')
def index():
    return 'Index Page'

def to_int(string):
    if type(string) == str:
        if string[0] == "-":
            return (-1) * int(string[1:])
        else:
            return int(string)
    return

@app.route('/test_api/', methods=['GET','POST'])
def test_api():
    
    if request.method == 'POST': #request is in the form of {'0':indexval, '1':col1val, '2':col2val, ...}
        value = []
        for i in range(3): #EDIT TO 17
            try:
                value.append(request.form.get(str(i)))
            except:
                continue

        if value[0] == 'END':
                
            header = ['id', 'col1', 'col2'] #EDIT TO 16 COLS
            data = []  
                
            #extract all entries from database
            num_rows = 0
            entries = Entry.query.all()
            for e in entries:
                row = [e.index, e.col1, e.col2]
                data.append(row)
                num_rows += 1
                
            #CSV export
            title = datetime.datetime.now()
            title = str(title).replace(':', '-')
            title = title[:10] + "-" + title[11:19] + '_export.csv'
                
            with open(title, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for d in data:
                    writer.writerow(d)
                
            #empty the database
            db.session.query(Entry).delete()
            db.session.commit()
            
            return "EXPORTED: " + str(num_rows) + " rows"
                
        elif value[0] != 'START':
                
            #save entry to database
            data_entry = Entry(index = to_int(value[0]), col1 = to_int(value[1]), col2 = to_int(value[2]))
            db.session.add(data_entry)
            db.session.commit()
            
            return "SAVED: row with id " + value[0]
        
        else:
            
            return "OK"
    
    return

@app.route('/visualize/<value>') 
def visualize(value):
    return 'Visualization'

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')