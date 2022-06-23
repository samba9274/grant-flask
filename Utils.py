from math import sin, cos, sqrt, atan2, radians
from mysqlx import SSLMode
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

conn_dict = psycopg.conninfo.conninfo_to_dict(os.getenv("DATABASE_URL"))


conn = psycopg.connect(**conn_dict, sslmode="disable")

mycursor = conn.cursor()


def resetDB():
    mycursor.execute("DROP TABLE IF EXISTS images,donations, users")
    conn.commit()
    mycursor.execute("CREATE TABLE users(userId int NOT NULL UNIQUE,name varchar(35) NOT NULL,email varchar(50) NOT NULL UNIQUE,password varchar(32) NOT NULL,mobile varchar(10) NOT NULL,latitude float,longitude float,role varchar(10) NOT NULL,PRIMARY KEY (userId))")
    conn.commit()
    mycursor.execute("CREATE TABLE donations(donationId int NOT NULL UNIQUE,donoruserId int NOT NULL,description varchar(300) NOT NULL,inventory int NOT NULL,donationDate timestamp NOT NULL,recieveruserId int,acceptationDate timestamp,donationStatus char(10) NOT NULL,PRIMARY KEY (donationId),FOREIGN KEY (donoruserId) REFERENCES users(userId),FOREIGN KEY (recieveruserId) REFERENCES users(userId))")
    conn.commit()
    mycursor.execute("CREATE TABLE images(imageId int NOT NULL UNIQUE,donationId int NOT NULL,image bytea NOT NULL,PRIMARY KEY (imageId),FOREIGN KEY (donationId) REFERENCES donations(donationId))")
    conn.commit()
    mycursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (1,
                                                                                   "Admin",
                                                                                   "admin@email.com",
                                                                                   os.getenv(
                                                                                       "ADMIN_PASSWORD"),
                                                                                   "0000000000", 0, 0, "ADMIN"))
    conn.commit()


def calcDistance(p1, p2):
    return (6371 * 2 * atan2(sqrt((sin(abs(radians(p2[0]) - radians(p1[0])) / 2)**2 + cos(p1[0]) * cos(p2[0]) * sin(abs(radians(p2[1]) - radians(p1[1])) / 2)**2)), sqrt(
        1 - (sin(abs(radians(p2[0]) - radians(p1[0])) / 2)**2 + cos(p1[0]) * cos(p2[0]) * sin(abs(radians(p2[1]) - radians(p1[1])) / 2)**2))))
