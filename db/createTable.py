from connect import mydb,mycursor

# mycursor.execute("CREATE TABLE visitors (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(20)NOT NULL)")
mycursor.execute("ALTER TABLE visitors ADD COLUMN started_At DATE ")
# mycursor.execute("INSERT INTO visitors ('', '') ")
mycursor.execute("SHOW TABLES")

for x in mycursor: # type: ignore
  print(x)

