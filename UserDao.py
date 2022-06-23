from User import User
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

conn_dict = psycopg.conninfo.conninfo_to_dict(os.getenv("DATABASE_URL"))


conn = psycopg.connect(**conn_dict, sslmode="disable")

mycursor = conn.cursor()


def getNextuserId():
    mycursor = conn.cursor()
    mycursor.execute("select max(userId) from users")
    r = mycursor.fetchone()
    if r[0]:
        return r[0]+1
    return 1


def getUserById(id):
    mycursor.execute("SELECT * FROM users WHERE userId=%s", tuple([id]))
    return mycursor.fetchone()[0]


def insertUser(user):
    mycursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user.userId,
                                                                                   user.name,
                                                                                   user.email,
                                                                                   user.password,
                                                                                   user.mobile,
                                                                                   user.latitude,
                                                                                   user.longitude,
                                                                                   user.role))
    conn.commit()


def getUserByEmail(email):
    mycursor.execute("SELECT * FROM users WHERE email=%s", tuple([email]))
    userTuple = mycursor.fetchone()
    return User(userTuple[0], userTuple[1], userTuple[2], userTuple[3], userTuple[4], userTuple[5], userTuple[6], userTuple[7])


def getAllEmails():
    mycursor.execute("SELECT DISTINCT email FROM users")
    return mycursor.fetchall()


def getUserById(id):
    mycursor.execute("SELECT * FROM users WHERE userId=%s", tuple([id]))
    userTuple = mycursor.fetchone()
    user = User(userTuple[0], userTuple[1], userTuple[2], userTuple[3],
                userTuple[4], userTuple[5], userTuple[6], userTuple[7])
    return user


def fetchReport():
    report = dict()
    mycursor.execute('SELECT COUNT(role) FROM users WHERE role="USER"')
    report["Users"] = mycursor.fetchone()[0]
    mycursor.execute('SELECT COUNT(role) FROM users WHERE role="INSTITUTE"')
    report["Institutes"] = mycursor.fetchone()[0]
    mycursor.execute(
        'SELECT COUNT(donationStatus) FROM donations WHERE donationStatus="PENDING"')
    report["Pending-Donations"] = mycursor.fetchone()[0]
    mycursor.execute(
        'SELECT COUNT(donationStatus) FROM donations WHERE donationStatus="COMPLETED"')
    report["Completed-Donations"] = mycursor.fetchone()[0]
    mycursor.execute(
        'SELECT COUNT(donationStatus) FROM donations WHERE donationStatus="REPORTED"')
    report["Reported-Donations"] = mycursor.fetchone()[0]
    mycursor.execute(
        'SELECT COUNT(donationStatus) FROM donations WHERE donationStatus="DELETED"')
    report["Deleted-Donations"] = mycursor.fetchone()[0]
    return report
