from datetime import date
from flask import Flask, redirect, render_template, jsonify, request, session, url_for
from db.connect import mycursor,mydb
from response import getRespons
from waitress import serve

app = Flask(__name__)
app.secret_key = "zuian21nuis91"

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
                
                return redirect(url_for('chat'))
        
            
        data = {"user":"Please login"}
        return render_template("index.html",**data)

        
    else:
        return render_template("index.html")

@app.route("/chatpage")
def chat():
    #the user must be logged in to access this page.....
    if 'username' in session:
      username = session['username']

      return render_template("base.html")
    
    return render_template("index.html")

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
    