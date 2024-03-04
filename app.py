from datetime import date
from flask import Flask, redirect, render_template, jsonify, request, session, url_for
from response import getRespons
import mysql.connector
# from waitress import serve

app = Flask(__name__)
app.secret_key = "zuian21nuis91"
mydb = mysql.connector.connect(
  host="itzZyee.mysql.pythonanywhere-services.com",
  user="itzZyee",
  password="LSAdbPass",
  database="itzZyee$LSA"
)

mycursor = mydb.cursor()
mycursor

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'POST':
        name = 'user'
        email = request.form.get('email')
        password = request.form.get('password')
        now = date.today()
        isa = "SELECT * FROM visitors WHERE email = %s"
        v1 = (email,)
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

      return render_template("base.html")
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

# /dash/manage-users
@app.route("/dashborad")
def dash():
    #the user must be logged in to access this page.....
    if 'username' in session:
        username = session['username'] 
        mycursor.execute("SELECT COUNT(*) FROM visitors")
        count = mycursor.fetchall()
        data = {"user":username, "count":count[0][0]}
       

        return render_template("dash.html",**data)
  
  
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

@app.route("/dash/manage-users")
def mUsers():
    #the user must be logged in to access this page.....
    if 'username' in session:
        username = session['username']
        q = "SELECT * from visitors"
        mycursor.execute(q)
        users = mycursor.fetchall()
        data = {"users":users,"user":username}

        return render_template("dash/manageUsers.html",**data)
  
  
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

@app.route("/update/<int:i>",methods=['POST','GET'])
def updateU(i):
    #the user must be logged in to access this page.....
    if 'username' in session:
        username = session['username']
        #getting values from the submmited form
        if request.method == 'POST':
            n = request.form.get('name')
            e = request.form.get('email')
            p = request.form.get('password')
        # updating the database
            q = "UPDATE visitors SET name = %s, email = %s, password = %s WHERE visitors.id = %s"
            val = (n,e,p,i)
            mycursor.execute(q,val)
            mydb.commit()
            s = "<script>if (confirm('Your update was successful ')) {goto('/dash/manageUsers.html')} else {txt = 'You pressed Cancel!';}</script>"

        

        return redirect(url_for('mUsers'))
  
  
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

@app.route("/dash/Pendding")
def pend():
    #the user must be logged in to access this page.....
    if 'username' in session:
        username = session['username']
        
        data = {"user":username}

        return render_template("dash/moreUpdates.html",**data)
  
  
    data = {"message":"Please login or signup"}
    return render_template("index.html",**data)

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
    response = getRespons(text)
    message = {"answer": response}
    print(message)
    return jsonify(message)

if __name__ =="__main__":
    app.run(debug=True, port=3000)
    