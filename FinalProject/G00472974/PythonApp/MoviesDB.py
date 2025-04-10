import pymysql
from neo4j import GraphDatabase, RoutingControl

URI = "neo4j://localhost"
AUTH = ("neo4j", "rootroot")

def main():
    while True:
        displaymenu()
        choice = input("Choice: ")
        if choice == 'x':
            break
        if int(choice) == 1:
            dodirectorsandfilms()
        if int(choice) == 2:
            domonth()
        if int(choice) == 3:
            doinsertactor()
        if int(choice) == 4:
            domarried()
        if int(choice) == 5:
            doaddmarriage()
        if int(choice) == 6:
            dostudios()  


def connect():
    global conn
    conn = pymysql.connect(host="localhost", user="root", password="root", database="appdbproj", cursorclass=pymysql.cursors.DictCursor)

def displaymenu():
    print("MoviesDB\n--------\n\nMENU\n====\n1 - View Directors & Films\n2 - View Actors by Month of Birth\n3 - Add New Actor\n4 - View Married Actors\n5 - Add Actor Marriage\n6 - View Studios\nx - Exit application")

def dodirectorsandfilms():
    connect()
    director = input("Enter Director Name: ")
    sql_search = "SELECT d.DirectorName, f.FilmName, s.StudioName FROM director d INNER JOIN film f on f.FilmDirectorID = d.DirectorID INNER JOIN studio s on s.StudioID = f.FilmStudioID WHERE d.DirectorName LIKE CONCAT('%%' %s '%%');"

    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql_search, (director))
            results = cursor.fetchall()
            if len(results) == 0:
                print("\n--------------------------\nNo directors found of that name")
            else:
                print("\n--------------------------\n")
                for result in results:
                    print(result['DirectorName'], "|", result['FilmName'], "|", result['StudioName'])
                print("\n--------------------------\n\n")
        except:
            print("Encountered Error")

def domonth():
    connect()
    while True:
        month = input("Enter Month: ")
        months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
        if type(month) == int:
            if month > 0 and month < 13:
                break
        elif month[0:3].lower() in months.keys():
            month = month[0:3].lower()
            month = months[month]
            break
    sql_search = "Select ActorName, date(ActorDOB) as ActorDob, ActorGender from actor where month(ActorDOB) = %s"

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql_search, (month,))
        results = cursor.fetchall()
        print("\n--------------------------\n")
        for result in results:
            print(result['ActorName'], "|", result['ActorDob'], "|", result['ActorGender'])
        print("\n--------------------------\n\n")

def doinsertactor():
    connect()
    actorid = input("Actor ID: ")
    name = input("Name: ")
    dob = input("DOB: ")
    gender = input("Gender: ")
    countryid = input("Country ID: ")
    sql_insert = "INSERT INTO actor (ActorID, ActorName, ActorDOB, ActorGender, ActorCountryID) VALUES (%s, %s, %s, %s, %s)"

    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql_insert, (actorid, name, dob, gender, countryid))
            conn.commit()
            print("\n--------------------------\n")
            print("Actor successfully added")
            print("\n--------------------------\n\n")
        except pymysql.err.IntegrityError as e:
            if e[0:4] == 1062:
                print(f"*** ERROR *** Actor ID: {actorid} already exists")
            if e[0:4] == 1452:
                print(f"*** ERROR *** Country ID: {countryid} does not exist")
            else:
                print(f"*** ERROR *** {e}")
        except pymysql.err.InternalError as e:
            print(f"*** ERROR *** {e}")
        except Exception as e:
            print(f"*** ERROR *** {e}")

def domarried():
    actorid_input = input("Enter ActorID: ")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records = driver.execute_query(
            "MATCH (p{ActorID: 1})-[:MARRIED_TO]-(q) RETURN p, q",
            actoridinput="1",
            database_="actorsmarried"
        ).records
    for person in records:
        print(person)

def doaddmarriage():
    pass

def dostudios():
    connect()
    sql_studios = "select * from studio order by StudioID"
    with conn: 
        cursor = conn.cursor()
        cursor.execute(sql_studios)
        result = cursor.fetchall()
        print("StudioID\t|\tStudioName")
        for studio in result:
            print(f"{studio['StudioID']}\t\t|\t{studio['StudioName']}")

if __name__ == "__main__":
    main()