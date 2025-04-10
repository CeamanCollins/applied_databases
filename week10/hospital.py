import pymysql

conn = None

def main():
    while True:
        displaymenu()
        choice = input("Please select an option: ")
        if int(choice) == 1:
            doinsert()
        if int(choice) == 2:
            dosearch()
        if int(choice) == -1:
            break

def connect():
    global conn
    conn = pymysql.connect(host="localhost", user="root", password="root", database="hospital", cursorclass=pymysql.cursors.DictCursor)

def displaymenu():
    print("Options\n===============\n\n1\tAdd new patient\n2\tSearch for patient\n\n")

def doinsert():
    if (not conn):
        connect()
    ppsn = input("PPSN: ")
    firstname = input("fName: ")
    surname = input("Surname: ")
    address = input("Address: ")
    doctorid = input("Doctor ID: ")
    sql_insert = "INSERT INTO patient_table (ppsn, first_name, surname, address, doctorID) VALUES (%s, %s, %s, %s, %s)"

    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql_insert, (ppsn, firstname, surname, address, doctorid))
            conn.commit()
        except pymysql.err.IntegrityError:
            print("Existing PPSN, or non-existant DoctorID entered")
        except pymysql.err.InternalError as e:
            print("Internal Error:", e)
        except Exception as e:
            print("Exception:", e)

def dosearch():
    if (not conn):
        connect()
    surname = input("Surname: ")
    with conn:
        cursor = conn.cursor()
        sql_search = "SELECT * FROM patient_table WHERE surname LIKE CONCAT(%s, '%%')"
        sql_search_doctor = "SELECT * FROM doctor_table WHERE doctorID = %s"
        cursor.execute(sql_search, (surname))
        results = cursor.fetchall()
        print("\n")
        for result in results:
            doctorID = result['doctorID']
            cursor.execute(sql_search_doctor, (doctorID))
            result_doctor = cursor.fetchall()
            print(result['ppsn'],"|",result['first_name'],"|",result["surname"],"|",result_doctor[0]['name'])
        print("\n")


if __name__ == "__main__":
    main()