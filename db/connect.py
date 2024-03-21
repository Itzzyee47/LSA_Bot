import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="LSA"
)

mycursor = mydb.cursor()
isa = "SELECT * FROM visitors WHERE email = %s"
v1 = ('ebongloveis@gmail.com',)
mycursor.execute(isa,v1)
indb = mycursor.fetchall()
if indb:
    print(indb[0])