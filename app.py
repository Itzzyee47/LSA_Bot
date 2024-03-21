from datetime import date
from flask import Flask, redirect, render_template, jsonify, request, session, url_for
from response import getRespons
from readJson import numOfNewQ, getUsers, getquestions
import mysql.connector
# <iframe src="https://lsa-chatbot.onrender.com/" style="position: absolute;" width="100%" height="100%" frameborder="0"></iframe>
# The above tag is for the integration of the chatpage...
 
# from waitress import serve
from flask_cors import CORS

app = Flask(__name__)

def login_required(func):
    def wrapper_func(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
            
        data = {"message":"Please login or signup"}
        return render_template("index.html",**data)
    
    wrapper_func.__name__ = func.__name__  # Preserve the original function name
    return wrapper_func
    

        

CORS(app)
# CORS(app, origins=['http://example.com', 'http://localhost:5000/chatpage']).
app.secret_key = "zuian21nuis91"
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="LSA"
    )
def getCursor():
    mycursor = mydb.cursor()
    return mycursor
#   host="itzZyee.mysql.pythonanywhere-services.com",
#   user="itzZyee",
#   password="LSAdbPass",
#   database="itzZyee$LSA"


@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'POST':
        name = 'user'
        email = request.form.get('email')
        password = request.form.get('password')
        now = date.today()
        isa = "SELECT * FROM visitors WHERE email = %s"
        v1 = (email,)
        mycursor = getCursor()
        mycursor.execute(isa,v1)
        indb = mycursor.fetchall()
        if indb:
            isa = "SELECT * FROM visitors WHERE email = %s and password = %s"
            v1 = (email,password)
            mycursor.execute(isa,v1)
            indb = mycursor.fetchall()
            if indb:
                session['username'] = email
                mycursor.close()
                return redirect(url_for('chat'))
            else:
                data = {"message":"Wrong email or password","user":email}
                return render_template("index.html",**data)  
        else:
            q = "INSERT INTO visitors VALUES (%s,%s,%s,%s,%s)"
            val = ("",name,email,password,now)
            mycursor.execute(q,val)
            query = mydb.commit()
            
            if query:
                print("logged")
                session['username'] = email
                
                mycursor.close()
                return redirect(url_for('chat'))
        
            
        data = {"message":"Please login"}
        return render_template("index.html",**data)

        
    else:
        return render_template("index.html")

@app.route("/chatpage")
def chat():
    #the user must be logged in to access this page.....
    if 'username' in session:
      username = session['username']
      data = {"user":username}
      return render_template("base.html",**data)
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

# /dash/manage-users
@app.route("/dashborad")
@login_required
def dash():
    #the user must be logged in to access this page.....
    username = session['username'] 
    mycursor = getCursor()
    mycursor.execute("SELECT COUNT(*) FROM visitors")
    count = mycursor.fetchall()
    newQ = numOfNewQ()
    data = {"user":username, "count":count[0][0], "newQ": newQ}
    

    return render_template("dash.html",**data)

@app.route("/dash/manage-users")
@login_required
def mUsers():
    #the user must be logged in to access this page.....
    username = session['username']
    q = "SELECT * from visitors"
    mycursor = getCursor()
    mycursor.execute(q)
    users = mycursor.fetchall()
    data = {"users":users,"user":username}

    return render_template("dash/manageUsers.html",**data)


@app.route("/update/<int:i>",methods=['POST','GET'])
@login_required
def updateU(i):
    username = session['username']
    #getting values from the submmited form
    if request.method == 'POST':
        n = request.form.get('name')
        e = request.form.get('email')
        p = request.form.get('password')
    # updating the database
        q = "UPDATE visitors SET name = %s, email = %s, password = %s WHERE visitors.id = %s"
        val = (n,e,p,i)
        mycursor = getCursor()
        mycursor.execute(q,val)
        mydb.commit()
        s = "<script>if (confirm('Your update was successful ')) {goto('/dash/manageUsers.html')} else {txt = 'You pressed Cancel!';}</script>"

    return redirect(url_for('mUsers'))


@app.route("/dash/manageNewQ")
@login_required
def manageNewQ():
    username = session['username'] 
    D = []
    i = 0
    users = getUsers()
    questions = getquestions()
    while i < len(users):
        D.append([users[i],questions[i]])
        i += 1
    
    data = {"user":username, "Qs":D}

    return render_template("dash/manageNewQ.html",**data)
  
  

@app.route("/dash/Pendding")
@login_required
def pend():
    #the user must be logged in to access this page.....
    username = session['username']
    
    data = {"user":username}

    return render_template("dash/moreUpdates.html",**data)
  

# The format for new questions to be saved in the json file...... 
# {
#     "user":"ebongloveis@gmail.com",
#     "qestions": [
#         "what are you"
#     ]
# }

@app.route("/logout")
def logO():
    # remove the user from the session...
    session.pop('username',None)
    
    return redirect(url_for('index'))

#something of an api that uses the ml algorithm...
@app.route("/send_message", methods=['POST'])
def send_message():
    text = request.form["message"]
    print(text)
    user = session['username']
    response = getRespons(text,user)
    message = {"answer": response}
    print(message)
    return jsonify(message)

if __name__ =="__main__":
    app.run(debug=True, port=3000)
    