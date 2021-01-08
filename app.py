from flask import Flask,jsonify, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import json

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        roll=userDetails['roll']
        name = userDetails['name']
        maths=userDetails['maths']
        physics=userDetails['physics']
        chemistry=userDetails['chemistry']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(roll,name,maths,physics,chemistry) VALUES(%s, %s,%s,%s,%s)",(roll,name,maths,physics,chemistry))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')
 
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users ORDER BY maths DESC")
    if resultValue > 0:
        userDetails = cur.fetchall()
        result=[]
        for info in userDetails:
            temp={}
            temp['roll']=info[0]
            temp['name']=info[1]
            temp['maths']=info[2]
            temp['physics']=info[3]
            temp['chemistry']=info[4]
            temp['total']=info[5]
            temp['percentage']=info[6]
            result.append(temp)
        # return userDetails
        # print(result.jsonify())
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)
