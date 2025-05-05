import pymysql
from neo4j import GraphDatabase
import random
import textwrap

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "rootroot")


def main():
    while True:
        displaymenu()
        choice = input("Choice: ")
        if choice == 'x':
            break
        try:
            choice = int(choice)
        except ValueError:
            continue
        if choice == 1:
            dodirectorsandfilms()
        if choice == 2:
            domonth()
        if choice == 3:
            doinsertactor()
        if choice == 4:
            domarried()
        if choice == 5:
            doaddmarriage()
        if choice == 6:
            dostudios()
        if choice == 7:
            dorecommend()
        if choice == 8:
            doactorsandfilms()
        if choice == 9:
            doupdategenre()


def connect():
    global conn
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="appdbproj",
        cursorclass=pymysql.cursors.DictCursor
        )


def displaymenu():
    print(
        "MoviesDB\n--------\n\n"
        "MENU\n"
        "====\n"
        "1 - View Directors & Films\n"
        "2 - View Actors by Month of Birth\n"
        "3 - Add New Actor\n"
        "4 - View Married Actors\n"
        "5 - Add Actor Marriage\n"
        "6 - View Studios\n"
        "7 - Recommend a Film\n"
        "8 - Search Films by Actor Name\n"
        "9 - Update Genre\n"
        "x - Exit application"
        )


def dodirectorsandfilms():
    connect()
    director = input("Enter Director Name: ")
    sql_search = "SELECT d.DirectorName, f.FilmName, s.StudioName " \
                 "FROM director d " \
                 "INNER JOIN film f on f.FilmDirectorID = d.DirectorID " \
                 "INNER JOIN studio s on s.StudioID = f.FilmStudioID " \
                 "WHERE d.DirectorName LIKE CONCAT('%%' %s '%%');"
    with conn.cursor() as cursor:
        cursor.execute(sql_search, (director))
        results = cursor.fetchall()
        if len(results) == 0:
            print(
                "\n--------------------------\n"
                "No directors found of that name"
                )
        else:
            print("\n--------------------------\n")
            for result in results:
                print(result['DirectorName'], "|",
                      result['FilmName'], "|",
                      result['StudioName']
                      )
            print("\n--------------------------\n\n")


def domonth():
    connect()
    while True:
        month = input("Enter Month: ")
        months = {'jan': 1,
                  'feb': 2,
                  'mar': 3,
                  'apr': 4,
                  'may': 5,
                  'jun': 6,
                  'jul': 7,
                  'aug': 8,
                  'sep': 9,
                  'oct': 10,
                  'nov': 11,
                  'dec': 12
                  }
        if month.lower() in months.keys():
            month = month.lower()
            month = months[month]
            break
        else:
            try:
                month = int(month)
            except ValueError:
                continue
            if month > 0 and month < 13:
                break
    sql_search = "SELECT ActorName, date(ActorDOB) " \
                 "AS ActorDob, ActorGender " \
                 "FROM actor " \
                 "WHERE MONTH(ActorDOB) = %s"
    with conn.cursor() as cursor:
        cursor.execute(sql_search, (month,))
        results = cursor.fetchall()
        print("\n--------------------------\n")
        for result in results:
            print(result['ActorName'],
                  "|", result['ActorDob'],
                  "|", result['ActorGender'])
        print("\n--------------------------\n\n")


def doinsertactor():
    connect()
    actorid = input("Actor ID: ")
    name = input("Name: ")
    dob = input("DOB: ")
    gender = input("Gender: ")
    countryid = input("Country ID: ")
    sql_insert = "INSERT INTO actor (ActorID, ActorName, " \
                 "ActorDOB, ActorGender, ActorCountryID) " \
                 "VALUES (%s, %s, %s, %s, %s)"

    with conn.cursor() as cursor:
        try:
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
    actorid_input = input("\nEnter ActorID: ")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            "MATCH (p{ActorID: $actoridinput})-[:MARRIED_TO]-(q) "
            "RETURN p{ActorID: p.ActorID}, q{ActorID: q.ActorID}",
            parameters_={"actoridinput": int(actorid_input)},
            database_="actorsmarried",
        )
    if records == []:
        print("\n----------------\nThis actor is not married\n")
    else:
        ActorID1 = records[0].data()['p']['ActorID']
        ActorID2 = records[0].data()['q']['ActorID']

        connect()
        sql_actors = "SELECT ActorID, ActorName " \
                     "FROM actor " \
                     "WHERE ActorID = %s OR ActorID = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql_actors, (ActorID1, ActorID2))
            result = cursor.fetchall()
        print("\n----------------\nThese Actors are married:")
        for actor in result:
            print(actor['ActorID'], "|", actor['ActorName'])
        print("\n")


def doaddmarriage():
    connect()
    while True:
        print("\r")
        Actor1ID = input("Enter Actor 1 ID: ")
        Actor2ID = input("Enter Actor 2 ID: ")
        if Actor1ID == Actor2ID:
            print("An actor cannot marry him/herself")
            continue
        try:
            Actor1ID = int(Actor1ID)
            Actor2ID = int(Actor2ID)
        except ValueError:
            continue
        sql = "SELECT * FROM actor"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except pymysql.err.Error as e:
            print(f"*** ERROR *** {e}")
            break
        lastid = result[-1]['ActorID']
        if Actor1ID < 0 or Actor1ID > int(lastid):
            print(f"Actor {Actor1ID} does not exist.")
        if Actor2ID < 0 or Actor2ID > int(lastid):
            print(f"Actor {Actor2ID} does not exist.")
        else:
            break

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records1, _, _ = driver.execute_query(
            "MATCH ({ActorID: $Actor1})-[r1:MARRIED_TO]-() RETURN r1",
            parameters_={"Actor1": Actor1ID},
            database_="actorsmarried",
        )
        if len(records1) == 1:
            print(f"Actor {Actor1ID} is already married")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records2, _, _ = driver.execute_query(
            "MATCH ({ActorID: $Actor2})-[r1:MARRIED_TO]-() RETURN r1",
            parameters_={"Actor2": Actor2ID},
            database_="actorsmarried",
        )
        if len(records2) == 1:
            print(f"Actor {Actor2ID} is already married")

    if len(records1) != 1 and len(records2) != 1:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.execute_query(
                "MERGE(:Actor{ActorID: $Actor1})-"
                "[:MARRIED_TO]->(:Actor{ActorID: $Actor2})",
                parameters_={"Actor1": Actor1ID, "Actor2": Actor2ID},
                database_="actorsmarried",
            )
        print(f"Actor {Actor1ID} and {Actor2ID} are now married")


