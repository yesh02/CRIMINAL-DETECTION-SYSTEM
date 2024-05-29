import pymysql

def insertData(data):
    """
    Insert criminal data into the database.
    
    Args:
    - data: Dictionary containing criminal data
    
    Returns:
    - ID of the inserted row
    """
    rowId = 0

    db = pymysql.connect(host="criminaldb.cpk0ayggcs0v.eu-north-1.rds.amazonaws.com", user="admin", password="yeshwanth", database="criminaldb")
    cursor = db.cursor()
    print("Database connected")

    query = "INSERT INTO criminaldata VALUES(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
            (data["Name"], data["Father's Name"], data["Mother's Name"], data["Gender"],
             data["DOB(yyyy-mm-dd)"], data["Blood Group"], data["Identification Mark"],
             data["Nationality"], data["Religion"], data["Crimes Done"])

    try:
        cursor.execute(query)
        db.commit()
        rowId = cursor.lastrowid
        print("Data stored on row %d" % rowId)
    except:
        db.rollback()
        print("Data insertion failed")

    db.close()
    print("Connection closed")
    return rowId

def retrieveData(name):
    """
    Retrieve criminal data from the database based on the name.
    
    Args:
    - name: Name of the criminal
    
    Returns:
    - Tuple containing ID and criminal data
    """
    id = None
    criminaldata = None

    db = pymysql.connect(host="criminaldb.cpk0ayggcs0v.eu-north-1.rds.amazonaws.com", user="admin", password="yeshwanth", database="criminaldb")
    cursor = db.cursor()
    print("Database connected")

    query = "SELECT * FROM criminaldata WHERE name='%s'" % name

    try:
        cursor.execute(query)
        result = cursor.fetchone()

        id = result[0]
        criminaldata = {
            "Name": result[1],
            "Father's Name": result[2],
            "Mother's Name": result[3],
            "Gender": result[4],
            "DOB(yyyy-mm-dd)": result[5],
            "Blood Group": result[6],
            "Identification Mark": result[7],
            "Nationality": result[8],
            "Religion": result[9],
            "Crimes Done": result[10]
        }

        print("Data retrieved")
    except:
        print("Error: Unable to fetch data")

    db.close()
    print("Connection closed")

    return id, criminaldata
