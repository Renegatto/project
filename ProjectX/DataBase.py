from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
 
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
 
 
class Currance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    rate = db.Column(db.String(120))
 
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
 
    def __repr__(self):
        return '<Currance %r, %r>' % (self.name, self.rate)
 
 
db.create_all()
 
@app.route('/test')
def test():
 
    url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
    all_courses = requests.get(url).json()
    courses = []  
 
    for k in all_courses:
        n = k["Cur_Name"], k["Cur_OfficialRate"]
        courses.append(n)
       
    for s in courses:
        print(s)
        if db.session.query(Currance).filter_by(name=s[0]).count() < 1:
            c = Currance(s[0], s[1])
            db.session.add(c)
        else:
           c = db.session.query(Currance).filter_by(name=s[0])          
           c.rate = s[1]          
 
    db.session.commit()    
    return render_template ('test.html', curr = Currance.query.all())
   
 
if __name__ == '__main__':
    app.debug = True
    app.run()