def dostudios():
    global studio_result
    if 'studio_result' in globals():
        print("StudioID\t|\tStudioName")
        for studio in studio_result:
            print(f"{studio['StudioID']}\t\t|\t{studio['StudioName']}")
    else:
        connect()
        sql_studios = "select * from studio order by StudioID"
        with conn.cursor() as cursor:
            cursor.execute(sql_studios)
            studio_result = cursor.fetchall()
            print("StudioID\t|\tStudioName")
            for studio in studio_result:
                print(f"{studio['StudioID']}\t\t|\t{studio['StudioName']}")


def dorecommend():
    while True:
        age = input('How old are you? ')
        try:
            age = int(age)
            break
        except ValueError:
            continue
    if age <= 12:
        while True:
            parents = input('Are your parent(s)/'
                            'guardian(s) watching too? (y/n) ').lower()
            if parents in ['y', 'n']:
                break
    if age >= 18:
        category = 6
    if age <= 17:
        category = 5
    if age <= 14:
        category = 4
    if age == 12 and parents == 'y':
        category = 4
    if age == 12 and parents == 'n':
        category = 3
    if age <= 11:
        category = 2
    if age <= 9 and parents == 'y':
        category = 2
    if age <= 9 and parents == 'n':
        category = 1
    connect()
    sql_recommend = "SELECT f.FilmName as 'Film Name', " \
        "f.FilmSynopsis, c.Certificate " \
        "FROM film f INNER JOIN certificate c " \
        "ON f.FilmCertificateID = c.CertificateID " \
        "WHERE c.CertificateID <= %s;"
    with conn.cursor() as cursor:
        cursor.execute(sql_recommend, (category))
        recommend_result = cursor.fetchall()
    length = len(recommend_result)-1
    selection = random.randint(0, length)
    print(f"\nRecommended Film: {recommend_result[selection]['Film Name']}\n"
          f"Rated: {recommend_result[selection]['Certificate']}")
    print("Synopsis:", end="")
    wrapped_text = textwrap.wrap(
                                recommend_result[selection]['FilmSynopsis'],
                                width=65
                                )
    print(wrapped_text[0])
    for line in wrapped_text[1:]:
        print("\t", line)
    print("\n\n")


def doactorsandfilms():
    actor = input("Enter Actor Name: ")
    connect()
    sql_actors = "SELECT a.ActorName, fc.CastCharacterName, f.FilmName " \
                 "FROM actor a " \
                 "INNER JOIN filmcast fc ON fc.CastActorID = a.ActorID " \
                 "INNER JOIN film f ON fc.CastFilmID = f.FilmID " \
                 "WHERE a.ActorName LIKE CONCAT ('%%' %s '%%');"
    with conn.cursor() as cursor:
        cursor.execute(sql_actors, (actor))
        results = cursor.fetchall()
        print("\n--------------------------\n")
        print("Actor Name | Character Name | Film Name")
        print("-----------|----------------|----------")
        for result in results:
            print(
                result['ActorName'],
                "|",
                result['CastCharacterName'],
                "|", result['FilmName']
                )
        print("\n--------------------------\n\n")


def doupdategenre():
    connect()
    sql_populate_genre = "SELECT f.FilmName, g.GenreName " \
                         "FROM film f " \
                         "INNER JOIN genre g " \
                         "ON f.FilmGenreID = g.GenreId " \
                         "WHERE g.GenreName = 'Other';"
    with conn.cursor() as cursor:
        cursor.execute(sql_populate_genre)
        results = cursor.fetchall()
    selection = random.randint(0, len(results)-1)
    filmname = results[selection]['FilmName']
    print("Film:", filmname)
    print("Action, Comedy, Drama, Musical, Romantic, Other")
    while True:
        selected_genre = input("Enter Genre: ").capitalize()
        genres = {
            'Action': 1,
            'Comedy': 4,
            'Drama': 2,
            'Musical': 5,
            'Romantic': 3,
            'Other': 6
            }
        if selected_genre in genres.keys():
            sql_update_genre = "UPDATE film " \
                               "SET FilmGenreID = %s " \
                               "WHERE FilmName = %s;"
            with conn.cursor() as cursor:
                cursor.execute(
                    sql_update_genre,
                    (genres[selected_genre], filmname)
                    )
                conn.commit()
            print("\n--------------------------\n")
            print("Genre updated:")
            print(f"Film {filmname} updated to {selected_genre}")
            print("\n--------------------------\n")
            break
        else:
            print("\n--------------------------\n")
            print(f"Genre {selected_genre} does not exist. "
                  f"Please choose from the following: ")
            print("Action, Comedy, Drama, Musical, Romantic, Other")
            print("\n--------------------------\n")

if __name__ == "__main__":
    main()
