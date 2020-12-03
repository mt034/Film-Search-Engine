import psycopg2
import os
import srt

#Ask for database info to connect
database = input("Enter database name: ")
user = input("Enter username: ")
password = input("Enter password: ")
host = input("Enter host: ")

#Connect to database using database name, username, password, host, port
conn = psycopg2.connect(database= database, user = user, password = password, host = host, port = "5432")
print("Opened database successfully")


#Get a cursor from the database connection
cur = conn.cursor()

#variable for ID
ID = 1

#boolean to stop the program or continue
cont = True

#Create a database table from the connector 'conn' with the fixed attributes
cur.execute("CREATE TABLE FILM \
     (ID INT PRIMARY KEY     NOT NULL,\
      TITLE           TEXT    NOT NULL,\
      YEAR            INT     NOT NULL,\
      GENRE        TEXT);")

def insert(cur, title, year, genre):
    """Insert record into the database"""
    global ID
    cur.execute("INSERT INTO FILM (ID,TITLE,YEAR,GENRE) \
    VALUES ({}, {}, {}, {})".format(ID, title, year, genre));
    conn.commit()
    #increment ID variable
    ID += 1
    print("Record created successfully")
    
def get_binary_array(path):
    with open(path, "rb") as image:
        f = image.read()
        b = bytes(f).hex()
        return b

def insertImages(conn, cur, file_names):
    query = "INSERT INTO SCREENSHOTS VALUES (decode(%s, 'hex'))"
    mylist = []
    for file_name in file_names:
        mylist.append(get_binary_array(file_name))

    try:
        cur.executemany(query, mylist)
       
        conn.commit()
        count = cur.rowcount # check that the images were all successfully added
        print (count, "Records inserted successfully into table")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insertSubs(conn, cur, sub_list):
    query = "INSERT INTO SUBTITLES VALUES (%s)"
    try:
        cur.executemany(query, sub_list)
       
        conn.commit()
        count = cur.rowcount # check that the subs were all successfully added
        print (count, "Records inserted successfully into table")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#prompt user for information to be inserted
while cont:
    #prompt user for directory
    directory = input("Enter directory with screenshots: ")
    #list of screenshots to be added
    screenshots = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            screenshots += [filename]
            
    #prompt user for filename containing subtiles
    filename = input("Enter .srt filename: ")
    #open .srt file and read into a string
    f = open(filename, "r", encoding = "utf-8")
    text = f.read()
    #parse string into list of subtitles to be added
    subs = list(srt.parse('''\
{}'''.format(text)))
    #prompt user for movie information
    title = input("Enter title: ")
    year = int(input("Enter year: "))
    genre = input("Enter genre: ")
    insertImages(conn,cur,screenshots)
    insertSubs(conn,cur,subs)
    insert(cur,title,year,genre)
    cont = input("Press y to continue, n to exit ")
    if cont == "y":
        continue
    elif cont == "n":
        break

#close the connection
conn.close()

